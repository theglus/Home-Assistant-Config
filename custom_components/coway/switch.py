"""Support for IOCare switches."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Coway Air Purifier devices."""

    coordinator = hass.data[DOMAIN]

    async_add_entities(
        IOCareSwitch(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class IOCareSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Coway Airmega air purifier switch."""

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
        """Return the name of the purifier + Light if any."""
        return self.coordinator.data[self._device].name + " Light"

    @property
    def icon(self):
        """Set purifier switch icon to lightbulb"""
        return 'mdi:lightbulb'

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.coordinator.data[self._device].is_light_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_light, True)
        self.coordinator.data[self._device].is_light_on = True
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_light, False)
        self.coordinator.data[self._device].is_light_on = False
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False
