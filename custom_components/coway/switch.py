"""Support for IOCare switches."""
import logging
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)



def setup_platform(hass, config, add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Coway Air Purifier devices."""
    iocare = hass.data[DOMAIN]

    devices = []

    for device in iocare.devices():
        devices.append(IOCareSwitch(device))

    async_add_entities(devices)


class IOCareSwitch(SwitchEntity):
    """Representation of a Coway Airmega air purifier switch."""

    def __init__(self, device):
        self._device = device
        self._available = True

    @property
    def unique_id(self):
        """Return the ID of this purifier."""
        return self._device.device_id

    @property
    def name(self):
        """Return the name of the purifier + Light if any."""
        return self._device.name + " Light"

    @property
    def icon(self):
        """Set purifier switch icon to lightbulb"""
        return 'mdi:lightbulb'

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._device.is_light_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.set_light(True)

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._device.set_light(False)
