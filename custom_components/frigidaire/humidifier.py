"""ClimateEntity for frigidaire integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.components.humidifier import HumidifierDeviceClass, HumidifierEntity
from homeassistant.components.humidifier.const import (
    MODE_AUTO,
    MODE_BOOST,
    MODE_NORMAL,
    MODE_SLEEP,
    HumidifierEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_platform
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import DOMAIN
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import bucket_is_full, filter_needs_attention, normalize_alerts
from .helpers import suggest_area

_LOGGER = logging.getLogger(__name__)


def _normalize_enum_value(value):
    """Normalize API values to uppercase for enum comparison."""
    if isinstance(value, str):
        return value.upper()
    return value


FAN_LOW = "low"
FAN_MEDIUM = "medium"
FAN_HIGH = "high"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up frigidaire from a config entry."""
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "set_fan_mode",
        {vol.Required("fan_mode"): cv.string},
        "set_fan_mode",
    )

    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]

    async_add_entities(
        FrigidaireDehumidifier(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if appliance.destination == frigidaire.Destination.DEHUMIDIFIER
    )


FRIGIDAIRE_TO_HA_MODE = {
    frigidaire.Mode.DRY: MODE_NORMAL,
    frigidaire.Mode.CONTINUOUS: MODE_BOOST,
    frigidaire.Mode.QUIET: MODE_SLEEP,
    frigidaire.Mode.AUTO: MODE_AUTO,
    frigidaire.Mode.SMART: MODE_AUTO,
}

HA_TO_FRIGIDAIRE_MODE = {
    MODE_NORMAL: frigidaire.Mode.DRY,
    MODE_BOOST: frigidaire.Mode.CONTINUOUS,
    MODE_SLEEP: frigidaire.Mode.QUIET,
    MODE_AUTO: frigidaire.Mode.AUTO,
}

FRIGIDAIRE_TO_HA_FAN_MODE = {
    frigidaire.FanSpeed.LOW: FAN_LOW,
    frigidaire.FanSpeed.MEDIUM: FAN_MEDIUM,
    frigidaire.FanSpeed.HIGH: FAN_HIGH,
}

HA_TO_FRIGIDAIRE_FAN_MODE = {v: k for k, v in FRIGIDAIRE_TO_HA_FAN_MODE.items()}


class FrigidaireDehumidifier(CoordinatorEntity[FrigidaireApplianceCoordinator], HumidifierEntity):
    """Representation of a Frigidaire dehumidifier."""

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None):
        """Build FrigidaireDehumidifier.

        coordinator: shared per-appliance coordinator that polls the frigidaire API
        """

        super().__init__(coordinator)
        self._client: frigidaire.Frigidaire = coordinator.client
        self._appliance: frigidaire.Appliance = coordinator.appliance

        # Entity Class Attributes
        self._attr_unique_id = self._appliance.appliance_id
        self._attr_name = self._appliance.nickname
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )
        self._attr_supported_features = HumidifierEntityFeature.MODES

        self._attr_device_class = HumidifierDeviceClass.DEHUMIDIFIER

        # self._attr_fan_modes = [
        #     FAN_LOW,
        #     FAN_HIGH,
        # ]

        self._attr_available_modes = [
            MODE_NORMAL,
            MODE_BOOST,
            MODE_AUTO,
            MODE_SLEEP,
        ]

    @property
    def _details(self) -> dict:
        return self.coordinator.data or {}

    @property
    def available(self) -> bool:
        # Prefer applianceState when present; fall back to a reported mode, since
        # some models omit applianceState from their API response.
        if not super().available:
            return False
        appliance_state = self._details.get(frigidaire.Detail.APPLIANCE_STATE)
        mode = self._details.get(frigidaire.Detail.MODE)
        return appliance_state is not None or mode is not None

    @property
    def is_on(self):
        return (
            _normalize_enum_value(self._details.get(frigidaire.Detail.APPLIANCE_STATE))
            == frigidaire.ApplianceState.RUNNING
        )

    @property
    def target_humidity(self):
        """Return the humidity we try to reach."""
        return self._details.get(frigidaire.Detail.TARGET_HUMIDITY)

    @property
    def mode(self):
        """Return current operation i.e. dry, continuous."""
        frigidaire_mode = _normalize_enum_value(self._details.get(frigidaire.Detail.MODE))

        if frigidaire_mode == frigidaire.Mode.OFF:
            return MODE_NORMAL

        if frigidaire_mode not in FRIGIDAIRE_TO_HA_MODE:
            _LOGGER.warning("Unsupported dehumidifier mode '%s' reported by device.", frigidaire_mode)
            return None

        return FRIGIDAIRE_TO_HA_MODE[frigidaire_mode]

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Add extra state attributes specific to Frigidaire dehumidifiers"""
        fan_speed = _normalize_enum_value(self._details.get(frigidaire.Detail.FAN_SPEED))

        attrib = {
            "current_humidity": self._details.get(frigidaire.Detail.SENSOR_HUMIDITY),
            "check_filter": filter_needs_attention(self._details.get(frigidaire.Detail.FILTER_STATE)) or False,
            "fan_mode": FRIGIDAIRE_TO_HA_FAN_MODE.get(fan_speed),
        }

        # The following attributes only exist on some models of dehumidifier
        alerts = normalize_alerts(self._details.get(frigidaire.Detail.ALERTS))
        if alerts is not None:
            attrib["active_alerts"] = alerts

        # Shared with the Bucket Status binary sensor; None (unreported) stays
        # False here to preserve the attribute's historical always-bool shape.
        attrib["bin_full"] = (
            bucket_is_full(
                alerts,
                self._details.get(frigidaire.Detail.WATER_BUCKET_LEVEL),
                self._details.get(frigidaire.Detail.WATER_TANK_FULL),
            )
            or False
        )

        return attrib

    @property
    def min_humidity(self):
        """Return the minimum humidity."""
        return 35

    @property
    def max_humidity(self):
        """Return the maximum humidity."""
        return 85

    def turn_on(self, **kwargs: Any) -> None:
        self._client.execute_action(self._appliance, frigidaire.Action.set_power(frigidaire.Power.ON))
        self.schedule_update_ha_state(force_refresh=True)

    def turn_off(self, **kwargs: Any) -> None:
        self._client.execute_action(self._appliance, frigidaire.Action.set_power(frigidaire.Power.OFF))
        self.schedule_update_ha_state(force_refresh=True)

    def set_humidity(self, humidity: int):
        """Set new target humidity."""
        if humidity is None:
            return
        # Only supports 5% steps
        humidity = 5 * round(humidity / 5)
        # We have to be in dry mode to set a target humidity
        self.set_mode(MODE_NORMAL)
        self._client.execute_action(self._appliance, frigidaire.Action.set_humidity(humidity))
        self.schedule_update_ha_state(force_refresh=True)

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        # Guard against unexpected fan modes
        if fan_mode not in HA_TO_FRIGIDAIRE_FAN_MODE:
            return

        action = frigidaire.Action.set_fan_speed(HA_TO_FRIGIDAIRE_FAN_MODE[fan_mode])
        self._client.execute_action(self._appliance, action)
        self.schedule_update_ha_state(force_refresh=True)

    def set_mode(self, mode):
        """Set new target operation mode."""

        # Guard against unexpected modes
        if mode not in HA_TO_FRIGIDAIRE_MODE:
            return

        # Turn on if not currently on.
        if _normalize_enum_value(self._details.get(frigidaire.Detail.APPLIANCE_STATE)) == frigidaire.ApplianceState.OFF:
            self.turn_on()

        self._client.execute_action(self._appliance, frigidaire.Action.set_mode(HA_TO_FRIGIDAIRE_MODE[mode]))
        self.schedule_update_ha_state(force_refresh=True)
