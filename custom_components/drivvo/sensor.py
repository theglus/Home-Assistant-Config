import hashlib
import json
import logging
import string
from collections import defaultdict
from datetime import datetime, timedelta

import homeassistant.helpers.config_validation as cv
import pytz
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_NAME,
    CONF_RESOURCES,
    STATE_UNKNOWN,
)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:gas-station"

SCAN_INTERVAL = timedelta(minutes=60)

ATTRIBUTION = "Data provided by drivvo api"

DOMAIN = "drivvo"

CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_MODEL = "model"
CONF_ID_VEHICLE = "id_vehicle"


LOGIN_BASE_URL = "https://api.drivvo.com/autenticacao/login"
BASE_URL = "https://api.drivvo.com/veiculo/{}/{}/web"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_MODEL): cv.string,
        vol.Required(CONF_ID_VEHICLE): cv.string,
    }
)


def get_data(email, password, id_vehicle):
    """Get The request from the api"""
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    url = BASE_URL.format(id_vehicle, "abastecimento")
    supplies = []

    response = requests.post(
        LOGIN_BASE_URL,
        data=dict(email=email, senha=password),
    )

    if response.ok:
        x_token = response.json().get("token")
        response = requests.get(url, headers={"x-token": x_token})
        if response.ok:
            supplies = response.json()
        else:
            _LOGGER.error("Cannot perform the request")
    else:
        _LOGGER.error("Cannot authentication")
    return supplies


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the currency sensor"""
    name = "{} - Refueling".format(config["model"])
    email = config["email"]
    password = config["password"]
    model = config["model"]
    id_vehicle = config["id_vehicle"]

    add_entities(
        [DrivvoSensor(hass, name, email, password, model, id_vehicle, SCAN_INTERVAL)],
        True,
    )


class DrivvoSensor(Entity):
    def __init__(self, hass, name, email, password, model, id_vehicle, interval):
        """Initialize sensor"""
        self._state = STATE_UNKNOWN
        self._hass = hass
        self._interval = interval
        self._email = email
        self._password = password
        self._model = model
        self._id_vehicle = id_vehicle
        self._name = name
        self._supplies = []

    @property
    def name(self):
        """Return the name sensor"""
        return self._name

    @property
    def icon(self):
        """Return the default icon"""
        return ICON

    @property
    def state(self):
        """Return number of refuelings."""
        return len(self._supplies)

    @property
    def supply(self):
        """Refueling."""
        return self._supplies[0]

    @property
    def total_payment(self):
        """Total cost of all refuelings."""
        total = 0
        for supply in self._supplies:
            total += supply.get("valor_total")
        return total

    @property
    def km_travel(self):
        """Miles travelled since last refueling."""
        km = 0
        odometers = [supply.get("odometro") for supply in self._supplies]
        if len(odometers) > 1:
            km = odometers[0] - odometers[1]
        return km

    @property
    def cheapest_gasoline_until_today(self):
        """Cheapest gas to date."""
        return min([supply.get("preco") for supply in self._supplies])

    @property
    def total_amount_of_supplies(self):
        """Total number of refuelings."""
        return len(self._supplies)

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "vehicle": self._model,
            "odometer": self.supply.get("odometro"),
            "gas_station": self.supply.get("posto_combustivel").get("nome"),
            "type_of_fuel": self.supply.get("combustivel"),
            "reason": self.supply.get("tipo_motivo"),
            "date_of_refueling": self.supply.get("data"),
            "volume_of_fuel": self.supply.get("tanques")[0].get("volume"),
            "cost_of_last_refueling": self.supply.get("valor_total"),
            "price_per_gallon": self.supply.get("preco"),
            "total_number_of_refuelings.": self.total_amount_of_supplies,
            "total_cost_of_all_refuelings": self.total_payment,
            "tank_full": "Yes" if self.supply.get("tanque_cheio") else "No",
            "miles_traveled_since_last_refueling": self.km_travel,
            "cheapest_gas_to_date": self.cheapest_gasoline_until_today,
        }

    def update(self):
        """Update the data by requesting the API."""
        self._supplies = get_data(self._email, self._password, self._id_vehicle)
