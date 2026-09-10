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
    CONF_BUCKET_STATUS_SENSOR,
    CONF_CHECK_FILTER_SENSOR,
    CONF_COMPRESSOR_ESTIMATE,
    DOMAIN,
)
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import bucket_is_full, filter_needs_attention, normalize_alerts, normalize_filter_state
from .helpers import suggest_area


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up frigidaire binary sensor entities from a config entry."""
    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]
    options: dict[str, dict[str, bool]] = entry.options

    # Connectivity is meaningful for every appliance and needs no per-device opt-in, so
    # unlike the check-filter sensor it has no key in const.BINARY_SENSOR_OPTIONS — and it
    # is created even when the entry has no options set at all.
    entities: list[BinarySensorEntity] = [
        FrigidaireConnectivitySensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if coordinators[appliance.appliance_id].connection_state is not None
    ]

    entities += [
        FrigidaireCheckFilterSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if options.get(appliance.appliance_id, {}).get(CONF_CHECK_FILTER_SENSOR, False)
    ]
    entities += [
        FrigidaireBucketStatusSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        # Only dehumidifiers have a water bucket.
        if appliance.destination == frigidaire.Destination.DEHUMIDIFIER
        and options.get(appliance.appliance_id, {}).get(CONF_BUCKET_STATUS_SENSOR, False)
    ]
    entities += [
        FrigidaireCompressorEstimateSensor(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if appliance.destination == frigidaire.Destination.AIR_CONDITIONER
        and options.get(appliance.appliance_id, {}).get(CONF_COMPRESSOR_ESTIMATE, False)
    ]

    async_add_entities(entities)


class FrigidaireConnectivitySensor(CoordinatorEntity[FrigidaireApplianceCoordinator], BinarySensorEntity):
    """Binary sensor that is ON while the cloud reports the appliance as connected.

    This distinguishes a genuinely offline appliance from one whose reported values have
    simply gone stale — the rest of the integration cannot tell the difference, because a
    disconnected appliance keeps returning its last-known reported properties.
    """

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_connectivity"
        self._attr_name = "Connectivity"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )

    @property
    def available(self) -> bool:
        # Like every other entity, go unavailable when the poll itself fails: a cached
        # "connected" during an API outage would be misleading.
        return super().available and self.coordinator.is_connected is not None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        state = self.coordinator.connection_state
        return None if state is None else {"connection_state": state}

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.is_connected


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


class FrigidaireBucketStatusSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], BinarySensorEntity):
    """Binary sensor that is ON when the dehumidifier's water bucket is full.

    Displayed states are "Full" (on) and "Empty" (off) via the bucket_status
    translation key; no device_class is set so the custom states render instead
    of a device-class pair.
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_translation_key = "bucket_status"

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_bucket_status"
        self._attr_name = "Bucket Status"
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
    def _bucket_full(self) -> bool | None:
        """None when this model reports no bucket signal at all."""
        return bucket_is_full(
            normalize_alerts(self._details.get(frigidaire.Detail.ALERTS)),
            self._details.get(frigidaire.Detail.WATER_BUCKET_LEVEL),
            self._details.get(frigidaire.Detail.WATER_TANK_FULL),
        )

    @property
    def available(self) -> bool:
        # Mirror the capability gating used elsewhere: models that never report
        # a bucket signal show as unavailable rather than a misleading "Empty".
        return super().available and self._bucket_full is not None

    @property
    def is_on(self) -> bool | None:
        return self._bucket_full

    @property
    def icon(self) -> str:
        return "mdi:water-alert" if self.is_on else "mdi:cup-water"


class FrigidaireCompressorEstimateSensor(CoordinatorEntity[FrigidaireApplianceCoordinator], BinarySensorEntity):
    """Expose the coordinator's opt-in compressor estimate."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None) -> None:
        super().__init__(coordinator)
        self._appliance = coordinator.appliance
        self._attr_unique_id = f"{self._appliance.appliance_id}_compressor"
        self._attr_name = "Compressor Estimate"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.compressor_running is not None

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.compressor_running
