"""The AirHealth integration."""

import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AirHealthApiClient
from .const import CONF_API_KEY
from .coordinator import AirHealthConfigEntry, AirHealthDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: AirHealthConfigEntry) -> bool:
    """Set up AirHealth from a config entry."""
    session = async_get_clientsession(hass)
    api_client = AirHealthApiClient(entry.data[CONF_API_KEY], session)

    coordinator = AirHealthDataUpdateCoordinator(hass, entry, api_client)
    await coordinator.async_config_entry_first_refresh()

    coordinator.setup_scheduled_updates()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: AirHealthConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator: AirHealthDataUpdateCoordinator = entry.runtime_data
    coordinator.shutdown()

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
