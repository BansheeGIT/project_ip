from __future__ import annotations

from dataclasses import dataclass

LANES = ("N", "S", "E", "W")

<<<<<<< HEAD

@dataclass(frozen=True)
class TopicRegistry:
    """Topic builder with run-specific prefix to avoid collisions."""

    prefix: str = "traffic"

=======
@dataclass(frozen=True)
# Topic names for one run live here.
class TopicRegistry:
    """Topic builder with run-specific prefix to avoid collisions."""
    # One prefix lets parallel runs stay out of each other's way.

    prefix: str = "traffic"

    # Join the run prefix with one topic suffix.
>>>>>>> master
    def _topic(self, suffix: str) -> str:
        base = self.prefix.strip("/")
        tail = suffix.strip("/")
        return f"{base}/{tail}"

<<<<<<< HEAD
    def camera_snapshot(self, lane: str) -> str:
=======
    # Camera topic for one lane.
    def camera_snapshot(self, lane: str) -> str:
        # Each lane gets its own camera topic.
>>>>>>> master
        lane = lane.upper()
        if lane not in LANES:
            raise ValueError(f"Unsupported lane: {lane}")
        return self._topic(f"camera/{lane}/snapshot")

    @property
<<<<<<< HEAD
=======
    # Topic used for controller commands.
>>>>>>> master
    def signal_command(self) -> str:
        return self._topic("signal/command")

    @property
<<<<<<< HEAD
=======
    # Topic sent after a phase is applied.
>>>>>>> master
    def signal_applied(self) -> str:
        return self._topic("signal/applied")


DEFAULT_TOPICS = TopicRegistry()


<<<<<<< HEAD
=======
# Default camera topic for one lane.
>>>>>>> master
def camera_snapshot_topic(lane: str) -> str:
    return DEFAULT_TOPICS.camera_snapshot(lane)


<<<<<<< HEAD
=======
# Default topic for controller commands.
>>>>>>> master
def signal_command_topic() -> str:
    return DEFAULT_TOPICS.signal_command


<<<<<<< HEAD
=======
# Default topic for applied phase events.
>>>>>>> master
def signal_applied_topic() -> str:
    return DEFAULT_TOPICS.signal_applied
