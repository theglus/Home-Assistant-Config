"""Utilities for Coway Integration"""
from __future__ import annotations

import async_timeout

from cowayaio import CowayClient
from cowayaio.exceptions import AuthError, CowayError

from homeassistant.core import async_get_hass, HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER, COWAY_ERRORS, TIMEOUT


# Create a single instance of CowayClient that is
# used during the initial config flow and afterwards by
# the update coordinator. The creation of two CowayClient objects
# during initial integration configuration caused errors as Coway's
# servers don't like rapid back-to-back logins.
COWAY_CLIENT = CowayClient(
    "",
    "",
    session=async_get_clientsession(async_get_hass()),
    timeout=TIMEOUT
)


async def async_validate_api(username: str, password: str) -> None:
    """Get data from API."""

    COWAY_CLIENT.username = username
    COWAY_CLIENT.password = password
    client = COWAY_CLIENT

    try:
        async with async_timeout.timeout(TIMEOUT):
            coway_query = await client.async_get_purifiers()
    except AuthError as err:
        LOGGER.error(f'Could not authenticate on Coway servers: {err}')
        raise AuthError from err
    except COWAY_ERRORS as err:
        LOGGER.error(f'Failed to get information from Coway servers: {err}')
        raise ConnectionError from err
    purifiers: list = coway_query['body']['deviceInfos']
    if not purifiers:
        LOGGER.error("Could not retrieve any purifiers from Coway servers")
        raise NoPurifiersError


class NoPurifiersError(Exception):
    """No Purifiers from Coway API."""
