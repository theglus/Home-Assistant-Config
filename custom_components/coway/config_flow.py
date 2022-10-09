"""Config Flow for Coway integration."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cowayaio.exceptions import AuthError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN
from .util import async_validate_api, NoPurifiersError


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class CowayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coway integration."""

    VERSION = 2

    entry: config_entries.ConfigEntry | None

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Handle re-authentication with Coway."""

        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm re-authentication with Coway."""

        errors: dict[str, str] = {}

        if user_input:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            try:
                await async_validate_api(username, password)
            except AuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPurifiersError:
                errors["base"] = "no_purifiers"
            else:
                assert self.entry is not None

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        **self.entry.data,
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                )
                await self.hass.config_entries.async_reload(self.entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            try:
                await async_validate_api(username, password)
            except AuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPurifiersError:
                errors["base"] = "no_purifiers"
            else:
                await self.async_set_unique_id(username)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
