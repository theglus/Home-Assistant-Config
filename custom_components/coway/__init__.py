"""Support for Coway IOCare"""
from datetime import timedelta
import asyncio
import logging
from iocare import IOCareApi

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME
)
from .const import DOMAIN, PLATFORMS


_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup of the component"""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up IOCare integration from a config entry."""
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    _LOGGER.info("Initializing the IOCare API")

    iocare = await hass.async_add_executor_job(IOCareApi, username, password)

    _LOGGER.info("Connected to API")


    async def async_update_data():
        """ Fetch data from IOCare API """
        try:
            iocare_update_data = await hass.async_add_executor_job(iocare.poll_devices_update)
            return iocare_update_data
        except Exception as e:
            raise UpdateFailed(f"Error occured while fetching data from IOCare servers: {e}")


    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name ="iocare_coordinator",
        update_method = async_update_data,
        update_interval = timedelta(seconds=30),
        )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Coway config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok
