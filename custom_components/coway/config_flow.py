"""Config Flow for Coway integration."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cowayaio.exceptions import AuthError, PasswordExpired
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN, SKIP_PASSWORD_CHANGE
from .util import async_validate_api, NoPurifiersError


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(SKIP_PASSWORD_CHANGE): bool,
    }
)


class CowayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coway integration."""

    VERSION = 3

    entry: config_entries.ConfigEntry | None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> CowayOptionsFlowHandler:
        """Get the options flow for this handler."""
        return CowayOptionsFlowHandler(config_entry)

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
            skip_password_change = user_input[SKIP_PASSWORD_CHANGE] if SKIP_PASSWORD_CHANGE in user_input else False
            try:
                session = async_create_clientsession(self.hass)
                await async_validate_api(self.hass, username, password, skip_password_change, session)
            except AuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPurifiersError:
                errors["base"] = "no_purifiers"
            except PasswordExpired:
                errors["base"] = "password_expired"
            else:
                assert self.entry is not None

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        **self.entry.data,
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                    options={SKIP_PASSWORD_CHANGE: skip_password_change},
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
            skip_password_change = user_input[SKIP_PASSWORD_CHANGE] if SKIP_PASSWORD_CHANGE in user_input else False
            try:
                session = async_create_clientsession(self.hass)
                await async_validate_api(self.hass, username, password, skip_password_change, session)
            except AuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPurifiersError:
                errors["base"] = "no_purifiers"
            except PasswordExpired:
                errors["base"] = "password_expired"
            else:
                await self.async_set_unique_id(username)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                    options={SKIP_PASSWORD_CHANGE: skip_password_change},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )


class CowayOptionsFlowHandler(config_entries.OptionsFlow):
    """ Handle Coway account options. """

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """ Manage options. """
        return await self.async_step_coway_account_settings()

    async def async_step_coway_account_settings(self, user_input=None):
        """Manage the Coway account options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Required(
                SKIP_PASSWORD_CHANGE,
                default=self.config_entry.options.get(
                    SKIP_PASSWORD_CHANGE, False
                ),
            ): bool,
        }

        return self.async_show_form(step_id="coway_account_settings", data_schema=vol.Schema(options))
