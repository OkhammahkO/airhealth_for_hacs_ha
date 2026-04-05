"""Tests for the sensor platform."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import (
    DOMAIN,
    ENDPOINT_AQ_WOODSMOKE,
    ENDPOINT_GRASS_POLLEN,
    ENDPOINT_OTHER_ALLERGENS,
    get_level_icon,
)


def _entity_id(
    hass: HomeAssistant,
    entry: MockConfigEntry,
    endpoint: str,
    sensor_key: str,
    day: int,
) -> str | None:
    """Look up entity_id via the entity registry using the sensor's unique_id."""
    ent_reg = er.async_get(hass)
    unique_id = f"{entry.entry_id}_{endpoint}_{sensor_key}_day{day}"
    return ent_reg.async_get_entity_id("sensor", DOMAIN, unique_id)


async def test_sensor_setup(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
) -> None:
    """Test the setup of the sensor platform."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # 3 endpoints × 3 days, but aq_woodsmoke creates 2 sensors/day → 3+3+6 = 12
    assert len(hass.states.async_all("sensor")) == 12

    # Check the state of a known sensor
    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_GRASS_POLLEN, "grass_level", 0
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "Low"


async def test_sensor_level_icon_attribute(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
):
    """Test that sensors have level_icon attribute."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_GRASS_POLLEN, "grass_level", 0
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert "level_icon" in state.attributes
    assert state.attributes["level_icon"] == get_level_icon(state.state)


async def test_allergen_breakdown_icons(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
):
    """Test that allergen breakdown includes level_icon for each allergen."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_OTHER_ALLERGENS, "overall_level", 0
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert "allergens" in state.attributes
    for allergen in state.attributes["allergens"]:
        assert "level_icon" in allergen
        level = allergen.get("level")
        if level:
            assert allergen["level_icon"] == get_level_icon(level)


def test_get_level_icon():
    """Test the get_level_icon helper function."""
    assert get_level_icon("Low") == "🟢"
    assert get_level_icon("None") == "🟢"
    assert get_level_icon("Moderate") == "🟡"
    assert get_level_icon("High") == "🟠"
    assert get_level_icon("Extreme") == "🔴"
    assert get_level_icon("Unknown") == "⚪"
    assert get_level_icon(None) == "⚪"


async def test_sensor_metadata_attributes(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
):
    """Test that sensors have metadata attributes."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_GRASS_POLLEN, "grass_level", 0
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert "last_successful_update" in state.attributes
    assert "api_status" in state.attributes
    assert state.attributes["api_status"] in [
        "ok",
        "error",
        "quota_exceeded",
        "unavailable",
    ]
    timestamp = state.attributes.get("last_successful_update")
    assert isinstance(timestamp, str)
    assert "T" in timestamp
    assert "sal_code" in state.attributes
    assert state.attributes["sal_code"] == "12345"


async def test_sensor_summary_attributes(
    hass: HomeAssistant, mock_airhealth_api, mock_config_entry: MockConfigEntry
):
    """Test that sensors have natural language summary attributes."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Grass pollen day0 and day1 have summaries; day2 does not
    for day in (0, 1):
        entity_id = _entity_id(
            hass, mock_config_entry, ENDPOINT_GRASS_POLLEN, "grass_level", day
        )
        assert entity_id is not None
        state = hass.states.get(entity_id)
        assert state is not None
        assert "summary" in state.attributes
        assert "grass pollen is" in state.attributes["summary"].lower()

    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_GRASS_POLLEN, "grass_level", 2
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert "summary" not in state.attributes

    # Other allergens day0 and day1 have summaries; day2 does not
    for day in (0, 1):
        entity_id = _entity_id(
            hass, mock_config_entry, ENDPOINT_OTHER_ALLERGENS, "overall_level", day
        )
        assert entity_id is not None
        state = hass.states.get(entity_id)
        assert state is not None
        assert "summary" in state.attributes
        assert "other allergens are" in state.attributes["summary"].lower()

    entity_id = _entity_id(
        hass, mock_config_entry, ENDPOINT_OTHER_ALLERGENS, "overall_level", 2
    )
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    assert "summary" not in state.attributes

    # AQ and woodsmoke sensors never have summaries
    for sensor_key in ("aq_level", "woodsmoke_level"):
        entity_id = _entity_id(
            hass, mock_config_entry, ENDPOINT_AQ_WOODSMOKE, sensor_key, 0
        )
        assert entity_id is not None
        state = hass.states.get(entity_id)
        assert state is not None
        assert "summary" not in state.attributes


def test_summary_helper_functions():
    """Test the summary generation helper functions."""
    from custom_components.airhealth.const import (
        summarize_allergen_breakdown,
        summarize_grass_pollen,
    )

    assert summarize_grass_pollen("Low") == "Grass pollen is low"
    assert summarize_grass_pollen("Moderate") == "Grass pollen is moderate"
    assert summarize_grass_pollen("High") == "Grass pollen is high"
    assert summarize_grass_pollen("Extreme") == "Grass pollen is extreme"
    assert summarize_grass_pollen("None") == "Grass pollen is none"
    assert summarize_grass_pollen(None) == "Grass pollen is none"

    assert summarize_allergen_breakdown("None", []) == "Other allergens are none"
    assert (
        summarize_allergen_breakdown("Low", [{"name": "Birch", "level": "Low"}])
        == "Other allergens are low"
    )

    allergens = [
        {"name": "Plantain", "level": "Moderate"},
        {"name": "Birch", "level": "Low"},
    ]
    summary = summarize_allergen_breakdown("Moderate", allergens)
    assert summary == "Other allergens are moderate. Plantain is moderate"
    assert "birch" not in summary.lower()

    allergens = [
        {"name": "Birch", "level": "High"},
        {"name": "Plantain", "level": "High"},
        {"name": "Olive", "level": "Moderate"},
    ]
    summary = summarize_allergen_breakdown("High", allergens)
    assert "birch and plantain are high" in summary.lower()
    assert "olive" not in summary.lower()

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
    assert "eucalyptus" not in summary.lower()
