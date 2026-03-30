from __future__ import annotations

from dataclasses import dataclass

LANES = ("N", "S", "E", "W")

@dataclass(frozen=True)
# Topic names for one run live here.
class TopicRegistry:
    """Topic builder with run-specific prefix to avoid collisions."""
    # One prefix lets parallel runs stay out of each other's way.

    prefix: str = "traffic"

    # Join the run prefix with one topic suffix.
    def _topic(self, suffix: str) -> str:
        base = self.prefix.strip("/")
        tail = suffix.strip("/")
        return f"{base}/{tail}"

    # Camera topic for one lane.
    def camera_snapshot(self, lane: str) -> str:
        # Each lane gets its own camera topic.
        lane = lane.upper()
        if lane not in LANES:
            raise ValueError(f"Unsupported lane: {lane}")
        return self._topic(f"camera/{lane}/snapshot")

    @property
    # Topic used for controller commands.
    def signal_command(self) -> str:
        return self._topic("signal/command")

    @property
    # Topic sent after a phase is applied.
    def signal_applied(self) -> str:
        return self._topic("signal/applied")


DEFAULT_TOPICS = TopicRegistry()


# Default camera topic for one lane.
def camera_snapshot_topic(lane: str) -> str:
    return DEFAULT_TOPICS.camera_snapshot(lane)


# Default topic for controller commands.
def signal_command_topic() -> str:
    return DEFAULT_TOPICS.signal_command


# Default topic for applied phase events.
def signal_applied_topic() -> str:
    return DEFAULT_TOPICS.signal_applied
