"""Binary sensor entities for frigidaire integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import (
    CONF_CHECK_FILTER_SENSOR,
    DOMAIN,
)
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import filter_needs_attention, normalize_filter_state
from .helpers import suggest_area


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up frigidaire binary sensor entities from a config entry."""
    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]
    options: dict[str, dict[str, bool]] = entry.options

    if not options:
        return

    entities: list[BinarySensorEntity] = [
        FrigidaireCheckFilterSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if options.get(appliance.appliance_id, {}).get(CONF_CHECK_FILTER_SENSOR, False)
    ]

    async_add_entities(entities)


class FrigidaireCheckFilterSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], BinarySensorEntity):
    """Binary sensor that is ON when the filter needs attention."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_check_filter"
        self._attr_name = "Check Filter"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )

    @property
    def _details(self) -> dict:
        return self.coordinator.data or {}

    @property
    def available(self) -> bool:
        return (
            super().available and normalize_filter_state(self._details.get(frigidaire.Detail.FILTER_STATE)) is not None
        )

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        filter_state = normalize_filter_state(self._details.get(frigidaire.Detail.FILTER_STATE))
        if filter_state is None:
            return None
        return {"filter_state": filter_state}

    @property
    def is_on(self) -> bool | None:
        return filter_needs_attention(self._details.get(frigidaire.Detail.FILTER_STATE))
