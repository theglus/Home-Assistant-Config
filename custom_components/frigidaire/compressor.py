"""Temperature-based compressor state estimation."""

from __future__ import annotations


def estimate_compressor_running(
    current: float | None,
    target: float | None,
    *,
    hysteresis: float,
    off_delay: float,
    previous: bool,
    satisfied_since: float | None,
    now: float,
) -> tuple[bool, float | None]:
    """Return the next compressor estimate and satisfied-band timestamp."""
    if current is None or target is None:
        return previous, None

    if current > target + hysteresis:
        return True, None

    if current <= target - hysteresis:
        satisfied_since = now if satisfied_since is None else satisfied_since
        if now - satisfied_since >= off_delay:
            return False, satisfied_since
        return previous, satisfied_since

    return previous, None


class CompressorEstimator:
    """Maintain one compressor estimate across coordinator refreshes."""

    def __init__(self, *, hysteresis: float, off_delay: float) -> None:
        self.hysteresis = hysteresis
        self.off_delay = off_delay
        self.running = True
        self.satisfied_since: float | None = None

    def force_off(self) -> bool:
        """Reset the estimate when operating state proves the compressor is off."""
        self.running = False
        self.satisfied_since = None
        return self.running

    def update(self, current: float | None, target: float | None, *, now: float) -> bool:
        """Update and return the shared estimate."""
        self.running, self.satisfied_since = estimate_compressor_running(
            current,
            target,
            hysteresis=self.hysteresis,
            off_delay=self.off_delay,
            previous=self.running,
            satisfied_since=self.satisfied_since,
            now=now,
        )
        return self.running
