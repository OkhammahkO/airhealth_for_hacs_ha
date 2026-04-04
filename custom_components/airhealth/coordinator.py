"""DataUpdateCoordinator for AirHealth integration."""

from collections.abc import Callable
from datetime import datetime
import logging
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AirHealthApiClient, AirHealthAuthError, AirHealthDataError
from .const import API_ENDPOINTS, CONF_SAL_CODE, DOMAIN

_LOGGER = logging.getLogger(__name__)

type AirHealthConfigEntry = ConfigEntry["AirHealthDataUpdateCoordinator"]


class AirHealthDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching AirHealth data."""

    config_entry: AirHealthConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: AirHealthConfigEntry,
        api_client: AirHealthApiClient,
    ) -> None:
        """Initialize coordinator."""
        self.api_client = api_client
        self.sal_code = config_entry.data[CONF_SAL_CODE]
        self._unsub_trackers: list[Callable[[], None]] = []

        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
        )

    def setup_scheduled_updates(self) -> None:
        """Schedule time-based updates for each enabled endpoint."""
        for endpoint_key, endpoint_info in API_ENDPOINTS.items():
            if not self.config_entry.data.get(endpoint_key):
                continue

            for hour, minute in endpoint_info["update_times"]:
                unsub = async_track_time_change(
                    self.hass,
                    self._async_scheduled_refresh,
                    hour=hour,
                    minute=minute,
                    second=0,
                )
                self._unsub_trackers.append(unsub)
                _LOGGER.debug(
                    "Scheduled daily refresh for %s at %02d:%02d AEST",
                    endpoint_key,
                    hour,
                    minute,
                )

    async def _async_scheduled_refresh(self, now) -> None:
        """Handle scheduled refresh."""
        await self.async_request_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from all enabled endpoints."""
        fetched_data = {}

        for endpoint_key, endpoint_info in API_ENDPOINTS.items():
            if not self.config_entry.data.get(endpoint_key):
                continue

            try:
                data = await self.api_client.async_get_data(
                    endpoint_info["path"], self.sal_code
                )
                # Wrap data with metadata
                fetched_data[endpoint_key] = {
                    "forecast": data.get("forecast", []),
                    "last_successful_update": datetime.now(ZoneInfo(self.hass.config.time_zone)).isoformat(),
                    "api_status": "ok",
                }
            except AirHealthAuthError as err:
                # Authentication errors - check for quota exceeded (403)
                if self.data and endpoint_key in self.data:
                    _LOGGER.warning(
                        "Authentication failed for %s (quota exceeded?), using cached data: %s",
                        endpoint_key,
                        err,
                    )
                    fetched_data[endpoint_key] = {
                        **self.data[endpoint_key],
                        "api_status": "quota_exceeded",
                    }
                else:
                    raise UpdateFailed(
                        f"Authentication failed for {endpoint_key}: {err}"
                    ) from err
            except AirHealthDataError as err:
                if self.data and endpoint_key in self.data:
                    _LOGGER.warning(
                        "Failed to fetch %s, using cached data: %s", endpoint_key, err
                    )
                    fetched_data[endpoint_key] = {
                        **self.data[endpoint_key],
                        "api_status": "error",
                    }
                else:
                    raise UpdateFailed(
                        f"Failed to fetch {endpoint_key}: {err}"
                    ) from err

        return fetched_data

    def shutdown(self) -> None:
        """Clean up time trackers."""
        for unsub in self._unsub_trackers:
            unsub()
        self._unsub_trackers.clear()
