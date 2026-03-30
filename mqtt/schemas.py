from __future__ import annotations

from dataclasses import dataclass

<<<<<<< HEAD

@dataclass(frozen=True)
class CameraSnapshot:
=======
@dataclass(frozen=True)
# Clean camera data ends up in this shape.
class CameraSnapshot:
    # The smart controller reads this cleaned data shape.
>>>>>>> master
    lane: str
    timestamp: float
    vehicle_count: int
    stopped_vehicle_count: int
    pedestrian_count: int
    emergency_vehicle_count: int
    emergency_siren_count: int


@dataclass(frozen=True)
<<<<<<< HEAD
=======
# Clean signal commands use this shape.
>>>>>>> master
class SignalCommand:
    timestamp: float
    mode: str
    phase: str
    reason: str


<<<<<<< HEAD
def validate_camera_payload(payload: dict) -> CameraSnapshot:
=======
# Clean and check one camera payload.
def validate_camera_payload(payload: dict) -> CameraSnapshot:
    # Check required fields first, then clean up types and negatives.
>>>>>>> master
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


<<<<<<< HEAD
def validate_signal_payload(payload: dict) -> SignalCommand:
=======
# Clean and check one signal payload.
def validate_signal_payload(payload: dict) -> SignalCommand:
    # Do the same validation for controller commands.
>>>>>>> master
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
