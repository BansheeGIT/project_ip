from __future__ import annotations

from dataclasses import dataclass

LANES = ("N", "S", "E", "W")


@dataclass(frozen=True)
class TopicRegistry:
    """Topic builder with run-specific prefix to avoid collisions."""

    prefix: str = "traffic"

    def _topic(self, suffix: str) -> str:
        base = self.prefix.strip("/")
        tail = suffix.strip("/")
        return f"{base}/{tail}"

    def camera_snapshot(self, lane: str) -> str:
        lane = lane.upper()
        if lane not in LANES:
            raise ValueError(f"Unsupported lane: {lane}")
        return self._topic(f"camera/{lane}/snapshot")

    @property
    def signal_command(self) -> str:
        return self._topic("signal/command")

    @property
    def signal_applied(self) -> str:
        return self._topic("signal/applied")


DEFAULT_TOPICS = TopicRegistry()


def camera_snapshot_topic(lane: str) -> str:
    return DEFAULT_TOPICS.camera_snapshot(lane)


def signal_command_topic() -> str:
    return DEFAULT_TOPICS.signal_command


def signal_applied_topic() -> str:
    return DEFAULT_TOPICS.signal_applied
