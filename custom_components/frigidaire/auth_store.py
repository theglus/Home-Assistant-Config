"""Persistence for the Frigidaire session key.

Kept free of Home Assistant imports so the persistence + migration logic can be
unit-tested without a full HA environment.

Each config entry stores its session key in its own ``frigidaire-<entry_id>.json``
file. A single shared ``frigidaire.json`` was used previously; when multiple
accounts were configured they clobbered each other's keys, forcing repeated
re-authentication (each mints a new server-side session and trips Frigidaire's
active-session cap, cas_3403). The legacy file is migrated per entry on first run.
"""

from __future__ import annotations

import json
import os

# Legacy shared auth file, pre-dating per-entry scoping. Still written by the
# config flow (which runs before an entry_id exists) and migrated on first setup.
AUTH_FILE = "frigidaire.json"


def load_auth(auth_path: str) -> tuple[str | None, str | None]:
    if not os.path.exists(auth_path):
        with open(auth_path, "w"):
            pass

    if os.path.getsize(auth_path) > 0:
        with open(auth_path) as f:
            obj: dict = json.loads(f.read())
            return obj.get("session_key"), obj.get("regional_base_url")
    return None, None


def save_auth(auth_path: str, session_key: str, regional_base_url: str | None) -> None:
    with open(auth_path, "w") as f:
        json.dump({"session_key": session_key, "regional_base_url": regional_base_url}, f, ensure_ascii=False, indent=4)


def per_entry_auth_path(config_dir: str, entry_id: str) -> str:
    """The auth file dedicated to a single config entry."""
    return os.path.join(config_dir, f"frigidaire-{entry_id}.json")


def resolve_initial_auth_path(config_dir: str, entry_id: str) -> str:
    """Where to load an entry's initial session key from.

    Prefer the entry's own file. When it does not exist yet, fall back to the
    legacy shared file for a one-time migration so existing users keep their
    cached session key instead of re-authenticating. When neither exists, return
    the per-entry path (avoiding creation of a stray legacy file).
    """
    per_entry = per_entry_auth_path(config_dir, entry_id)
    legacy = os.path.join(config_dir, AUTH_FILE)
    if not os.path.exists(per_entry) and os.path.exists(legacy):
        return legacy
    return per_entry
