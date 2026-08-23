"""Parsing helpers for Frigidaire appliance diagnostics."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

AIR_FILTER_LIFETIME_KEY = "airFilterLifeTime"
GOOD_FILTER_STATE = "GOOD"


def normalize_alerts(value: Any) -> list[str] | None:
    """Return alert codes from either supported API response format."""
    if value is None:
        return None

    raw_alerts = value if isinstance(value, list | tuple | set | frozenset) else [value]
    alerts: list[str] = []
    for alert in raw_alerts:
        code = alert.get("code") if isinstance(alert, Mapping) else alert
        if code is not None:
            alerts.append(str(code).upper())
    return alerts


def normalize_filter_state(value: Any) -> str | None:
    """Return a normalized filter-state string."""
    if value is None:
        return None
    return str(value).upper()


def filter_needs_attention(value: Any) -> bool | None:
    """Return whether a reported filter state requires attention."""
    state = normalize_filter_state(value)
    return None if state is None else state != GOOD_FILTER_STATE


def filter_runtime_seconds(value: Any) -> float | None:
    """Return valid cumulative filter-runtime seconds."""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(seconds) or seconds < 0:
        return None
    return seconds
