""" Setting Up Coway Select Entities """

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.select import SelectEntity

from .const import (
    DOMAIN,
    IOCARE_TIMER_OFF,
    IOCARE_TIMER_1H,
    IOCARE_TIMER_2H,
    IOCARE_TIMER_4H,
    IOCARE_TIMER_8H
)

IOCARE_TIMERS = ["OFF", "1 Hour", "2 Hours", "4 Hours", "8 Hours"]

IOCARE_TIMERS_TO_HASS = {
    IOCARE_TIMER_OFF: "OFF",
    IOCARE_TIMER_1H: "1 Hour",
    IOCARE_TIMER_2H: "2 Hours",
    IOCARE_TIMER_4H: "4 Hours",
    IOCARE_TIMER_8H: "8 Hours"
}

HASS_TIMER_TO_IOCARE = {v: k for (k, v) in IOCARE_TIMERS_TO_HASS.items()}


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Coway Air Purifier select entity."""

    coordinator = hass.data[DOMAIN]

    async_add_entities(
        CowayTimer(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )

######### Timer Select Entities #########

class CowayTimer(CoordinatorEntity, SelectEntity):
    """Representation of a Coway Airmega air purifier select entity."""

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
        return self.coordinator.data[self._device].name + " Current Timer"

    @property
    def icon(self):
        """Set icon"""
        if self.current_option is "OFF":
            return 'mdi:timer-off'
        else:
            return 'mdi:timer'

    @property
    def current_option(self):
        """Returns Currently Active Timer"""
        try:
            return IOCARE_TIMERS_TO_HASS.get(self.coordinator.data[self._device].timer)
        except AttributeError:
            _LOGGER.warning(f'Coway IoCare: Unable to get info for {self.coordinator.data[self._device].name}. Make sure purifier is connected to WiFi.')

    @property
    def options(self):
        return IOCARE_TIMERS

    async def async_select_option(self, option) -> None:
        """Change the selected option."""
        await self.hass.async_add_executor_job(self.coordinator.data[self._device].set_timer, HASS_TIMER_TO_IOCARE.get(option))
        self.coordinator.data[self._device].timer = HASS_TIMER_TO_IOCARE.get(option)
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False
