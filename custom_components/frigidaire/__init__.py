"""The frigidaire integration."""
from __future__ import annotations

import os
import traceback

import frigidaire

from homeassistant import data_entry_flow
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .config_flow import load_auth, save_auth, AUTH_FILE
from .const import DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up frigidaire from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    def setup(username: str, password: str) -> None:
        auth_path: str = os.path.join(hass.config.path(), AUTH_FILE)

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

            hass.data[DOMAIN][entry.entry_id] = client
        except ConnectionError as err:
            raise ConfigEntryNotReady("Cannot connect to Frigidaire") from err
        except frigidaire.FrigidaireException as err:
            # Handle frigidaire 429 gracefully
            if "cas_3403" in traceback.format_exc():
                raise data_entry_flow.AbortFlow("You have exceeded Frigidaire's maximum number of active sessions. Please log out of another device or wait until an existing session expires.") from err
            raise data_entry_flow.AbortFlow("Frigidaire backend exception") from err

    await hass.async_add_executor_job(
        setup, entry.data["username"], entry.data["password"]
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
