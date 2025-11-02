"""Config flow for frigidaire integration."""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

import frigidaire
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({"username": str, "password": str})

AUTH_FILE = 'frigidaire.json'


def load_auth(auth_path: str) -> tuple[Optional[str], Optional[str]]:
    if not os.path.exists(auth_path):
        with open(auth_path, 'w'):
            pass

    if os.path.getsize(auth_path) > 0:
        with open(auth_path, 'r') as f:
            obj: dict = json.loads(f.read())
            return obj.get('session_key'), obj.get('regional_base_url')
    return None, None


def save_auth(auth_path: str, session_key: str, regional_base_url: str) -> None:
    with open(auth_path, 'w') as f:
        json.dump({'session_key': session_key, 'regional_base_url': regional_base_url}, f, ensure_ascii=False, indent=4)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]):
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    def setup(username: str, password: str) -> list[frigidaire.Appliance]:
        auth_path = os.path.join(hass.config.path(), AUTH_FILE)

        try:
            session_key, regional_base_url = load_auth(auth_path)
            client = frigidaire.Frigidaire(
                username=username,
                password=password,
                timeout=60,
                session_key=session_key,
                regional_base_url=regional_base_url
            )
            save_auth(auth_path, client.session_key, client.regional_base_url)

            return client.get_appliances()
        except frigidaire.FrigidaireException as err:
            if "Failed to authenticate" in str(err):
                raise InvalidAuth from err

            raise CannotConnect from err

    appliances = await hass.async_add_executor_job(
        setup, data["username"], data["password"]
    )

    if len(appliances) == 0:
        raise NoAppliances

    # Validation Succeeded
    return True


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for frigidaire."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            await validate_input(self.hass, user_input)
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
            return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class NoAppliances(HomeAssistantError):
    """Error to indicate there are no appliances."""


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
