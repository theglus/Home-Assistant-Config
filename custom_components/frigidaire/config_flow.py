"""Config flow for frigidaire integration."""

from __future__ import annotations

import logging
import os
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

import frigidaire

from .auth_store import AUTH_FILE, load_auth, save_auth
from .const import (
    BINARY_SENSOR_OPTIONS,
    DOMAIN,
    SENSOR_OPTIONS,
    SWITCH_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({"username": str, "password": str})

ALL_OPTIONS = {**SWITCH_OPTIONS, **BINARY_SENSOR_OPTIONS, **SENSOR_OPTIONS}


def _device_schema(current: dict) -> vol.Schema:
    return vol.Schema({vol.Optional(key, default=current.get(key, False)): bool for key in ALL_OPTIONS})


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> list[frigidaire.Appliance]:
    """Validate credentials and return list of appliances."""

    def setup(username: str, password: str) -> list[frigidaire.Appliance]:
        auth_path = os.path.join(hass.config.path(), AUTH_FILE)

        try:
            session_key, regional_base_url = load_auth(auth_path)
            client = frigidaire.Frigidaire(
                username=username,
                password=password,
                timeout=60,
                session_key=session_key,
                regional_base_url=regional_base_url,
            )
            save_auth(auth_path, client.session_key, client.regional_base_url)

            return client.get_appliances()
        except frigidaire.FrigidaireException as err:
            if "Failed to authenticate" in str(err):
                raise InvalidAuth from err

            raise CannotConnect from err

    appliances = await hass.async_add_executor_job(setup, data["username"], data["password"])

    if len(appliances) == 0:
        raise NoAppliances

    return appliances


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for frigidaire."""

    VERSION = 1

    def __init__(self) -> None:
        self._user_input: dict[str, Any] = {}
        self._appliances: list[frigidaire.Appliance] = []
        self._pending_appliances: list[frigidaire.Appliance] = []
        self._options: dict[str, dict[str, bool]] = {}

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        errors = {}

        try:
            appliances = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except NoAppliances:
            errors["base"] = "no_appliances"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(user_input["username"].lower())
            self._abort_if_unique_id_configured()
            self._user_input = user_input
            self._appliances = appliances
            self._pending_appliances = list(appliances)
            return await self._async_next_device_step()

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

    async def _async_next_device_step(self) -> FlowResult:
        if not self._pending_appliances:
            return self.async_create_entry(title="Frigidaire", data=self._user_input, options=self._options)
        return await self.async_step_device()

    async def async_step_device(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show switch checkboxes for the current appliance in the queue."""
        appliance = self._pending_appliances[0]

        if user_input is not None:
            self._options[appliance.appliance_id] = user_input
            self._pending_appliances.pop(0)
            return await self._async_next_device_step()

        schema = _device_schema({})
        return self.async_show_form(
            step_id="device",
            data_schema=schema,
            description_placeholders={"device_name": appliance.nickname},
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for the frigidaire integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry_id = config_entry.entry_id
        self._appliances: list[frigidaire.Appliance] = []
        self._pending_appliances: list[frigidaire.Appliance] = []
        self._options: dict[str, dict[str, bool]] = {}

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Load appliances then start per-device steps."""
        entry = self.hass.config_entries.async_get_entry(self._entry_id)
        self._appliances = self.hass.data[DOMAIN][self._entry_id]["appliances"]
        self._pending_appliances = list(self._appliances)
        self._options = dict(entry.options)
        return await self._async_next_device_step()

    async def _async_next_device_step(self) -> FlowResult:
        if not self._pending_appliances:
            return self.async_create_entry(title="", data=self._options)
        return await self.async_step_device()

    async def async_step_device(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show switch checkboxes for the current appliance in the queue."""
        appliance = self._pending_appliances[0]
        current = self._options.get(appliance.appliance_id, {})

        if user_input is not None:
            self._options[appliance.appliance_id] = {**current, **user_input}
            self._pending_appliances.pop(0)
            return await self._async_next_device_step()

        schema = _device_schema(current)
        return self.async_show_form(
            step_id="device",
            data_schema=schema,
            description_placeholders={"device_name": appliance.nickname},
        )


class NoAppliances(HomeAssistantError):
    """Error to indicate there are no appliances."""


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
