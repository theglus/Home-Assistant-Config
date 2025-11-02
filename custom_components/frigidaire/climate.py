"""ClimateEntity for frigidaire integration."""
from __future__ import annotations

import logging
from typing import Optional, List, Mapping, Any, Dict

import frigidaire

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_OFF,
    HVACMode,
    ClimateEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up frigidaire from a config entry."""
    client = hass.data[DOMAIN][entry.entry_id]

    def get_entities(username: str, password: str) -> List[frigidaire.Appliance]:
        return client.get_appliances()

    appliances = await hass.async_add_executor_job(
        get_entities, entry.data["username"], entry.data["password"]
    )

    async_add_entities(
        [
            FrigidaireClimate(client, appliance)
            for appliance in appliances
            if appliance.destination == frigidaire.Destination.AIR_CONDITIONER
        ],
        update_before_add=True,
    )


FRIGIDAIRE_TO_HA_UNIT = {
    frigidaire.Unit.FAHRENHEIT: UnitOfTemperature.FAHRENHEIT,
    frigidaire.Unit.CELSIUS: UnitOfTemperature.CELSIUS,
}

FRIGIDAIRE_TO_HA_MODE = {
    frigidaire.Mode.OFF: HVACMode.OFF,
    frigidaire.Mode.COOL: HVACMode.COOL,
    frigidaire.Mode.FAN: HVACMode.FAN_ONLY,
    frigidaire.Mode.ECO: HVACMode.AUTO,
}

FRIGIDAIRE_TO_HA_FAN_SPEED = {
    frigidaire.FanSpeed.AUTO: FAN_AUTO,
    frigidaire.FanSpeed.LOW: FAN_LOW,
    frigidaire.FanSpeed.MEDIUM: FAN_MEDIUM,
    frigidaire.FanSpeed.HIGH: FAN_HIGH,
}

HA_TO_FRIGIDAIRE_UNIT = {
    UnitOfTemperature.FAHRENHEIT: frigidaire.Unit.FAHRENHEIT,
    UnitOfTemperature.CELSIUS: frigidaire.Unit.CELSIUS,
}

HA_TO_FRIGIDAIRE_FAN_MODE = {
    FAN_AUTO: frigidaire.FanSpeed.AUTO,
    FAN_LOW: frigidaire.FanSpeed.LOW,
    FAN_MEDIUM: frigidaire.FanSpeed.MEDIUM,
    FAN_HIGH: frigidaire.FanSpeed.HIGH,
}

HA_TO_FRIGIDAIRE_HVAC_MODE = {
    HVACMode.AUTO: frigidaire.Mode.ECO,
    HVACMode.FAN_ONLY: frigidaire.Mode.FAN,
    HVACMode.COOL: frigidaire.Mode.COOL,
    HVACMode.OFF: frigidaire.Mode.OFF,
}


class FrigidaireClimate(ClimateEntity):
    """Representation of a Frigidaire appliance."""

    def __init__(self, client, appliance):
        """Build FrigidaireClimate.

        client: the client used to contact the frigidaire API
        appliance: the basic information about the frigidaire appliance, used to contact
            the API
        """

        self._client: frigidaire.Frigidaire = client
        self._appliance: frigidaire.Appliance = appliance
        self._details: Optional[Dict] = None

        # Entity Class Attributes
        self._attr_unique_id = self._appliance.appliance_id
        self._attr_name = self._appliance.nickname
        self._attr_supported_features = (ClimateEntityFeature.TARGET_TEMPERATURE |
                                         ClimateEntityFeature.FAN_MODE |
                                         ClimateEntityFeature.TURN_OFF |
                                         ClimateEntityFeature.TURN_ON)
        self._attr_target_temperature_step = 1

        # Although we can access the Frigidaire API to get updates, they are
        # not reflected immediately after making a request. To improve the UX
        # around this, we set assume_state to True
        self._attr_assumed_state = True

        self._attr_fan_modes = [
            FAN_AUTO,
            FAN_LOW,
            FAN_MEDIUM,
            FAN_HIGH,
        ]

        self._attr_hvac_modes = [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.AUTO,
            HVACMode.FAN_ONLY,
        ]

    @property
    def assumed_state(self):
        """Return True if unable to access real state of the entity."""
        return self._attr_assumed_state

    @property
    def unique_id(self):
        """Return unique ID based on Frigidaire ID."""
        return self._attr_unique_id

    @property
    def name(self):
        """Return the name of the entity."""
        return self._attr_name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._attr_supported_features

    @property
    def hvac_modes(self):
        """List of available operation modes."""
        return self._attr_hvac_modes

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return self._attr_target_temperature_step

    @property
    def fan_modes(self):
        """List of available fan modes."""
        return self._attr_fan_modes

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        unit = self._details.get(
            frigidaire.Detail.TEMPERATURE_REPRESENTATION
        )

        return FRIGIDAIRE_TO_HA_UNIT[unit]

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return self._details.get(frigidaire.Detail.TARGET_TEMPERATURE_F)
        else:
            return self._details.get(frigidaire.Detail.TARGET_TEMPERATURE_C)

    @property
    def hvac_mode(self):
        """Return current operation i.e. heat, cool, idle."""
        frigidaire_mode = self._details.get(frigidaire.Detail.MODE)

        return FRIGIDAIRE_TO_HA_MODE[frigidaire_mode]

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F)
        else:
            return self._details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C)

    @property
    def fan_mode(self):
        """Return the fan setting."""
        fan_speed = self._details.get(frigidaire.Detail.FAN_SPEED)

        if not fan_speed:
            return FAN_OFF

        return FRIGIDAIRE_TO_HA_FAN_SPEED[fan_speed]

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return 60

        return 16

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self.temperature_unit == UnitOfTemperature.FAHRENHEIT:
            return 90

        return 32

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {
            "check_filter": bool(
                self._details.get(frigidaire.Detail.FILTER_STATE) == "CHANGE"
            ),
        }

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        temperature = int(temperature)
        temperature_unit = HA_TO_FRIGIDAIRE_UNIT[self.temperature_unit]

        _LOGGER.debug("Setting temperature to int({}) {}".format(temperature, self.temperature_unit))
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_temperature(temperature, temperature_unit)
        )

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        # Guard against unexpected fan modes
        if fan_mode not in HA_TO_FRIGIDAIRE_FAN_MODE:
            return

        action = frigidaire.Action.set_fan_speed(HA_TO_FRIGIDAIRE_FAN_MODE[fan_mode])
        self._client.execute_action(self._appliance, action)

    def set_hvac_mode(self, hvac_mode):
        """Set new target operation mode."""
        if hvac_mode == HVACMode.OFF:
            self._client.execute_action(
                self._appliance, frigidaire.Action.set_power(frigidaire.Power.OFF)
            )
            return

        # Guard against unexpected hvac modes
        if hvac_mode not in HA_TO_FRIGIDAIRE_HVAC_MODE:
            return

        # Turn on if not currently on.
        if self._details.get(frigidaire.Detail.MODE) == frigidaire.Mode.OFF:
            self._client.execute_action(
                self._appliance, frigidaire.Action.set_power(frigidaire.Power.ON)
            )

            # temperature reverts to default when the device is turned on
            self._client.execute_action(
                self._appliance,
                frigidaire.Action.set_temperature(int(self.target_temperature))
            )

        self._client.execute_action(
            self._appliance,
            frigidaire.Action.set_mode(HA_TO_FRIGIDAIRE_HVAC_MODE[hvac_mode]),
        )

    def update(self):
        """Retrieve latest state and updates the details."""
        try:
            details = self._client.get_appliance_details(self._appliance)
            self._details = details
        except frigidaire.FrigidaireException:
            if self.available:
                _LOGGER.error("Failed to connect to Frigidaire servers")
            self._attr_available = False
        else:
            self._attr_available = (
                self._details.get("connectivityState")
                == "connected"
            )
