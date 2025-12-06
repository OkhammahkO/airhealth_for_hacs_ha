"""Platform for sensor integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ENDPOINT_AQ_WOODSMOKE,
    ENDPOINT_GRASS_POLLEN,
    ENDPOINT_OTHER_ALLERGENS,
    get_level_icon,
)
from .coordinator import AirHealthConfigEntry
from .entity import AirHealthEntity

PARALLEL_UPDATES = 0


class AirHealthSensor(AirHealthEntity, SensorEntity):
    """Representation of an AirHealth sensor."""

    def __init__(
        self,
        coordinator,
        endpoint_key: str,
        sensor_key: str,
        day_idx: int,
        icon: str,
        entity_id_suffix: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._endpoint_key = endpoint_key
        self._sensor_key = sensor_key
        self._day_idx = day_idx

        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{endpoint_key}_{sensor_key}_day{day_idx}"
        )
        self._attr_translation_key = f"{sensor_key}_day{day_idx}"
        self._attr_icon = icon
        self._attr_name = name
        # Suggest entity_id for cleaner IDs
        self.entity_id = f"sensor.airhealth_{entity_id_suffix}_day{day_idx}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if (
            not self.coordinator.data
            or self._endpoint_key not in self.coordinator.data
        ):
            return None

        try:
            forecast = self.coordinator.data[self._endpoint_key]["forecast"]
            if self._day_idx < len(forecast):
                return forecast[self._day_idx].get(self._sensor_key)
        except (KeyError, IndexError, TypeError):
            return None

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if (
            not self.coordinator.data
            or self._endpoint_key not in self.coordinator.data
        ):
            return {}

        try:
            forecast = self.coordinator.data[self._endpoint_key]["forecast"]
            if self._day_idx < len(forecast):
                day_data = forecast[self._day_idx]
                attributes = {"date": day_data.get("date")}

                # Add level icon for the main sensor value
                level = self.native_value
                if level:
                    attributes["level_icon"] = get_level_icon(str(level))

                # Add endpoint-specific attributes
                if self._endpoint_key == ENDPOINT_OTHER_ALLERGENS:
                    # Include full allergen breakdown with icons
                    allergens = day_data.get("allergens")
                    if allergens:
                        # Add level_icon to each allergen
                        allergens_with_icons = []
                        for allergen in allergens:
                            allergen_copy = allergen.copy()
                            allergen_level = allergen.get("level")
                            if allergen_level:
                                allergen_copy["level_icon"] = get_level_icon(allergen_level)
                            allergens_with_icons.append(allergen_copy)
                        attributes["allergens"] = allergens_with_icons
                elif self._endpoint_key == ENDPOINT_AQ_WOODSMOKE:
                    if self._sensor_key == "aq_level":
                        # For AQ sensor, include woodsmoke and supporting data
                        woodsmoke_level = day_data.get("woodsmoke_level")
                        attributes["woodsmoke_level"] = woodsmoke_level
                        if woodsmoke_level:
                            attributes["woodsmoke_icon"] = get_level_icon(woodsmoke_level)
                        attributes["supporting_data"] = day_data.get("supporting_data")
                    elif self._sensor_key == "woodsmoke_level":
                        # For woodsmoke sensor, include supporting data
                        attributes["supporting_data"] = day_data.get("supporting_data")

                return attributes
        except (KeyError, IndexError, TypeError):
            return {}

        return {}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AirHealthConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data

    if not coordinator.data:
        return

    sensors = []

    # Day name helper
    day_names = ["today", "tomorrow", "in 2 days"]

    # Grass pollen sensors
    if ENDPOINT_GRASS_POLLEN in coordinator.data:
        forecast = coordinator.data[ENDPOINT_GRASS_POLLEN].get("forecast", [])
        for day_idx in range(len(forecast)):
            sensors.append(
                AirHealthSensor(
                    coordinator,
                    ENDPOINT_GRASS_POLLEN,
                    "grass_level",
                    day_idx,
                    "mdi:grass",
                    "grass",
                    f"Grass pollen {day_names[day_idx]}",
                )
            )

    # Other allergens sensors
    if ENDPOINT_OTHER_ALLERGENS in coordinator.data:
        forecast = coordinator.data[ENDPOINT_OTHER_ALLERGENS].get("forecast", [])
        for day_idx in range(len(forecast)):
            sensors.append(
                AirHealthSensor(
                    coordinator,
                    ENDPOINT_OTHER_ALLERGENS,
                    "overall_level",
                    day_idx,
                    "mdi:flower-pollen",
                    "other_allergens",
                    f"Other allergens {day_names[day_idx]}",
                )
            )

    # AQ & Woodsmoke sensors
    if ENDPOINT_AQ_WOODSMOKE in coordinator.data:
        forecast = coordinator.data[ENDPOINT_AQ_WOODSMOKE].get("forecast", [])
        for day_idx in range(len(forecast)):
            sensors.extend(
                [
                    AirHealthSensor(
                        coordinator,
                        ENDPOINT_AQ_WOODSMOKE,
                        "aq_level",
                        day_idx,
                        "mdi:air-filter",
                        "air_quality",
                        f"Air quality {day_names[day_idx]}",
                    ),
                    AirHealthSensor(
                        coordinator,
                        ENDPOINT_AQ_WOODSMOKE,
                        "woodsmoke_level",
                        day_idx,
                        "mdi:smoke",
                        "woodsmoke",
                        f"Woodsmoke {day_names[day_idx]}",
                    ),
                ]
            )

    async_add_entities(sensors)
