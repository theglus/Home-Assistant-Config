"""The frigidaire integration."""

from __future__ import annotations

import threading

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

import frigidaire

from .auth_store import load_auth, per_entry_auth_path, resolve_initial_auth_path, save_auth
from .const import DOMAIN, PLATFORMS
from .coordinator import FrigidaireApplianceCoordinator

# Guards writes to an entry's auth file: the client may re-authenticate from
# multiple entity worker threads, so its persist callback can fire concurrently.
_AUTH_WRITE_LOCK = threading.Lock()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up frigidaire from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    def setup(username: str, password: str) -> tuple[frigidaire.Frigidaire, list[frigidaire.Appliance]]:
        # Each entry persists to its own file so multiple accounts don't clobber
        # each other's session keys (which would force re-auth and trip cas_3403).
        auth_path: str = per_entry_auth_path(hass.config.path(), entry.entry_id)

        def persist_session_key(session_key: str, regional_base_url: str | None) -> None:
            # Called whenever the client mints a new session key, including on
            # runtime re-authentication. Persisting it means a still-valid token
            # survives restarts instead of being abandoned — abandoned sessions
            # linger server-side and trip Frigidaire's active-session cap (cas_3403).
            with _AUTH_WRITE_LOCK:
                save_auth(auth_path, session_key, regional_base_url)

        try:
            # Fall back to the legacy shared file on first run so an existing
            # cached key is migrated instead of forcing a re-auth.
            session_key, regional_base_url = load_auth(resolve_initial_auth_path(hass.config.path(), entry.entry_id))
            client = frigidaire.Frigidaire(
                username=username,
                password=password,
                timeout=60,
                session_key=session_key,
                regional_base_url=regional_base_url,
                on_session_key_update=persist_session_key,
            )
            persist_session_key(client.session_key, client.regional_base_url)

            # Fetch the appliance list once and share it across every platform
            # (climate, humidifier, number, switch) instead of each calling the
            # API separately.
            appliances = client.get_appliances()
            return client, appliances
        except ConnectionError as err:
            raise ConfigEntryNotReady("Cannot connect to Frigidaire") from err
        except frigidaire.FrigidaireException as err:
            # Handle frigidaire's active-session cap (cas_3403) gracefully. Raise
            # ConfigEntryNotReady so HA retries setup automatically rather than
            # aborting — AbortFlow is only valid inside a config flow, not here.
            if "cas_3403" in str(err):
                raise ConfigEntryNotReady("Rate limited by Frigidaire. Will retry automatically.") from err
            raise ConfigEntryNotReady(f"Frigidaire error during setup: {err}") from err

    client, appliances = await hass.async_add_executor_job(setup, entry.data["username"], entry.data["password"])

    # One coordinator per appliance consolidates polling: every entity for a
    # device reads from a single shared fetch instead of hitting the API on its
    # own schedule. A first refresh here primes the data; individual failures are
    # tolerated (the coordinator backs off and retries) so one flaky appliance
    # doesn't block the whole entry from loading.
    coordinators: dict[str, FrigidaireApplianceCoordinator] = {}
    for appliance in appliances:
        coordinator = FrigidaireApplianceCoordinator(hass, client, appliance)
        await coordinator.async_refresh()
        coordinators[appliance.appliance_id] = coordinator

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "appliances": appliances,
        "coordinators": coordinators,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry when options change so switch selection takes effect."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
