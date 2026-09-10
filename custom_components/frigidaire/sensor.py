"""Sensor entities for the frigidaire integration."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfDensity,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import CONF_FILTER_RUNTIME_SENSOR, DOMAIN
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import (
    AIR_FILTER_LIFETIME_KEY,
    filter_runtime_seconds,
    humidity_percent,
    link_quality,
    network_rssi,
    particulate_matter,
)
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


@dataclass(frozen=True)
class SensorDescription:
    """A sensor derived from a single reported detail.

    value_fn does the parsing and validation, so a detail the appliance reports as a
    placeholder or in an impossible range yields None and the sensor is never created.
    """

    key: str
    name: str
    detail: frigidaire.Detail
    value_fn: Callable[[Any], float | None]
    device_class: SensorDeviceClass
    native_unit: str
    state_class: SensorStateClass = SensorStateClass.MEASUREMENT
    entity_category: EntityCategory | None = None
    enabled_default: bool = True
    attributes_fn: Callable[[Any], Mapping[str, Any] | None] | None = None
    suggested_display_precision: int | None = None


def _link_quality_attributes(raw: Any) -> Mapping[str, Any] | None:
    indicator = link_quality(raw)
    return None if indicator is None else {"link_quality": indicator}


# Details the appliance already sends on every poll. Each entity is created only when its
# value_fn returns a value, so appliances without the hardware stay clean.
#
# Deliberately absent: Detail.PM10. On a Telica portable AC it alternates between a fixed
# placeholder (199) and a value identical to pm25, so it carries no information that pm25
# does not already provide and would publish a bogus reading half the time.
SENSOR_DESCRIPTIONS: tuple[SensorDescription, ...] = (
    SensorDescription(
        key="humidity",
        name="Humidity",
        detail=frigidaire.Detail.SENSOR_HUMIDITY,
        value_fn=humidity_percent,
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit=PERCENTAGE,
    ),
    SensorDescription(
        key="pm25",
        name="PM2.5",
        detail=frigidaire.Detail.PM25,
        value_fn=particulate_matter,
        device_class=SensorDeviceClass.PM25,
        native_unit=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
    ),
    SensorDescription(
        key="wifi_signal",
        name="Wi-Fi Signal",
        detail=frigidaire.Detail.NETWORK_INTERFACE,
        value_fn=network_rssi,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        # Useful when diagnosing a flaky appliance, noise the rest of the time.
        enabled_default=False,
        attributes_fn=_link_quality_attributes,
    ),
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
    # Reported-detail sensors apply to every appliance type. Creation is gated on the
    # appliance actually reporting a usable value, which the primed coordinator data
    # already tells us, so no extra API call is needed to detect capabilities.
    entities += [
        FrigidaireDetailSensor(
            coordinators[appliance.appliance_id], description, suggest_area(hass, appliance.nickname)
        )
        for appliance in appliances
        for description in SENSOR_DESCRIPTIONS
        if description.value_fn((coordinators[appliance.appliance_id].data or {}).get(description.detail)) is not None
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


class FrigidaireDetailSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], SensorEntity):
    """A sensor backed by a single reported detail, described by SENSOR_DESCRIPTIONS."""

    def __init__(
        self,
        coordinator: FrigidaireApplianceCoordinator,
        description: SensorDescription,
        suggested_area: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._desc = description
        self._attr_unique_id = f"{self._appliance.appliance_id}_{description.key}"
        self._attr_name = description.name
        self._attr_device_class = description.device_class
        self._attr_native_unit_of_measurement = description.native_unit
        self._attr_state_class = description.state_class
        self._attr_entity_category = description.entity_category
        self._attr_entity_registry_enabled_default = description.enabled_default
        self._attr_suggested_display_precision = description.suggested_display_precision
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )

    @property
    def _raw(self) -> Any:
        return (self.coordinator.data or {}).get(self._desc.detail)

    @property
    def available(self) -> bool:
        # An appliance can stop reporting a detail (or report a placeholder) while staying
        # online, so fall back to unavailable rather than holding a stale reading.
        return super().available and self._desc.value_fn(self._raw) is not None

    @property
    def native_value(self) -> float | None:
        return self._desc.value_fn(self._raw)

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        if self._desc.attributes_fn is None:
            return None
        return self._desc.attributes_fn(self._raw)
