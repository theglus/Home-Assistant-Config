"""Config flow of our component"""
import logging
import voluptuous as vol
from iocare.iocareapi import IOCareApi
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME
)
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

class IoCareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle our config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize IoCare configuration flow"""
        self.schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str
        })

        self._username = None
        self._password = None

    async def async_step_user(self, user_input=None):
        """Handle a flow start."""

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if not user_input:
            return self._show_form()

        self._username = user_input[CONF_USERNAME]
        self._password = user_input[CONF_PASSWORD]

        return await self._async_iocare_login()


    async def _async_iocare_login(self):

        errors = {}

        try:
            client = await self.hass.async_add_executor_job(IOCareApi, self._username, self._password)
            await self.hass.async_add_executor_job(client.check_access_token)

        except Exception:
            _LOGGER.error("Unable to connect to IoCare: Failed to Log In")
            errors = {"base": "auth_error"}

        if errors:
            return self._show_form(errors=errors)

        return await self._async_create_entry()

    async def _async_create_entry(self):
        """Create the config entry."""
        config_data = {
            CONF_USERNAME: self._username,
            CONF_PASSWORD: self._password,
        }

        return self.async_create_entry(title='Coway IoCare', data=config_data)

    @callback
    def _show_form(self, errors=None):
        """Show the form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=self.schema,
            errors=errors if errors else {},
        )
