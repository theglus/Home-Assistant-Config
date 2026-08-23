"""Sensor entities for the frigidaire integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import CONF_FILTER_RUNTIME_SENSOR, DOMAIN
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import AIR_FILTER_LIFETIME_KEY, filter_runtime_seconds
from .helpers import suggest_area


def _normalize(value):
    if isinstance(value, str):
        return value.upper()
    return value


FRIGIDAIRE_TO_HA_UNIT = {
    frigidaire.Unit.FAHRENHEIT: UnitOfTemperature.FAHRENHEIT,
    frigidaire.Unit.CELSIUS: UnitOfTemperature.CELSIUS,
}


def _reports_temperature(details: dict) -> bool:
    """Return True if the appliance is reporting an ambient temperature.

    Only some dehumidifiers have a temperature sensor, so we key entity
    creation off whether the device actually reports one. Devices without it
    never get a temperature entity.
    """
    return (
        details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F) is not None
        or details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C) is not None
    )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up frigidaire sensor entities from a config entry."""
    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]
    options: dict[str, dict[str, bool]] = entry.options

    entities: list[SensorEntity] = [
        FrigidaireTemperatureSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if appliance.destination == frigidaire.Destination.DEHUMIDIFIER
        # Only dehumidifiers that actually report an ambient temperature get a
        # sensor; the coordinator's data is primed before platform setup, so
        # this reflects the device's real capabilities.
        and _reports_temperature(coordinators[appliance.appliance_id].data or {})
    ]
    entities += [
        FrigidaireFilterRuntimeSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if options.get(appliance.appliance_id, {}).get(CONF_FILTER_RUNTIME_SENSOR, False)
    ]

    async_add_entities(entities)


class FrigidaireTemperatureSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], SensorEntity):
    """Ambient temperature reported by a Frigidaire dehumidifier."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_temperature"
        self._attr_name = "Temperature"
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
    def native_unit_of_measurement(self) -> str:
        """Return the unit the device is reporting temperature in.

        Prefer the device's stated representation; if that's missing, infer it
        from whichever ambient value is present so the unit always matches
        native_value.
        """
        unit = FRIGIDAIRE_TO_HA_UNIT.get(_normalize(self._details.get(frigidaire.Detail.TEMPERATURE_REPRESENTATION)))
        if unit is not None:
            return unit
        if (
            self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F) is None
            and self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C) is not None
        ):
            return UnitOfTemperature.CELSIUS
        return UnitOfTemperature.FAHRENHEIT

    @property
    def native_value(self) -> float | None:
        """Return the current ambient temperature in native_unit_of_measurement."""
        if self.native_unit_of_measurement == UnitOfTemperature.CELSIUS:
            return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C)
        return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F)


class FrigidaireFilterRuntimeSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], SensorEntity):
    """Report cumulative air-filter runtime from the owning appliance entity."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:air-filter"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_filter_runtime"
        self._attr_name = "Filter Runtime"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )

    @property
    def _runtime_seconds(self) -> float | None:
        return filter_runtime_seconds((self.coordinator.data or {}).get(AIR_FILTER_LIFETIME_KEY))

    @property
    def available(self) -> bool:
        return super().available and self._runtime_seconds is not None

    @property
    def native_value(self) -> float | None:
        return self._runtime_seconds
