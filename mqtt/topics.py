"""MQTT topic names used by in-process broker simulation."""

CAMERA_SNAPSHOT_FMT = "traffic/camera/{lane}/snapshot"
SIGNAL_COMMAND = "traffic/signal/command"
SIGNAL_APPLIED = "traffic/signal/applied"
MONITOR_EVENT = "traffic/monitor/event"

LANES = ("N", "S", "E", "W")


def camera_snapshot_topic(lane: str) -> str:
    lane = lane.upper()
    if lane not in LANES:
        raise ValueError(f"Unsupported lane: {lane}")
    return CAMERA_SNAPSHOT_FMT.format(lane=lane)
