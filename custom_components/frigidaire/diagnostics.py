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


def bucket_is_full(
    alerts: list[str] | None,
    water_bucket_level: Any,
    water_tank_full: Any,
) -> bool | None:
    """Return whether the water bucket is full, or None when unreported.

    Different dehumidifier models report the bucket through different signals,
    so all three are checked: a BUCKET_FULL alert code, waterBucketLevel == 1,
    and waterTankFull. ``alerts`` must already be normalized (see
    ``normalize_alerts``). Returns None when the appliance reports none of the
    signals, letting callers distinguish "empty" from "not supported by this
    model".
    """
    if alerts is None and water_bucket_level is None and water_tank_full is None:
        return None
    if alerts is not None and "BUCKET_FULL" in alerts:
        return True
    if water_bucket_level == 1:
        return True
    tank = water_tank_full.upper() if isinstance(water_tank_full, str) else water_tank_full
    return tank in ("YES", True)


def filter_runtime_seconds(value: Any) -> float | None:
    """Return valid cumulative filter-runtime seconds."""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(seconds) or seconds < 0:
        return None
    return seconds


def _finite_float(value: Any) -> float | None:
    """Coerce to a finite float, or None if the value is missing or unparseable."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def humidity_percent(value: Any) -> float | None:
    """Return a reported relative-humidity reading, or None if out of range."""
    humidity = _finite_float(value)
    if humidity is None or not 0 <= humidity <= 100:
        return None
    return humidity


def particulate_matter(value: Any) -> float | None:
    """Return a reported particulate concentration in ug/m3, or None if implausible."""
    concentration = _finite_float(value)
    if concentration is None or concentration < 0:
        return None
    return concentration


def network_rssi(value: Any) -> float | None:
    """Return the RSSI from a reported networkInterface mapping.

    Appliances report signal strength nested under networkInterface rather than as a
    top-level key, and omit the mapping entirely when they have never reported Wi-Fi
    telemetry. A non-negative RSSI is rejected: real dBm readings here are always negative,
    so 0 or above means the field is a placeholder rather than a measurement.
    """
    if not isinstance(value, Mapping):
        return None
    rssi = _finite_float(value.get("rssi"))
    if rssi is None or rssi >= 0:
        return None
    return rssi


def link_quality(value: Any) -> str | None:
    """Return the normalized link-quality indicator from a networkInterface mapping."""
    if not isinstance(value, Mapping):
        return None
    indicator = value.get("linkQualityIndicator")
    if indicator is None:
        return None
    return str(indicator).upper()
