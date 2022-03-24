"""Support for Coway Air Purifiers."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.percentage import ordered_list_item_to_percentage
from homeassistant.components.fan import (
    FanEntity,
    SUPPORT_SET_SPEED,
    SUPPORT_PRESET_MODE,
)

from .const import (
    DOMAIN,
    IOCARE_FAN_OFF,
    IOCARE_FAN_LOW,
    IOCARE_FAN_MEDIUM,
    IOCARE_FAN_HIGH,
    IOCARE_TIMER_OFF,
    IOCARE_TIMER_1H,
    IOCARE_TIMER_2H,
    IOCARE_TIMER_4H,
    IOCARE_TIMER_8H,
    PRESET_MODE_AUTO,
    PRESET_MODE_NIGHT
)

ORDERED_NAMED_FAN_SPEEDS = [IOCARE_FAN_LOW, IOCARE_FAN_MEDIUM, IOCARE_FAN_HIGH]
PRESET_MODES = [PRESET_MODE_AUTO, PRESET_MODE_NIGHT]


IOCARE_FAN_SPEED_TO_HASS = {
    IOCARE_FAN_OFF: 0,
    IOCARE_FAN_LOW: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_LOW),
    IOCARE_FAN_MEDIUM: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_MEDIUM),
    IOCARE_FAN_HIGH: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_HIGH)
}

HASS_FAN_SPEED_TO_IOCARE = {v: k for (k, v) in IOCARE_FAN_SPEED_TO_HASS.items()}


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Coway Air Purifier devices."""

    coordinator = hass.data[DOMAIN]

    async_add_entities(
        AirPurifier(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class AirPurifier(CoordinatorEntity, FanEntity):
    """Representation of a Coway Airmega air purifier."""

    def __init__(self, coordinator, idx):
        super().__init__(coordinator)
        self._device = idx

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data[self._device].device_id)},
            "name": self.coordinator.data[self._device].name,
            "manufacturer": "Coway",
            "model": self.coordinator.data[self._device].product_name_full,
        }

    @property
    def unique_id(self):
        """Return the ID of this purifier."""
        return self.coordinator.data[self._device].device_id

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self.coordinator.data[self._device].name

    @property
    def is_on(self):
        """Return true if the purifier is on"""
        return self.coordinator.data[self._device].is_on

    @property
    def preset_modes(self):
        """Return the available preset modes"""
        return PRESET_MODES

    @property
    def preset_mode(self):
        """"Return the current preset mode"""
        if self.coordinator.data[self._device].is_auto_eco:
            return PRESET_MODE_AUTO
        if self.coordinator.data[self._device].is_auto:
            return PRESET_MODE_AUTO
        if self.coordinator.data[self._device].is_night:
            return PRESET_MODE_NIGHT

    @property
    def percentage(self) -> int:
        """Return the current speed."""
        if not self.coordinator.data[self._device].is_on:
            return 0
        return IOCARE_FAN_SPEED_TO_HASS.get(self.coordinator.data[self._device].fan_speed)

    @property
    def speed_count(self) -> int:
        """Get the list of available speeds."""
        return len(ORDERED_NAMED_FAN_SPEEDS)

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_SET_SPEED | SUPPORT_PRESET_MODE

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False

    async def async_turn_on(self, percentage: int = None, **kwargs) -> None:
        """Turn the air purifier on."""
        if percentage is not None:
            await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_fan_speed, HASS_FAN_SPEED_TO_IOCARE.get(percentage))
            self.coordinator.data[self._device].fan_speed = HASS_FAN_SPEED_TO_IOCARE.get(percentage)
            await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_power, True)
            self.coordinator.data[self._device].is_on = True
            self.coordinator.data[self._device].is_light_on = True
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
        else:
            await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_power, True)
            self.coordinator.data[self._device].is_on = True
            self.coordinator.data[self._device].is_light_on = True
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()


    async def async_turn_off(self, **kwargs) -> None:
        """Turn the air purifier off."""
        await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_power, False)
        self.coordinator.data[self._device].is_on = False
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the fan_mode of the air purifier."""
        if percentage == 0:
            await self.async_turn_off()
        elif not self.is_on:
            await self.async_turn_on(percentage)
        else:
            await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_fan_speed, HASS_FAN_SPEED_TO_IOCARE.get(percentage))
            self.coordinator.data[self._device].fan_speed = HASS_FAN_SPEED_TO_IOCARE.get(percentage)
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set a preset mode on the fan."""
        if preset_mode == PRESET_MODE_AUTO:
            if not self.is_on:
                await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_auto_mode)
                self.coordinator.data[self._device].is_auto = True
                self.coordinator.data[self._device].fan_speed = IOCARE_FAN_LOW
                self.async_write_ha_state()
                await self.async_turn_on()
            else:
                await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_auto_mode)
                self.coordinator.data[self._device].is_auto = True
                self.coordinator.data[self._device].fan_speed = IOCARE_FAN_LOW
                self.async_write_ha_state()
                await self.coordinator.async_request_refresh()
        if preset_mode == PRESET_MODE_NIGHT:
            if not self.is_on:
                await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_night_mode)
                self.coordinator.data[self._device].is_night = True
                self.coordinator.data[self._device].is_auto = False
                self.coordinator.data[self._device].fan_speed = IOCARE_FAN_OFF
                self.async_write_ha_state()
                await self.async_turn_on()
            else:
                await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_night_mode)
                self.coordinator.data[self._device].is_night = True
                self.coordinator.data[self._device].is_auto = False
                self.coordinator.data[self._device].fan_speed = IOCARE_FAN_OFF
                self.async_write_ha_state()
                await self.coordinator.async_request_refresh()
