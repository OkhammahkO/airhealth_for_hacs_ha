"""Base entity for AirHealth integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SAL_CODE, DOMAIN
from .coordinator import AirHealthDataUpdateCoordinator


class AirHealthEntity(CoordinatorEntity[AirHealthDataUpdateCoordinator]):
    """Base class for AirHealth entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AirHealthDataUpdateCoordinator) -> None:
        """Initialize AirHealth entity."""
        super().__init__(coordinator)

        sal_code = coordinator.config_entry.data[CONF_SAL_CODE]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=f"AirHealth (SAL {sal_code})",
            manufacturer="AirHealth Services",
            entry_type=DeviceEntryType.SERVICE,
        )
