"""Support for Coway Air Quality Sensor."""

import logging
from homeassistant.components.air_quality import AirQualityEntity
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Coway Air Quality device."""
    _LOGGER.info("Setting up config entry for the Air Quality platform")

    iocare = hass.data[DOMAIN]

    devices = []
    for device in iocare.devices():
        devices.append(AirMonitor(device))

    async_add_entities(devices)


class AirMonitor(AirQualityEntity):
    """Representation of a Coway Airmega air monitor."""

    def __init__(self, device):
        self._device = device
        self._available = True

    @property
    def unique_id(self):
        """Return the ID of this purifier."""
        return self._device.device_id

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self._device.name

    @property
    def air_quality_index(self):
        """Return the Air Quality Index (AQI)."""
        return round(float(self._device.quality["air_quality_index"]), 1)

    @property
    def particulate_matter_2_5(self):
        """Return the particulate matter 2.5 level."""
        return self._device.quality["particulate_matter_2_5"]

    @property
    def particulate_matter_10(self):
        """Return the particulate matter 10 level."""
        return self._device.quality["particulate_matter_10"]

    @property
    def carbon_dioxide(self):
        """Return the CO2 (carbon dioxide) level."""
        return self._device.quality["carbon_dioxide"]

    @property
    def volatile_organic_compounds(self):
        """Return the VOC (Volatile Organic Compounds) level."""
        return self._device.quality["volatile_organic_compounds"]

    @property
    def state(self):
        """Return the current state."""
        return self.air_quality_index

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._device.refresh()
