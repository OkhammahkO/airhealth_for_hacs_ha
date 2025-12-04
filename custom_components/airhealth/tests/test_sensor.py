"""Tests for the sensor platform."""
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import DOMAIN


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
