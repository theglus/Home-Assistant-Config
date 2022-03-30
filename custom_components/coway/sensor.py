""" Coway Airmega Purifier Air Quality Sensors"""
from datetime import time
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity, STATE_CLASS_MEASUREMENT, SensorDeviceClass
from .const import DOMAIN
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
)
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Coway Air Quality sensors."""

    _LOGGER.info("Setting up config entry for the Coway Airmega sensor platform")

    coordinator = hass.data[DOMAIN]

    sensors = []

    for idx, ent in enumerate(coordinator.data):
        if not coordinator.data[idx].new_model:
            sensors.append(AirQualityIndex(coordinator, idx))
        sensors.append(PreFilter(coordinator, idx))
        sensors.append(MAX2Filter(coordinator, idx))
        sensors.append(TimerRemaining(coordinator, idx))
        sensors.append(ParticulateMatter25(coordinator, idx))
        sensors.append(ParticulateMatter10(coordinator, idx))
        sensors.append(CarbonDioxide(coordinator, idx))
        sensors.append(VolatileOrganicCompounds(coordinator, idx))

    async_add_entities(sensors)


class PreFilter(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega Pre Filter Percentage Remaining."""

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
        return self.coordinator.data[self._device].device_id + '_pre_filter'

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self.coordinator.data[self._device].name + ' Pre Filter'

    @property
    def native_value(self):
        """Returns Pre Filter Percentage"""
        return self.coordinator.data[self._device].filters[0]["life_level_pct"]

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False

class MAX2Filter(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega MAX2 Filter Percentage Remaining."""

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
        return self.coordinator.data[self._device].device_id + '_max_filter'

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self.coordinator.data[self._device].name + ' MAX2 Filter'

    @property
    def native_value(self):
        """Returns MAX2 Filter Percentage"""
        return self.coordinator.data[self._device].filters[1]["life_level_pct"]

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False

class TimerRemaining(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega MAX2 Filter Percentage Remaining."""

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
        return self.coordinator.data[self._device].device_id + '_timer_remaining'

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self.coordinator.data[self._device].name + ' Timer Remaining'

    @property
    def native_value(self):
        """Returns time left on timer"""
        total_time = round((float(self.coordinator.data[self._device].timer_remaining) / 60), 2)
        hours, minutes = int(total_time), round(((total_time - int(total_time)) * 60))
        timer_remaining = time(hour = hours, minute = minutes)
        return timer_remaining.isoformat(timespec = "minutes")

    @property
    def icon(self):
        return 'mdi:timer'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False

class AirQualityIndex(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega Air Quality Index."""

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
        return self.coordinator.data[self._device].device_id + '_aqi'

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self.coordinator.data[self._device].name + ' AQI'

    @property
    def native_value(self):
        """Return AQI Measurement"""
        return round(float(self.coordinator.data[self._device].quality["air_quality_index"]), 1)

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.AQI

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False


class ParticulateMatter25(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega Particulate Matter 2.5"""

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
        return self.coordinator.data[self._device].device_id + '_particulate_matter_2_5'

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.coordinator.data[self._device].name + ' Particulate Matter 2.5'

    @property
    def native_value(self):
        """Return the particulate matter 2.5 level."""
        return self.coordinator.data[self._device].quality["particulate_matter_2_5"]

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.PM25

    @property
    def unit_of_measurement(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False


class ParticulateMatter10(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega Particulate Matter 1.0"""

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
        return self.coordinator.data[self._device].device_id + '_particulate_matter_1_0'

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.coordinator.data[self._device].name + ' Particulate Matter 10'

    @property
    def native_value(self):
        """Return the particulate matter 1.0 level."""
        return self.coordinator.data[self._device].quality["particulate_matter_10"]

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.PM10

    @property
    def unit_of_measurement(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False


class CarbonDioxide(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega Carbon Dioxide Sensor"""

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
        return self.coordinator.data[self._device].device_id + '_carbon_dioxide'

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.coordinator.data[self._device].name + ' Carbon Dioxide'

    @property
    def native_value(self):
        """Return the CO2 (carbon dioxide) level."""
        return self.coordinator.data[self._device].quality["carbon_dioxide"]

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.CO2

    @property
    def unit_of_measurement(self):
        return CONCENTRATION_PARTS_PER_MILLION

    @property
    def icon(self):
        return 'mdi:molecule-co2'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False


class VolatileOrganicCompounds(CoordinatorEntity, SensorEntity):
    """Representation of a Coway Airmega VOC Sensor"""

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
        return self.coordinator.data[self._device].device_id + '_voc'

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.coordinator.data[self._device].name + ' VOC'

    @property
    def native_value(self):
        """Return the VOC (Volatile Organic Compounds) level."""
        return self.coordinator.data[self._device].quality["volatile_organic_compounds"]

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS

    @property
    def icon(self):
        return 'mdi:air-filter'

    @property
    def available(self):
        """Return true if purifier is available."""
        if hasattr(self.coordinator.data[self._device], 'device_connected_to_servers'):
            return self.coordinator.data[self._device].device_connected_to_servers
        else:
            return False
