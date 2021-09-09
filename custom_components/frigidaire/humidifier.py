"""ClimateEntity for frigidaire integration."""
from __future__ import annotations

import logging
from typing import List, Any, Mapping, Optional

import frigidaire
import voluptuous as vol

from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.humidifier.const import (
    DEVICE_CLASS_DEHUMIDIFIER,
    MODE_BOOST,
    MODE_NORMAL,
    SUPPORT_MODES,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


FAN_LOW = "low"
FAN_HIGH = "high"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up frigidaire from a config entry."""
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "set_fan_mode",
        {vol.Required("fan_mode"): cv.string},
        "set_fan_mode",
    )

    client = hass.data[DOMAIN][entry.entry_id]

    def get_entities(username: str, password: str) -> List[frigidaire.Appliance]:
        return client.get_appliances()

    appliances = await hass.async_add_executor_job(
        get_entities, entry.data["username"], entry.data["password"]
    )

    async_add_entities(
        [
            FrigidaireDehumidifier(client, appliance)
            for appliance in appliances
            if appliance.appliance_class == frigidaire.ApplianceClass.DEHUMIDIFIER
        ],
        update_before_add=True,
    )


FRIGIDAIRE_TO_HA_MODE = {
    frigidaire.Mode.DRY.value: MODE_NORMAL,
    frigidaire.Mode.CONTINUOUS.value: MODE_BOOST,
}

HA_TO_FRIGIDAIRE_MODE = {
    MODE_NORMAL: frigidaire.Mode.DRY,
    MODE_BOOST: frigidaire.Mode.CONTINUOUS,
}

FRIGIDAIRE_TO_HA_FAN_MODE = {
    frigidaire.FanSpeed.LOW.value: FAN_LOW,
    frigidaire.FanSpeed.HIGH.value: FAN_HIGH,
}

HA_TO_FRIGIDAIRE_FAN_MODE = {
    FAN_LOW: frigidaire.FanSpeed.LOW,
    FAN_HIGH: frigidaire.FanSpeed.HIGH,
}


class FrigidaireDehumidifier(HumidifierEntity):
    """Representation of a Frigidaire dehumidifier."""

    def __init__(self, client, appliance):
        """Build FrigidaireClimate.

        client: the client used to contact the frigidaire API
        appliance: the basic information about the frigidaire appliance, used to contact the API
        """

        self._client: frigidaire.Frigidaire = client
        self._appliance: frigidaire.Appliance = appliance
        self._details: Optional[frigidaire.ApplianceDetails] = None

        # Entity Class Attributes
        self._attr_unique_id = self._appliance.appliance_id
        self._attr_name = self._appliance.nickname
        self._attr_supported_features = SUPPORT_MODES

        # Although we can access the Frigidaire API to get updates, they are
        # not reflected immediately after making a request. To improve the UX
        # around this, we set assume_state to True
        self._attr_assumed_state = True

        # self._attr_fan_modes = [
        #     FAN_LOW,
        #     FAN_HIGH,
        # ]

        self._attr_modes = [
            MODE_NORMAL,
            MODE_BOOST,
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
    def device_class(self):
        return DEVICE_CLASS_DEHUMIDIFIER

    @property
    def is_on(self):
        return (
            self._details.for_code(frigidaire.HaclCode.APPLIANCE_STATE).number_value
            != 0
        )

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._attr_supported_features

    @property
    def available_modes(self):
        """List of available operation modes."""
        return self._attr_modes

    @property
    def target_humidity(self):
        """Return the humidity we try to reach."""
        return self._details.for_code(frigidaire.HaclCode.TARGET_HUMIDITY).number_value

    @property
    def mode(self):
        """Return current operation ie. dry, continuous."""
        frigidaire_mode = self._details.for_code(
            frigidaire.HaclCode.AC_MODE
        ).number_value

        return FRIGIDAIRE_TO_HA_MODE[frigidaire_mode]

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        fan_speed = self._details.for_code(
            frigidaire.HaclCode.AC_FAN_SPEED_SETTING
        ).number_value

        return {
            "current_humidity": self._details.for_code(
                frigidaire.HaclCode.AMBIENT_HUMIDITY
            ).number_value,
            "check_filter": bool(
                self._details.for_code(
                    frigidaire.HaclCode.AC_CLEAN_FILTER_ALERT
                ).number_value
            ),
            "fan_mode": FRIGIDAIRE_TO_HA_FAN_MODE[fan_speed],
        }

    @property
    def min_humidity(self):
        """Return the minimum humidity."""
        return 35

    @property
    def max_humidity(self):
        """Return the maximum humidity."""
        return 85

    def turn_on(self, **kwargs: Any) -> None:
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_power(frigidaire.Power.ON)
        )

    def turn_off(self, **kwargs: Any) -> None:
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_power(frigidaire.Power.OFF)
        )

    def set_humidity(self, humidity: int):
        """Set new target humidity."""
        if humidity is None:
            return
        # Only supports 5% steps
        humidity = 5 * round(humidity / 5)
        # We have to be in dry mode to set a target humidity
        self.set_mode(MODE_NORMAL)
        self._client.execute_action(
            self._appliance, frigidaire.Action.set_humidity(humidity)
        )

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        # Guard against unexpected fan modes
        if fan_mode not in HA_TO_FRIGIDAIRE_FAN_MODE:
            return

        action = frigidaire.Action.set_fan_speed(HA_TO_FRIGIDAIRE_FAN_MODE[fan_mode])
        self._client.execute_action(self._appliance, action)

    def set_mode(self, mode):
        """Set new target operation mode."""

        # Guard against unexpected modes
        if mode not in HA_TO_FRIGIDAIRE_MODE:
            return

        # Turn on if not currently on.
        if (
            self._details.for_code(frigidaire.HaclCode.APPLIANCE_STATE).number_value
            == 0
        ):
            self.turn_on()

        self._client.execute_action(
            self._appliance, frigidaire.Action.set_mode(HA_TO_FRIGIDAIRE_MODE[mode])
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
                self._details.for_code(
                    frigidaire.HaclCode.CONNECTIVITY_STATE
                ).string_value
                == frigidaire.ConnectivityState.CONNECTED
            )
