"""Number entities for Frigidaire AC timers (ON/OFF)."""

from __future__ import annotations

import time

from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import frigidaire

from .const import DOMAIN
from .coordinator import FrigidaireApplianceCoordinator
from .helpers import suggest_area


def _normalize(value):
    if isinstance(value, str):
        return value.upper()
    return value


STEP_SECONDS = 1800  # 30 minutes
MAX_SECONDS = 86400  # 24 hours
OPTIMISTIC_WINDOW = 5  # seconds to hold optimistic state after a command


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Frigidaire timer number entities."""
    coordinators: dict[str, FrigidaireApplianceCoordinator] = hass.data[DOMAIN][entry.entry_id]["coordinators"]
    appliances: list[frigidaire.Appliance] = hass.data[DOMAIN][entry.entry_id]["appliances"]

    entities = [
        FrigidaireTimerNumber(coordinators[appliance.appliance_id], timer_type, suggest_area(hass, appliance.nickname))
        for appliance in appliances
        if appliance.destination == frigidaire.Destination.AIR_CONDITIONER
        for timer_type in ("on", "off")
    ]

    async_add_entities(entities)


class FrigidaireTimerNumber(CoordinatorEntity[FrigidaireApplianceCoordinator], NumberEntity):
    """AC ON or OFF timer, expressed in seconds with 30-minute steps."""

    def __init__(
        self,
        coordinator: FrigidaireApplianceCoordinator,
        timer_type: str,
        suggested_area: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._client = coordinator.client
        self._appliance = coordinator.appliance
        self._timer_type = timer_type  # "on" or "off"
        self._optimistic_until: float = 0
        self._optimistic_value: float | None = None

        suffix = "On Timer" if timer_type == "on" else "Off Timer"
        self._attr_unique_id = f"{self._appliance.appliance_id}_timer_{timer_type}"
        self._attr_name = suffix
        self._attr_native_min_value = 0
        self._attr_native_max_value = MAX_SECONDS
        self._attr_native_step = STEP_SECONDS
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS
        self._attr_device_class = NumberDeviceClass.DURATION
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
    def native_value(self) -> float:
        if time.monotonic() < self._optimistic_until:
            return self._optimistic_value or 0
        appliance_state = _normalize(self._details.get(frigidaire.Detail.APPLIANCE_STATE))
        if self._timer_type == "on":
            active = appliance_state in (frigidaire.ApplianceState.OFF, frigidaire.ApplianceState.DELAYED_START)
            detail_key = frigidaire.Detail.START_TIME
        else:
            active = appliance_state == frigidaire.ApplianceState.RUNNING
            detail_key = frigidaire.Detail.STOP_TIME
        if not active:
            return 0
        raw = self._details.get(detail_key) or 0
        return max(0, round(raw / STEP_SECONDS) * STEP_SECONDS)

    def set_native_value(self, value: float) -> None:
        seconds = int(round(value / STEP_SECONDS) * STEP_SECONDS)
        seconds = max(0, min(MAX_SECONDS, seconds))
        action = (
            frigidaire.Action.set_start_time(seconds)
            if self._timer_type == "on"
            else frigidaire.Action.set_stop_time(seconds)
        )
        self._client.execute_action(self._appliance, action)
        self._optimistic_value = float(seconds)
        self._optimistic_until = time.monotonic() + OPTIMISTIC_WINDOW
        self.schedule_update_ha_state(force_refresh=True)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Clear stale optimistic state once the real value has settled."""
        if time.monotonic() >= self._optimistic_until:
            self._optimistic_value = None
        super()._handle_coordinator_update()
