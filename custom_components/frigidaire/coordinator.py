"""DataUpdateCoordinator for the frigidaire integration."""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

import frigidaire

from .compressor import CompressorEstimator
from .const import (
    CONF_COMPRESSOR_ESTIMATE,
    CONF_COMPRESSOR_OFF_DELAY,
    CONF_COOL_HYSTERESIS,
    DEFAULT_COMPRESSOR_OFF_DELAY,
    DEFAULT_COOL_HYSTERESIS,
)

_LOGGER = logging.getLogger(__name__)

# A single account-level poll replaces the old per-appliance polling, which had
# itself replaced per-entity polling: the whole account is fetched once per cycle
# and each appliance's record is pushed to its own coordinator, so an account with
# N appliances makes one request per cycle instead of N identical ones. On failure
# we back off exponentially up to MAX_INTERVAL so that when Frigidaire's auth
# servers are flaky (upstream Gigya/token outages) we stop hammering them —
# repeated re-auth is what trips Frigidaire's active-session cap (cas_3403).
BASE_INTERVAL = timedelta(seconds=30)
MAX_INTERVAL = timedelta(minutes=10)
FAN_SPEED_STATE_KEY = "fanSpeedState"
# Reported by the cloud as a sibling of "properties", so it never appears in the
# properties.reported dict that becomes coordinator.data.
CONNECTION_STATE_KEY = "connectionState"
CONNECTED_STATE = "CONNECTED"


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.upper()
    return value


def _coerce_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _error_context(err: Exception) -> str:
    """Return " (status=…, error=…)" when the library attached structured error info.

    The library redacts response bodies from exception messages, so without this the
    log line for a 429 or a cas_3403 session cap is indistinguishable from any other
    failure.
    """
    parts = []
    status = getattr(err, "status_code", None)
    if status is not None:
        parts.append(f"status={status}")
    code = getattr(err, "error_code", None)
    if code:
        parts.append(f"error={code}")
    return f" ({', '.join(parts)})" if parts else ""


class FrigidaireAccountCoordinator(DataUpdateCoordinator[dict[str, dict]]):
    """Polls the whole account in one request and pushes each record to its appliance coordinator.

    Before this, every appliance coordinator fetched the full appliance list on its own
    30-second timer, so N appliances meant N identical requests per cycle and N
    independent re-authentications when one failed, which is what tripped Frigidaire's
    session cap (issue #146). Now only this coordinator polls; the per-appliance
    coordinators receive their slice through push_to_appliances() and fetch on their
    own only when an entity asks for an immediate refresh after a command.
    """

    def __init__(self, hass: HomeAssistant, client: frigidaire.Frigidaire) -> None:
        super().__init__(hass, _LOGGER, name="frigidaire account", update_interval=BASE_INTERVAL)
        self.client = client
        self.appliance_coordinators: list[FrigidaireApplianceCoordinator] = []
        self._failure_count = 0

    async def _async_update_data(self) -> dict[str, dict]:
        """Fetch every appliance record, backing off on repeated failures."""
        try:
            records = await self.hass.async_add_executor_job(self.client.get_appliances_raw)
        except (frigidaire.FrigidaireException, ConnectionError) as err:
            self._failure_count += 1
            # 30s, 60s, 120s, 240s … capped at MAX_INTERVAL.
            # The exponent is capped so timedelta can't overflow after a very long outage;
            # anything past a few doublings is clamped to MAX_INTERVAL anyway.
            backoff = BASE_INTERVAL * (2 ** min(self._failure_count - 1, 20))
            self.update_interval = min(backoff, MAX_INTERVAL)
            raise UpdateFailed(f"Error communicating with Frigidaire{_error_context(err)}: {err}") from err

        # Recovered — resume the normal polling cadence.
        if self._failure_count:
            self._failure_count = 0
            self.update_interval = BASE_INTERVAL
        # Indexed with .get(): a record without an applianceId would otherwise raise
        # KeyError out of the try above, skipping the backoff entirely.
        return {appliance_id: record for record in records if (appliance_id := record.get("applianceId"))}

    @callback
    def push_to_appliances(self) -> None:
        """Listener: hand each appliance coordinator its record, or the shared failure."""
        for coordinator in self.appliance_coordinators:
            # The coordinator that asked for this refresh applies the record itself (and
            # raises on failure) once the await returns. Pushing to it here would call
            # async_set_updated_data mid-refresh, whose _debounced_refresh.async_cancel()
            # silently drops any refresh queued after that refresh began — a script that
            # sets hvac_mode and then temperature would lose the second command's refresh.
            if coordinator.refreshing_self:
                continue
            if not self.last_update_success:
                coordinator.async_set_update_error(self.last_exception or UpdateFailed("Account fetch failed"))
                continue
            record = (self.data or {}).get(coordinator.appliance.appliance_id)
            if record is None:
                coordinator.async_set_update_error(
                    UpdateFailed(f"Appliance {coordinator.appliance.nickname} not found in list of appliances")
                )
                continue
            try:
                data = coordinator.apply_record(record)
            except Exception as err:
                # Deliberately broad: one malformed record must never abort the loop and
                # leave the remaining appliances without their update.
                coordinator.async_set_update_error(
                    err
                    if isinstance(err, UpdateFailed)
                    else UpdateFailed(f"Unexpected error applying record for {coordinator.appliance.nickname}: {err}")
                )
                continue
            coordinator.async_set_updated_data(data)


class FrigidaireApplianceCoordinator(DataUpdateCoordinator[dict]):
    """Shares one appliance's slice of the account fetch with every entity for that device."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: frigidaire.Frigidaire,
        appliance: frigidaire.Appliance,
        account: FrigidaireAccountCoordinator,
        options: Mapping[str, Any] | None = None,
    ) -> None:
        # No update_interval: the account coordinator is the only thing that polls.
        super().__init__(
            hass,
            _LOGGER,
            name=f"frigidaire {appliance.nickname}",
            update_interval=None,
        )
        self.client = client
        self.appliance = appliance
        self.account = account
        # True only while this coordinator is inside its own _async_update_data; the
        # account's push skips it so it is not updated mid-refresh. See push_to_appliances.
        self.refreshing_self = False
        account.appliance_coordinators.append(self)
        options = options or {}
        self._compressor_estimator = (
            CompressorEstimator(
                hysteresis=_coerce_float(options.get(CONF_COOL_HYSTERESIS), DEFAULT_COOL_HYSTERESIS),
                off_delay=_coerce_float(options.get(CONF_COMPRESSOR_OFF_DELAY), DEFAULT_COMPRESSOR_OFF_DELAY),
            )
            if appliance.destination == frigidaire.Destination.AIR_CONDITIONER
            and options.get(CONF_COMPRESSOR_ESTIMATE, False)
            else None
        )
        self._compressor_running: bool | None = None
        self._connection_state: str | None = None

    @property
    def compressor_estimation_enabled(self) -> bool:
        """Return whether temperature-based compressor estimation is enabled."""
        return self._compressor_estimator is not None

    @property
    def compressor_running(self) -> bool | None:
        """Return the shared temperature-based compressor estimate."""
        return self._compressor_running

    @property
    def connection_state(self) -> str | None:
        """Return the appliance's normalized cloud connection state, if reported."""
        return self._connection_state

    @property
    def is_connected(self) -> bool | None:
        """Return whether the appliance is currently reachable by the cloud.

        None when the appliance does not report a connection state at all, so callers can
        omit the entity rather than inventing a value.
        """
        if self._connection_state is None:
            return None
        return self._connection_state == CONNECTED_STATE

    @property
    def reported_fan_speed(self) -> str | None:
        """Return the reported fan-speed state without implying motion."""
        raw = (self.data or {}).get(FAN_SPEED_STATE_KEY)
        if raw is None:
            return None
        return {
            frigidaire.FanSpeed.AUTO: "auto",
            frigidaire.FanSpeed.LOW: "low",
            frigidaire.FanSpeed.MEDIUM: "medium",
            frigidaire.FanSpeed.HIGH: "high",
        }.get(_normalize(raw), str(raw).lower())

    def _update_compressor_estimate(self, details: dict) -> None:
        """Update the opt-in estimate from one coordinator response."""
        if self._compressor_estimator is None:
            return

        mode = _normalize(details.get(frigidaire.Detail.MODE))
        appliance_state = _normalize(details.get(frigidaire.Detail.APPLIANCE_STATE))
        if mode == frigidaire.Mode.OFF or (
            appliance_state is not None and appliance_state != frigidaire.ApplianceState.RUNNING
        ):
            self._compressor_running = self._compressor_estimator.force_off()
            return
        if mode == frigidaire.Mode.FAN:
            self._compressor_running = self._compressor_estimator.force_off()
            return
        if mode not in (frigidaire.Mode.COOL, frigidaire.Mode.ECO, frigidaire.Mode.AUTO, frigidaire.Mode.DRY):
            self._compressor_running = None
            return

        unit = _normalize(details.get(frigidaire.Detail.TEMPERATURE_REPRESENTATION))
        if unit == frigidaire.Unit.FAHRENHEIT:
            current = details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_F)
            target = details.get(frigidaire.Detail.TARGET_TEMPERATURE_F)
        elif unit == frigidaire.Unit.CELSIUS:
            current = details.get(frigidaire.Detail.AMBIENT_TEMPERATURE_C)
            target = details.get(frigidaire.Detail.TARGET_TEMPERATURE_C)
        else:
            self._compressor_running = None
            return

        self._compressor_running = self._compressor_estimator.update(current, target, now=time.monotonic())

    def apply_record(self, record: dict) -> dict:
        """Derive this appliance's coordinator data from its raw account record.

        The whole record is used rather than just properties.reported: connectionState
        is a sibling of "properties" and is dropped by get_appliance_details().
        """
        self._connection_state = _normalize(record.get(CONNECTION_STATE_KEY))
        # coordinator.data stays exactly the properties.reported dict that every platform
        # already indexes with frigidaire.Detail keys.
        reported = (record.get("properties") or {}).get("reported")
        if not isinstance(reported, dict) or not reported:
            raise UpdateFailed(f"Frigidaire returned no reported properties for {self.appliance.nickname}")
        self._update_compressor_estimate(reported)
        return reported

    async def _async_update_data(self) -> dict:
        """Explicit refresh (an entity's force_refresh after a command): fetch the account now."""
        self.refreshing_self = True
        try:
            await self.account.async_refresh()
        finally:
            self.refreshing_self = False
        if not self.account.last_update_success:
            raise UpdateFailed(str(self.account.last_exception))
        record = (self.account.data or {}).get(self.appliance.appliance_id)
        if record is None:
            raise UpdateFailed(f"Appliance {self.appliance.nickname} not found in list of appliances")
        return self.apply_record(record)
