"""Test AirHealth config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.airhealth.api import AirHealthAuthError, AirHealthDataError
from custom_components.airhealth.const import (
    CONF_API_KEY,
    CONF_SAL_CODE,
    DOMAIN,
)


async def test_form_user_step(hass: HomeAssistant) -> None:
    """Test user step shows form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}


async def test_form_user_valid_credentials(
    hass: HomeAssistant, mock_airhealth_api
) -> None:
    """Test successful authentication leads to endpoint selection."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_airhealth_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "endpoints"
    assert result["errors"] == {}


async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test invalid authentication error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    mock_api = AsyncMock()
    mock_api.async_get_data.side_effect = AirHealthAuthError("Invalid credentials")

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "invalid_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    mock_api = AsyncMock()
    mock_api.async_get_data.side_effect = AirHealthDataError("Connection failed")

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: HomeAssistant) -> None:
    """Test unknown error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    mock_api = AsyncMock()
    mock_api.async_get_data.side_effect = Exception("Unexpected error")

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "unknown"}


async def test_form_duplicate_sal_code(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry
) -> None:
    """Test duplicate SAL code is rejected."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_airhealth_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",  # Same as mock_config_entry
            },
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_endpoints_step_all_enabled(
    hass: HomeAssistant, mock_airhealth_api
) -> None:
    """Test endpoint selection with all endpoints enabled."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_airhealth_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "endpoints"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "grass_pollen": True,
            "other_allergens": True,
            "aq_woodsmoke": True,
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "AirHealth (SAL 12345)"
    assert result["data"] == {
        CONF_API_KEY: "test_api_key",
        CONF_SAL_CODE: "12345",
        "grass_pollen": True,
        "other_allergens": True,
        "aq_woodsmoke": True,
    }


async def test_endpoints_step_partial_enabled(
    hass: HomeAssistant, mock_airhealth_api
) -> None:
    """Test endpoint selection with some endpoints disabled."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_airhealth_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "67890",
            },
        )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "grass_pollen": True,
            "other_allergens": False,
            "aq_woodsmoke": True,
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "AirHealth (SAL 67890)"
    assert result["data"]["grass_pollen"] is True
    assert result["data"]["other_allergens"] is False
    assert result["data"]["aq_woodsmoke"] is True


async def test_endpoints_step_shows_form(
    hass: HomeAssistant, mock_airhealth_api
) -> None:
    """Test endpoint selection shows form with all endpoint options."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.airhealth.config_flow.AirHealthApiClient",
        return_value=mock_airhealth_api,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_API_KEY: "test_api_key",
                CONF_SAL_CODE: "12345",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "endpoints"

    # Check that all endpoint keys are in the schema
    schema_keys = list(result["data_schema"].schema.keys())
    assert len(schema_keys) == 3  # grass_pollen, other_allergens, aq_woodsmoke
    assert any("grass_pollen" in str(key) for key in schema_keys)
    assert any("other_allergens" in str(key) for key in schema_keys)
    assert any("aq_woodsmoke" in str(key) for key in schema_keys)
