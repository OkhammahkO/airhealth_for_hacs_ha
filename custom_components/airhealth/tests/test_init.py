"""Tests for the AirHealth integration."""
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import DOMAIN


async def test_setup_entry(hass: HomeAssistant, mock_api):
    """Test setting up a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "test_api_key", "sal_code": "12345"},
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.data[DOMAIN][entry.entry_id]
    coordinator = hass.data[DOMAIN][entry.entry_id]
    assert coordinator.data is not None
    assert "grass_pollen" in coordinator.data
    assert "other_allergens" in coordinator.data
    assert "aq_woodsmoke" in coordinator.data
