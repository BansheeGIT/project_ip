from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraSnapshot:
    lane: str
    timestamp: float
    vehicle_count: int
    stopped_vehicle_count: int
    pedestrian_count: int
    emergency_vehicle_count: int
    emergency_siren_count: int


@dataclass(frozen=True)
class SignalCommand:
    timestamp: float
    mode: str
    phase: str
    reason: str


def validate_camera_payload(payload: dict) -> CameraSnapshot:
    required = {
        "lane",
        "timestamp",
        "vehicle_count",
        "stopped_vehicle_count",
        "pedestrian_count",
        "emergency_vehicle_count",
        "emergency_siren_count",
    }
    missing = required.difference(payload)
    if missing:
        raise ValueError(f"Camera payload missing fields: {sorted(missing)}")

    lane = str(payload["lane"]).upper()
    return CameraSnapshot(
        lane=lane,
        timestamp=float(payload["timestamp"]),
        vehicle_count=max(0, int(payload["vehicle_count"])),
        stopped_vehicle_count=max(0, int(payload["stopped_vehicle_count"])),
        pedestrian_count=max(0, int(payload["pedestrian_count"])),
        emergency_vehicle_count=max(0, int(payload["emergency_vehicle_count"])),
        emergency_siren_count=max(0, int(payload["emergency_siren_count"])),
    )


def validate_signal_payload(payload: dict) -> SignalCommand:
    required = {"timestamp", "mode", "phase", "reason"}
    missing = required.difference(payload)
    if missing:
        raise ValueError(f"Signal payload missing fields: {sorted(missing)}")

    return SignalCommand(
        timestamp=float(payload["timestamp"]),
        mode=str(payload["mode"]),
        phase=str(payload["phase"]),
        reason=str(payload["reason"]),
    )
