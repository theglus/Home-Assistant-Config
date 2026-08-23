"""Shared helpers for the frigidaire integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar


def suggest_area(hass: HomeAssistant, nickname: str) -> str | None:
    """Return the longest area name that appears in the appliance nickname, or None."""
    registry = ar.async_get(hass)
    nickname_lower = nickname.lower()

    match = max(
        (area.name for area in registry.areas.values() if area.name.lower() in nickname_lower),
        key=len,
        default=None,
    )
    return match
