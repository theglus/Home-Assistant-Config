"""ClimateEntity for frigidaire integration."""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from typing import Any

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    PRESET_NONE,
    PRESET_SLEEP,
    SWING_OFF,
    SWING_VERTICAL,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import DOMAIN
from .coordinator import FrigidaireApplianceCoordinator
from .diagnostics import filter_needs_attention, normalize_alerts
from .helpers import suggest_area

_LOGGER = logging.getLogger(__name__)


def _normalize_enum_value(value):
    """Normalize API values to uppercase for enum comparison."""
    if isinstance(value, str):
        return value.upper()
    return value


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up frigidaire from a config entry."""
    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]

    async_add_entities(
        FrigidaireClimate(coordinators[appliance.appliance_id], suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if appliance.destination == frigidaire.Destination.AIR_CONDITIONER
    )


FRIGIDAIRE_TO_HA_UNIT = {
    frigidaire.Unit.FAHRENHEIT: UnitOfTemperature.FAHRENHEIT,
    frigidaire.Unit.CELSIUS: UnitOfTemperature.CELSIUS,
}

FRIGIDAIRE_TO_HA_MODE = {
    frigidaire.Mode.OFF: HVACMode.OFF,
    frigidaire.Mode.COOL: HVACMode.COOL,
    frigidaire.Mode.FAN: HVACMode.FAN_ONLY,
    frigidaire.Mode.ECO: HVACMode.AUTO,
    frigidaire.Mode.AUTO: HVACMode.AUTO,
    frigidaire.Mode.DRY: HVACMode.DRY,
}

# Detail.MODE_STATE is the mode the appliance reports it is actually running, as opposed to
# Detail.MODE which is what was requested. Only the concrete running modes are mapped:
# anything else (ECO, AUTO, SMART) is a setting rather than an activity and falls through to
# the mode-derived fallback in hvac_action.
FRIGIDAIRE_MODE_STATE_TO_HA_ACTION = {
    frigidaire.Mode.COOL: HVACAction.COOLING,
    frigidaire.Mode.FAN: HVACAction.FAN,
    frigidaire.Mode.DRY: HVACAction.DRYING,
}

FRIGIDAIRE_TO_HA_FAN_SPEED = {
    frigidaire.FanSpeed.AUTO: FAN_AUTO,
    frigidaire.FanSpeed.LOW: FAN_LOW,
    frigidaire.FanSpeed.MEDIUM: FAN_MEDIUM,
    frigidaire.FanSpeed.HIGH: FAN_HIGH,
}

HA_TO_FRIGIDAIRE_UNIT = {
    UnitOfTemperature.FAHRENHEIT: frigidaire.Unit.FAHRENHEIT,
    UnitOfTemperature.CELSIUS: frigidaire.Unit.CELSIUS,
}

HA_TO_FRIGIDAIRE_FAN_MODE = {
    FAN_AUTO: frigidaire.FanSpeed.AUTO,
    FAN_LOW: frigidaire.FanSpeed.LOW,
    FAN_MEDIUM: frigidaire.FanSpeed.MEDIUM,
    FAN_HIGH: frigidaire.FanSpeed.HIGH,
}

# frigidaire.Mode.AUTO is a dehumidifier-only value (see frigidaire.Mode); this
# platform only ever handles Destination.AIR_CONDITIONER appliances (see
# async_setup_entry below), whose energy-saving mode is Mode.ECO. Sending
# Mode.AUTO to an AC unit is silently ignored, so HVACMode.AUTO must map to
# Mode.ECO here to round-trip with FRIGIDAIRE_TO_HA_MODE's ECO -> AUTO mapping.
HA_TO_FRIGIDAIRE_HVAC_MODE = {
    HVACMode.AUTO: frigidaire.Mode.ECO,
    HVACMode.FAN_ONLY: frigidaire.Mode.FAN,
    HVACMode.COOL: frigidaire.Mode.COOL,
    HVACMode.OFF: frigidaire.Mode.OFF,
    HVACMode.DRY: frigidaire.Mode.DRY,
}

FRIGIDAIRE_TO_HA_SWING = {
    frigidaire.VerticalSwing.ON: SWING_VERTICAL,
    frigidaire.VerticalSwing.OFF: SWING_OFF,
}

HA_TO_FRIGIDAIRE_SWING = {
    SWING_VERTICAL: frigidaire.VerticalSwing.ON,
    SWING_OFF: frigidaire.VerticalSwing.OFF,
}

HA_TO_FRIGIDAIRE_PRESET = {
    PRESET_SLEEP: frigidaire.SleepMode.ON,
    PRESET_NONE: frigidaire.SleepMode.OFF,
}

OPTIMISTIC_WINDOW = 5  # seconds


class FrigidaireClimate(CoordinatorEntity[FrigidaireApplianceCoordinator], ClimateEntity):
    """Representation of a Frigidaire appliance."""

    def __init__(self, coordinator: FrigidaireApplianceCoordinator, suggested_area: str | None = None):
        """Build FrigidaireClimate.

        coordinator: shared per-appliance coordinator that polls the frigidaire API
        """

        super().__init__(coordinator)
        self._client: frigidaire.Frigidaire = coordinator.client
        self._appliance: frigidaire.Appliance = coordinator.appliance

        # Optimistic state — holds values for OPTIMISTIC_WINDOW seconds after a command
        self._optimistic_until: float = 0
        self._optimistic_temperature: float | None = None
        self._optimistic_hvac_mode: str | None = None
        self._optimistic_fan_mode: str | None = None
        self._optimistic_preset_mode: str | None = None
        self._optimistic_swing_mode: str | None = None

        # Entity Class Attributes
        self._attr_unique_id = self._appliance.appliance_id
        self._attr_name = self._appliance.nickname
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._appliance.appliance_id)},
            name=self._appliance.nickname,
            manufacturer="Frigidaire",
            suggested_area=suggested_area,
        )
        # Base feature set. SWING_MODE is added dynamically by _update_swing_support()
        # only when the device actually reports a VERTICAL_SWING detail — some models
        # (e.g. FHWW144TF1) have no motorized louver and don't support it.
        self._base_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )
        self._attr_supported_features = self._base_supported_features
        self._attr_preset_modes = [PRESET_NONE, PRESET_SLEEP]
        # Populated by _update_swing_support() once swing support is detected.
        self._attr_swing_modes = None
        self._attr_target_temperature_step = 1

        self._attr_fan_modes = [
            FAN_AUTO,
            FAN_LOW,
            FAN_MEDIUM,
            FAN_HIGH,
        ]

        self._attr_hvac_modes = [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.AUTO,
            HVACMode.FAN_ONLY,
            HVACMode.DRY,
        ]

        # coordinator.data is already populated at this point (async_setup_entry
        # awaits the first refresh before entities are created), so detect swing
        # support up front rather than waiting for the first coordinator update.
        self._update_swing_support()

    @property
    def _details(self) -> dict:
        return self.coordinator.data or {}

    def _update_swing_support(self) -> None:
        """Advertise SWING_MODE only when the device reports a VERTICAL_SWING detail.

        Models without a motorized louver (e.g. FHWW144TF1) omit it, so we must
        not advertise a control that does nothing on those units.
        """
        if self._details.get(frigidaire.Detail.VERTICAL_SWING) is not None:
            self._attr_supported_features = self._base_supported_features | ClimateEntityFeature.SWING_MODE
            self._attr_swing_modes = [SWING_OFF, SWING_VERTICAL]
        else:
            self._attr_supported_features = self._base_supported_features
            self._attr_swing_modes = None

    @property
    def available(self) -> bool:
        # Prefer applianceState when present; fall back to a reported mode, since
        # some portable AC models (e.g. FHPW-series) omit applianceState from
        # their API response.
        if not super().available:
            return False
        appliance_state = self._details.get(frigidaire.Detail.APPLIANCE_STATE)
        mode = self._details.get(frigidaire.Detail.MODE)
        return appliance_state is not None or mode is not None

    def _set_optimistic_window(self) -> None:
        self._optimistic_until = time.monotonic() + OPTIMISTIC_WINDOW

    def _is_optimistic(self) -> bool:
        return time.monotonic() < self._optimistic_until

    def _clear_optimistic(self) -> None:
        self._optimistic_temperature = None
        self._optimistic_hvac_mode = None
        self._optimistic_fan_mode = None
        self._optimistic_preset_mode = None
        self._optimistic_swing_mode = None

    @property
    def reported_fan_speed(self) -> str | None:
        """Return the appliance's reported fan-speed state.

        This can resolve an AUTO setting to a concrete level, but it may retain
        the last value while the appliance is off and is not running telemetry.
        """
        return self.coordinator.reported_fan_speed

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        unit = _normalize_enum_value(self._details.get(frigidaire.Detail.TEMPERATURE_REPRESENTATION))

        return FRIGIDAIRE_TO_HA_UNIT[unit]

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self._is_optimistic() and self._optimistic_temperature is not None:
            return self._optimistic_temperature
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return self._details.get(frigidaire.Detail.TARGET_TEMPERATURE_F)
        else:
            return self._details.get(frigidaire.Detail.TARGET_TEMPERATURE_C)

    @property
    def hvac_mode(self):
        """Return current operation i.e. heat, cool, idle."""
        if self._is_optimistic() and self._optimistic_hvac_mode is not None:
            return self._optimistic_hvac_mode
        appliance_state = _normalize_enum_value(self._details.get(frigidaire.Detail.APPLIANCE_STATE))
        if appliance_state == frigidaire.ApplianceState.OFF:
            return HVACMode.OFF
        frigidaire_mode = _normalize_enum_value(self._details.get(frigidaire.Detail.MODE))

        if frigidaire_mode not in FRIGIDAIRE_TO_HA_MODE:
            _LOGGER.warning("Unsupported HVAC mode '%s' reported by device.", frigidaire_mode)
            return None

        return FRIGIDAIRE_TO_HA_MODE[frigidaire_mode]

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action."""
        mode = self.hvac_mode
        if mode == HVACMode.OFF:
            return HVACAction.OFF
        appliance_state = _normalize_enum_value(self._details.get(frigidaire.Detail.APPLIANCE_STATE))
        if appliance_state != frigidaire.ApplianceState.RUNNING:
            return HVACAction.IDLE

        # Prefer the appliance's reported modeState over the requested mode. In ECO/AUTO the
        # requested mode says nothing about what the unit is doing right now, so this is the
        # only way to distinguish actually cooling from just running the fan. Note that
        # hvac_mode deliberately stays on the requested mode — that is the user's selection
        # and must not flap as the compressor cycles.
        mode_state = FRIGIDAIRE_MODE_STATE_TO_HA_ACTION.get(
            _normalize_enum_value(self._details.get(frigidaire.Detail.MODE_STATE))
        )
        if mode_state is not None:
            return mode_state

        # No modeState reported — fall back to the action implied by the active mode rather
        # than collapsing everything to COOLING.
        if mode == HVACMode.FAN_ONLY:
            return HVACAction.FAN
        # The opt-in temperature-based estimate only refines hvac_action on appliances
        # that do not report modeState; real telemetry above always wins.
        if self.coordinator.compressor_estimation_enabled and self.coordinator.compressor_running is False:
            return HVACAction.IDLE
        if mode == HVACMode.DRY:
            return HVACAction.DRYING
        return HVACAction.COOLING

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F)
        else:
            return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C)

    @property
    def fan_mode(self):
        """Return the fan setting."""
        if self._is_optimistic() and self._optimistic_fan_mode is not None:
            return self._optimistic_fan_mode
        fan_speed = _normalize_enum_value(self._details.get(frigidaire.Detail.FAN_SPEED))

        if not fan_speed:
            return None

        return FRIGIDAIRE_TO_HA_FAN_SPEED.get(fan_speed)

    @property
    def swing_mode(self) -> str | None:
        """Return the swing setting."""
        if not self._attr_supported_features & ClimateEntityFeature.SWING_MODE:
            return None
        if self._is_optimistic() and self._optimistic_swing_mode is not None:
            return self._optimistic_swing_mode
        swing = _normalize_enum_value(self._details.get(frigidaire.Detail.VERTICAL_SWING))
        if swing == frigidaire.VerticalSwing.ON:
            return SWING_VERTICAL
        return SWING_OFF

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return 60

        return 16

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return 90

        return 32

    @property
    def preset_mode(self) -> str | None:
        if self._is_optimistic() and self._optimistic_preset_mode is not None:
            return self._optimistic_preset_mode
        sleep = _normalize_enum_value(self._details.get(frigidaire.Detail.SLEEP_MODE))
        if sleep == frigidaire.SleepMode.ON:
            return PRESET_SLEEP
        return PRESET_NONE

    def set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode not in HA_TO_FRIGIDAIRE_PRESET:
            return
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_sleep_mode(HA_TO_FRIGIDAIRE_PRESET[preset_mode])
        )
        self._optimistic_preset_mode = preset_mode
        self._set_optimistic_window()
        self.schedule_update_ha_state(force_refresh=True)

    def set_swing_mode(self, swing_mode: str) -> None:
        if not self._attr_supported_features & ClimateEntityFeature.SWING_MODE:
            return
        if swing_mode not in HA_TO_FRIGIDAIRE_SWING:
            return
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_vertical_swing(HA_TO_FRIGIDAIRE_SWING[swing_mode])
        )
        self._optimistic_swing_mode = swing_mode
        self._set_optimistic_window()
        self.schedule_update_ha_state(force_refresh=True)

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        attributes: dict[str, Any] = {
            "check_filter": filter_needs_attention(self._details.get(frigidaire.Detail.FILTER_STATE)) or False,
        }
        reported_fan_speed = self.reported_fan_speed
        if reported_fan_speed is not None:
            attributes["reported_fan_speed"] = reported_fan_speed
            # Keep the original attribute for existing dashboards and templates.
            attributes["current_fan_speed"] = reported_fan_speed
        active_alerts = normalize_alerts(self._details.get(frigidaire.Detail.ALERTS))
        if active_alerts is not None:
            attributes["active_alerts"] = active_alerts
        return attributes

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        temperature = int(temperature)
        temperature_unit = HA_TO_FRIGIDAIRE_UNIT[self.temperature_unit]

        _LOGGER.debug("Setting temperature to %s %s", temperature, self.temperature_unit)
        self._client.execute_action(self._appliance, frigidaire.Action.set_temperature(temperature, temperature_unit))
        self._optimistic_temperature = float(temperature)
        self._set_optimistic_window()
        self.schedule_update_ha_state(force_refresh=True)

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        if fan_mode not in HA_TO_FRIGIDAIRE_FAN_MODE:
            return
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_fan_speed(HA_TO_FRIGIDAIRE_FAN_MODE[fan_mode])
        )
        self._optimistic_fan_mode = fan_mode
        self._set_optimistic_window()
        self.schedule_update_ha_state(force_refresh=True)

    def set_hvac_mode(self, hvac_mode):
        """Set new target operation mode."""
        _LOGGER.debug("Setting HVAC mode to %s", hvac_mode)

        if hvac_mode == HVACMode.OFF:
            self._client.execute_action(self._appliance, frigidaire.Action.set_mode(frigidaire.Mode.OFF))
        else:
            if hvac_mode not in HA_TO_FRIGIDAIRE_HVAC_MODE:
                return
            appliance_state = _normalize_enum_value(self._details.get(frigidaire.Detail.APPLIANCE_STATE))
            frigidaire_mode = _normalize_enum_value(self._details.get(frigidaire.Detail.MODE))
            was_off = appliance_state == frigidaire.ApplianceState.OFF or frigidaire_mode == frigidaire.Mode.OFF
            _LOGGER.debug(
                "Turn-on requested; cloud reports appliance_state=%s mode=%s", appliance_state, frigidaire_mode
            )
            # Always send power-on. The cloud reports the DESIRED state, not the hardware
            # state: after a single failed turn-on it keeps reporting RUNNING, so gating
            # set_power on it skips the power command on every retry and the unit never
            # starts. Power is a set (ON/OFF), not a toggle, so this is harmless on a unit
            # that really is running.
            self._client.execute_action(self._appliance, frigidaire.Action.set_power(frigidaire.Power.ON))
            self._client.execute_action(
                self._appliance, frigidaire.Action.set_mode(HA_TO_FRIGIDAIRE_HVAC_MODE[hvac_mode])
            )
            if was_off:
                # The appliance forgets its setpoint when powered on, and engaging the mode
                # restores that default, so the remembered setpoint must be re-sent last.
                # On the stale-RUNNING retry path the cloud still says RUNNING, so was_off is
                # False and the setpoint is deliberately not re-sent; the next poll picks up the
                # appliance's default instead, which is the trade-off for not doubling write
                # traffic on every mode change.
                current_temp = self.target_temperature
                if current_temp is not None:
                    self._client.execute_action(
                        self._appliance,
                        frigidaire.Action.set_temperature(
                            int(current_temp), HA_TO_FRIGIDAIRE_UNIT[self.temperature_unit]
                        ),
                    )

        self._optimistic_hvac_mode = hvac_mode
        self._set_optimistic_window()
        self.schedule_update_ha_state(force_refresh=True)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Drop stale optimistic values once the command window has elapsed."""
        if not self._is_optimistic():
            self._clear_optimistic()
        self._update_swing_support()
        super()._handle_coordinator_update()
