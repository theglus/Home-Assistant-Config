"""Fan platform for Coway integration."""
from __future__ import annotations

from typing import Any
import asyncio

from cowayaio.purifier_model import CowayPurifier

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    COWAY_COORDINATOR,
    DOMAIN,
    IOCARE_FAN_LOW,
    IOCARE_FAN_OFF,
    IOCARE_FAN_SPEED_TO_HASS,
    ORDERED_NAMED_FAN_SPEEDS,
    PRESET_MODES,
    PRESET_MODES_AP,
    PRESET_MODE_AUTO,
    PRESET_MODE_ECO,
    PRESET_MODE_NIGHT,
)
from .coordinator import CowayDataUpdateCoordinator


HASS_FAN_SPEED_TO_IOCARE = {v: k for (k, v) in IOCARE_FAN_SPEED_TO_HASS.items()}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Coway Fan Entities."""

    coordinator: CowayDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][COWAY_COORDINATOR]

    fans = []

    for purifier_id, purifier_data in coordinator.data.purifiers.items():
            fans.extend((
                Purifier(coordinator, purifier_id),
            ))

    async_add_entities(fans)


class Purifier(CoordinatorEntity, FanEntity):
    """Representation of a Coway Airmega air purifier."""

    def __init__(self, coordinator, purifier_id):
        super().__init__(coordinator)
        self.purifier_id = purifier_id

    @property
    def purifier_data(self) -> CowayPurifier:
        """Handle coordinator purifier data."""

        return self.coordinator.data.purifiers[self.purifier_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device registry information for this entity."""

        return {
            "identifiers": {(DOMAIN, self.purifier_data.device_attr['device_id'])},
            "name": self.purifier_data.device_attr['name'],
            "manufacturer": "Coway",
            "model": self.purifier_data.device_attr['model'],
        }

    @property
    def unique_id(self) -> str:
        """Sets unique ID for this entity."""

        return self.purifier_data.device_attr['device_id'] + '_purifier'

    @property
    def name(self) -> str:
        """Return name of the entity."""

        return "Purifier"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""

        return True

    @property
    def is_on(self) -> bool:
        """Return true if the purifier is on."""

        return self.purifier_data.is_on

    @property
    def preset_modes(self) -> list:
        """Return the available preset modes."""

        if self.purifier_data.device_attr['model'] == "AIRMEGA AP-1512HHS":
            return PRESET_MODES_AP
        else:
            return PRESET_MODES

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""

        if self.purifier_data.device_attr['model'] == "AIRMEGA AP-1512HHS":
            if self.purifier_data.auto_mode:
                return PRESET_MODE_AUTO
            if self.purifier_data.eco_mode:
                return PRESET_MODE_ECO
        else:
            if self.purifier_data.auto_eco_mode or self.purifier_data.auto_mode:
                return PRESET_MODE_AUTO
            if self.purifier_data.night_mode:
                return PRESET_MODE_NIGHT

    @property
    def percentage(self) -> int:
        """Return the current speed."""

        if not self.is_on:
            return 0
        return IOCARE_FAN_SPEED_TO_HASS.get(self.purifier_data.fan_speed)

    @property
    def speed_count(self) -> int:
        """Get length of available speeds list."""

        return len(ORDERED_NAMED_FAN_SPEEDS)

    @property
    def supported_features(self) -> int:
        """Return supported features."""

        return FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE

    @property
    def available(self) -> bool:
        """Return true if purifier is connected to Coway servers."""

        if self.purifier_data.network_status:
            return True
        else:
            return False

    async def async_turn_on(self, percentage: int = None, **kwargs) -> None:
        """Turn the air purifier on."""

        if percentage is not None:
            speed = HASS_FAN_SPEED_TO_IOCARE.get(percentage)
            await self.coordinator.client.async_set_power(self.purifier_data.device_attr, True)
            await asyncio.sleep(1.5)
            await self.coordinator.client.async_set_fan_speed(self.purifier_data.device_attr, speed)
            self.purifier_data.is_on = True
            self.purifier_data.light_on = True
            self.purifier_data.auto_mode = False
            self.purifier_data.night_mode = False
            self.purifier_data.fan_speed = speed
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
        else:
            await self.coordinator.client.async_set_power(self.purifier_data.device_attr, True)
            self.purifier_data.is_on = True
            self.purifier_data.light_on = True
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the air purifier off."""

        await self.coordinator.client.async_set_power(self.purifier_data.device_attr, False)
        self.purifier_data.is_on = False
        self.purifier_data.light_on = False
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the fan speed of the air purifier."""

        if percentage == 0:
            await self.async_turn_off()
        else:
            if not self.is_on:
                await self.async_turn_on(percentage)
            else:
                speed = HASS_FAN_SPEED_TO_IOCARE.get(percentage)
                await self.coordinator.client.async_set_fan_speed(self.purifier_data.device_attr, speed)
                self.purifier_data.fan_speed = speed
                self.purifier_data.auto_mode = False
                self.purifier_data.night_mode = False
                self.async_write_ha_state()
                await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set a preset mode for the purifier."""

        if not self.is_on:
            await self.coordinator.client.async_set_power(self.purifier_data.device_attr, True)
            self.purifier_data.is_on = True
            self.purifier_data.light_on = True
            await asyncio.sleep(1.5)
        if preset_mode == PRESET_MODE_AUTO:
            await self.coordinator.client.async_set_auto_mode(self.purifier_data.device_attr)
            self.purifier_data.auto_mode = True
            self.purifier_data.auto_eco_mode = False
            self.purifier_data.eco_mode = False
            self.purifier_data.night_mode = False
            self.purifier_data.fan_speed = IOCARE_FAN_LOW
        if preset_mode in [PRESET_MODE_NIGHT, PRESET_MODE_ECO]:
            if self.purifier_data.device_attr['model'] == "AIRMEGA AP-1512HHS":
                await self.coordinator.client.async_set_eco_mode(self.purifier_data.device_attr)
                self.purifier_data.eco_mode = True
            else:
                await self.coordinator.client.async_set_night_mode(self.purifier_data.device_attr)
                self.purifier_data.auto_eco_mode = False
                self.purifier_data.night_mode = True
            self.purifier_data.auto_mode = False
            self.purifier_data.fan_speed = IOCARE_FAN_OFF

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
