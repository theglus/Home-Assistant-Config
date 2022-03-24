"""Support for Coway IoCare"""
import asyncio
import logging
import voluptuous as vol
from iocare import IOCareApi

import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME
)
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup of the component"""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up IoCare integration from a config entry."""
    username = config_entry.data.get(CONF_USERNAME)
    password = config_entry.data.get(CONF_PASSWORD)

    _LOGGER.info("Initializing the IOCare API")
    iocare = await hass.async_add_executor_job(IOCareApi, username, password)
    _LOGGER.info("Connected to API")

    hass.data[DOMAIN] = iocare

    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "fan")
    )
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "air_quality")
    )
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "switch")
    )

    return True
