"""Select platform for Coway integration."""
from __future__ import annotations

from typing import Any

from cowayaio.purifier_model import CowayPurifier

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    COWAY_COORDINATOR,
    DOMAIN,
    IOCARE_TIMERS,
    IOCARE_TIMERS_TO_HASS,
    LOGGER,
)
from .coordinator import CowayDataUpdateCoordinator


HASS_TIMER_TO_IOCARE = {v: k for (k, v) in IOCARE_TIMERS_TO_HASS.items()}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Coway Select Entities."""

    coordinator: CowayDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][COWAY_COORDINATOR]

    selects = []

    for purifier_id, purifier_data in coordinator.data.purifiers.items():
            selects.extend((
                Timer(coordinator, purifier_id),
            ))

    async_add_entities(selects)

class Timer(CoordinatorEntity, SelectEntity):
    """Representation of purifier timer."""

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

        return self.purifier_data.device_attr['device_id'] + '_timer'

    @property
    def name(self) -> str:
        """Return name of the entity."""

        return "Current timer"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""

        return True

    @property
    def icon(self) -> str:
        """Set icon."""

        if self.current_option is "OFF":
            return 'mdi:timer-off'
        else:
            return 'mdi:timer'

    @property
    def current_option(self) -> str:
        """Returns currently active timer."""

        return IOCARE_TIMERS_TO_HASS.get(self.purifier_data.timer)

    @property
    def options(self) -> list:
        """Return list of all the available timers."""

        return IOCARE_TIMERS

    @property
    def available(self) -> bool:
        """Return true if purifier is connected to Coway servers."""

        if self.purifier_data.network_status:
            return True
        else:
            return False

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""

        if self.purifier_data.is_on:
            time = HASS_TIMER_TO_IOCARE.get(option)
            await self.coordinator.client.async_set_timer(self.purifier_data.device_attr, time)
            self.purifier_data.timer = time
            self.purifier_data.timer_remaining = time
        else:
            LOGGER.error(f'Setting a timer for {self.purifier_data.device_attr["name"]} can only be done when the purifier is On.')
            self.purifier_data.timer = '0'
            self.purifier_data.timer_remaining = '0'

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

