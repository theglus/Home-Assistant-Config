"""DataUpdateCoordinator for the Coway integration."""
from __future__ import annotations

from datetime import timedelta

from cowayaio.exceptions import AuthError, CowayError, PasswordExpired
from cowayaio.purifier_model import PurifierData

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER, SKIP_PASSWORD_CHANGE
from .util import COWAY_CLIENT


class CowayDataUpdateCoordinator(DataUpdateCoordinator):
    """Coway Data Update Coordinator."""

    data: PurifierData

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the Coway coordinator."""

        COWAY_CLIENT.username = entry.data[CONF_USERNAME]
        COWAY_CLIENT.password = entry.data[CONF_PASSWORD]
        COWAY_CLIENT.skip_password_change = entry.options[SKIP_PASSWORD_CHANGE]
        self.client = COWAY_CLIENT
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> PurifierData:
        """Fetch data from Coway."""

        try:
            data = await self.client.async_get_purifiers_data()
        except AuthError as error:
            raise ConfigEntryAuthFailed from error
        except PasswordExpired as error:
            raise ConfigEntryAuthFailed("Coway servers are requesting a password change as the password on this account hasn't been changed for 60 days or more. Either use the IoCare app to change your password or reauthenticate the integration with the skip password change option.")
        except CowayError as error:
            raise UpdateFailed(error) from error

        if not data.purifiers:
            raise UpdateFailed("No Purifiers found")

        return data
