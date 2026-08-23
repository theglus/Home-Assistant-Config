"""DataUpdateCoordinator for the frigidaire integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

import frigidaire

_LOGGER = logging.getLogger(__name__)

# A single shared poll per appliance replaces the old per-entity polling: a
# device that exposes several entities (climate/switch/number/binary_sensor/…)
# now hits the API once per cycle instead of once per entity. On failure we back
# off exponentially up to MAX_INTERVAL so that when Frigidaire's auth servers are
# flaky (upstream Gigya/token outages) we stop hammering them — repeated re-auth
# is what trips Frigidaire's active-session cap (cas_3403).
BASE_INTERVAL = timedelta(seconds=30)
MAX_INTERVAL = timedelta(minutes=10)
FAN_SPEED_STATE_KEY = "fanSpeedState"


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.upper()
    return value


class FrigidaireApplianceCoordinator(DataUpdateCoordinator[dict]):
    """Polls a single Frigidaire appliance and shares its details with every entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: frigidaire.Frigidaire,
        appliance: frigidaire.Appliance,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"frigidaire {appliance.nickname}",
            update_interval=BASE_INTERVAL,
        )
        self.client = client
        self.appliance = appliance
        self._failure_count = 0

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

    async def _async_update_data(self) -> dict:
        """Fetch the latest appliance details, backing off on repeated failures."""
        try:
            details = await self.hass.async_add_executor_job(self.client.get_appliance_details, self.appliance)
        except (frigidaire.FrigidaireException, ConnectionError) as err:
            self._failure_count += 1
            # 30s, 60s, 120s, 240s … capped at MAX_INTERVAL.
            backoff = BASE_INTERVAL * (2 ** (self._failure_count - 1))
            self.update_interval = min(backoff, MAX_INTERVAL)
            raise UpdateFailed(f"Error communicating with Frigidaire: {err}") from err

        # Recovered — resume the normal polling cadence.
        if self._failure_count:
            self._failure_count = 0
            self.update_interval = BASE_INTERVAL
        return details
