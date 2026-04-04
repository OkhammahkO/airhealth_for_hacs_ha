"""Tests for the sensor platform."""
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import DOMAIN, get_level_icon


async def test_sensor_setup(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
) -> None:
    """Test the setup of the sensor platform."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # 3 endpoints × 3 days, but aq_woodsmoke creates 2 sensors/day → 3+3+6 = 12
    assert len(hass.states.async_all()) == 12

    # Check the state of a known sensor
    grass_pollen_sensor = hass.states.get("sensor.airhealth_grass_day0")
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
        # Verify SAL code is present
        assert "sal_code" in state.attributes
        assert state.attributes["sal_code"] == "12345"


async def test_sensor_summary_attributes(hass: HomeAssistant, mock_airhealth_api, mock_config_entry):
    """Test that sensors have natural language summary attributes."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Test grass pollen day0 has summary
    grass_day0 = hass.states.get("sensor.airhealth_grass_day0")
    if grass_day0:
        assert "summary" in grass_day0.attributes
        summary = grass_day0.attributes["summary"]
        assert isinstance(summary, str)
        assert "grass pollen is" in summary.lower()

    # Test grass pollen day1 has summary
    grass_day1 = hass.states.get("sensor.airhealth_grass_day1")
    if grass_day1:
        assert "summary" in grass_day1.attributes

    # Test grass pollen day2 does NOT have summary
    grass_day2 = hass.states.get("sensor.airhealth_grass_day2")
    if grass_day2:
        assert "summary" not in grass_day2.attributes

    # Test other allergens day0 has summary with breakdown
    allergen_day0 = hass.states.get("sensor.airhealth_other_allergens_day0")
    if allergen_day0:
        assert "summary" in allergen_day0.attributes
        summary = allergen_day0.attributes["summary"]
        assert isinstance(summary, str)
        assert "other allergens are" in summary.lower()

    # Test other allergens day1 has summary
    allergen_day1 = hass.states.get("sensor.airhealth_other_allergens_day1")
    if allergen_day1:
        assert "summary" in allergen_day1.attributes

    # Test other allergens day2 does NOT have summary
    allergen_day2 = hass.states.get("sensor.airhealth_other_allergens_day2")
    if allergen_day2:
        assert "summary" not in allergen_day2.attributes

    # Test air quality does NOT have summary
    aq_state = hass.states.get("sensor.airhealth_air_quality_day0")
    if aq_state:
        assert "summary" not in aq_state.attributes

    # Test woodsmoke does NOT have summary
    woodsmoke_state = hass.states.get("sensor.airhealth_woodsmoke_day0")
    if woodsmoke_state:
        assert "summary" not in woodsmoke_state.attributes


def test_summary_helper_functions():
    """Test the summary generation helper functions."""
    from custom_components.airhealth.const import (
        summarize_grass_pollen,
        summarize_allergen_breakdown,
    )

    # Test grass pollen summaries
    assert summarize_grass_pollen("Low") == "Grass pollen is low"
    assert summarize_grass_pollen("Moderate") == "Grass pollen is moderate"
    assert summarize_grass_pollen("High") == "Grass pollen is high"
    assert summarize_grass_pollen("Extreme") == "Grass pollen is extreme"
    assert summarize_grass_pollen("None") == "Grass pollen is none"
    assert summarize_grass_pollen(None) == "Grass pollen is none"

    # Test allergen summaries - None/Low (no sub-items)
    assert summarize_allergen_breakdown("None", []) == "Other allergens are none"
    assert summarize_allergen_breakdown("Low", [{"name": "Birch", "level": "Low"}]) == "Other allergens are low"

    # Test allergen summaries - Moderate (only shows moderates)
    allergens = [
        {"name": "Plantain", "level": "Moderate"},
        {"name": "Birch", "level": "Low"},
    ]
    summary = summarize_allergen_breakdown("Moderate", allergens)
    assert summary == "Other allergens are moderate. Plantain is moderate"
    assert "birch" not in summary.lower()  # Low allergen not shown

    # Test allergen summaries - High (only shows highs)
    allergens = [
        {"name": "Birch", "level": "High"},
        {"name": "Plantain", "level": "High"},
        {"name": "Olive", "level": "Moderate"},
    ]
    summary = summarize_allergen_breakdown("High", allergens)
    assert "birch and plantain are high" in summary.lower()
    assert "olive" not in summary.lower()  # Moderate allergen not shown

    # Test allergen summaries - Extreme (shows extremes and highs)
    allergens = [
        {"name": "Birch", "level": "Extreme"},
        {"name": "Olive", "level": "Extreme"},
        {"name": "Plantain", "level": "High"},
        {"name": "Cypress", "level": "High"},
        {"name": "Eucalyptus", "level": "Moderate"},
    ]
    summary = summarize_allergen_breakdown("Extreme", allergens)
    assert "birch and olive are extreme" in summary.lower()
    assert "plantain and cypress are high" in summary.lower()
    assert "eucalyptus" not in summary.lower()  # Moderate allergen not shown
