"""Config flow for AirHealth."""

import logging

import voluptuous as vol
from aiohttp import ClientError

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AirHealthApiClient, AirHealthAuthError, AirHealthDataError
from .const import API_ENDPOINTS, CONF_API_KEY, CONF_SAL_CODE, DOMAIN

_LOGGER = logging.getLogger(__name__)


class AirHealthConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AirHealth."""

    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self._api_key: str | None = None
        self._sal_code: str | None = None

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._api_key = user_input[CONF_API_KEY]
            self._sal_code = user_input[CONF_SAL_CODE]

            await self.async_set_unique_id(self._sal_code)
            self._abort_if_unique_id_configured()

            try:
                session = async_get_clientsession(self.hass)
                api = AirHealthApiClient(self._api_key, session)
                test_endpoint = next(iter(API_ENDPOINTS.values()))
                await api.async_get_data(test_endpoint["path"], self._sal_code)
            except AirHealthAuthError:
                errors["base"] = "invalid_auth"
            except (AirHealthDataError, ClientError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error")
                errors["base"] = "unknown"
            else:
                return await self.async_step_endpoints()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_SAL_CODE): str,
                }
            ),
            errors=errors,
        )

    async def async_step_endpoints(self, user_input=None) -> ConfigFlowResult:
        """Handle endpoint selection step."""
        if user_input is not None:
            data = {
                CONF_API_KEY: self._api_key,
                CONF_SAL_CODE: self._sal_code,
                **user_input,
            }

            return self.async_create_entry(
                title=f"AirHealth (SAL {self._sal_code})",
                data=data,
            )

        schema = vol.Schema(
            {vol.Required(ep_key, default=True): bool for ep_key in API_ENDPOINTS}
        )

        return self.async_show_form(step_id="endpoints", data_schema=schema)
