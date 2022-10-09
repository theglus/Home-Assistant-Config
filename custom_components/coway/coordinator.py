"""DataUpdateCoordinator for the Coway integration."""
from __future__ import annotations

from datetime import timedelta

from cowayaio.exceptions import AuthError, CowayError
from cowayaio.purifier_model import PurifierData

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER
from .util import COWAY_CLIENT


class CowayDataUpdateCoordinator(DataUpdateCoordinator):
    """Coway Data Update Coordinator."""

    data: PurifierData

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the Coway coordinator."""

        COWAY_CLIENT.username = entry.data[CONF_USERNAME]
        COWAY_CLIENT.password = entry.data[CONF_PASSWORD]
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
        except CowayError as error:
            raise UpdateFailed(error) from error

        if not data.purifiers:
            raise UpdateFailed("No Purifiers found")

        return data
