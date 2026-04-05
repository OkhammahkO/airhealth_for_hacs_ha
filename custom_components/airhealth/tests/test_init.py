"""Tests for the AirHealth integration."""
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.coordinator import AirHealthDataUpdateCoordinator


async def test_setup_entry(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
) -> None:
    """Test setting up a config entry."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator: AirHealthDataUpdateCoordinator = mock_config_entry.runtime_data
    assert coordinator.data is not None
    assert "grass_pollen" in coordinator.data
    assert "other_allergens" in coordinator.data
    assert "aq_woodsmoke" in coordinator.data


async def test_unload_entry(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
) -> None:
    """Test unloading a config entry."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
