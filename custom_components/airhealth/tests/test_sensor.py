"""Tests for the sensor platform."""
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import DOMAIN, get_level_icon


async def test_sensor_setup(hass: HomeAssistant, mock_api):
    """Test the setup of the sensor platform."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "test_api_key", "sal_code": "12345"},
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    # Check that the sensors have been created
    assert len(hass.states.async_all()) == 9

    # Check the state of one of the sensors
    grass_pollen_sensor = hass.states.get("sensor.grass_pollen_level")
    assert grass_pollen_sensor is not None
    assert grass_pollen_sensor.state == "Low"


async def test_sensor_level_icon_attribute(hass: HomeAssistant, mock_airhealth_api, mock_config_entry):
    """Test that sensors have level_icon attribute."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Test grass pollen sensor has level_icon
    state = hass.states.get("sensor.airhealth_grass_day0")
    if state:
        assert "level_icon" in state.attributes
        level = state.state
        expected_icon = get_level_icon(level)
        assert state.attributes["level_icon"] == expected_icon


async def test_allergen_breakdown_icons(hass: HomeAssistant, mock_airhealth_api, mock_config_entry):
    """Test that allergen breakdown includes level_icon for each allergen."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Test other allergens sensor has allergen breakdown with icons
    state = hass.states.get("sensor.airhealth_other_allergens_day0")
    if state and "allergens" in state.attributes:
        allergens = state.attributes["allergens"]
        for allergen in allergens:
            assert "level_icon" in allergen
            level = allergen.get("level")
            if level:
                expected_icon = get_level_icon(level)
                assert allergen["level_icon"] == expected_icon


def test_get_level_icon():
    """Test the get_level_icon helper function."""
    assert get_level_icon("Low") == "🟢"
    assert get_level_icon("None") == "🟢"
    assert get_level_icon("Moderate") == "🟡"
    assert get_level_icon("High") == "🟠"
    assert get_level_icon("Extreme") == "🔴"
    assert get_level_icon("Unknown") == "⚪"
    assert get_level_icon(None) == "⚪"


async def test_sensor_metadata_attributes(hass: HomeAssistant, mock_airhealth_api, mock_config_entry):
    """Test that sensors have metadata attributes."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Test grass pollen sensor has metadata
    state = hass.states.get("sensor.airhealth_grass_day0")
    if state:
        assert "last_successful_update" in state.attributes
        assert "api_status" in state.attributes
        # Verify api_status is valid
        assert state.attributes["api_status"] in ["ok", "error", "quota_exceeded", "unavailable"]
        # Verify timestamp format (ISO 8601 compatible)
        timestamp = state.attributes.get("last_successful_update")
        if timestamp:
            # Should be a string in ISO 8601 format
            assert isinstance(timestamp, str)
            assert "T" in timestamp  # ISO 8601 has 'T' separator
