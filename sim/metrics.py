from __future__ import annotations

import csv
import datetime as dtm
import os
from typing import Tuple


def count_queues(world) -> Tuple[int, int]:
    """Count stopped vehicles per traffic axis (NS, EW)."""
    ns_dirs = {"N", "S"}
    ew_dirs = {"E", "W"}
    queue_ns = 0
    queue_ew = 0

    for vehicle in getattr(world, "vehicles", []):
        if not vehicle.get("is_stopped"):
            continue
        direction = vehicle.get("direction")
        if direction in ns_dirs:
            queue_ns += 1
        elif direction in ew_dirs:
            queue_ew += 1

    return queue_ns, queue_ew


class EfficiencyLogger:
    """Writes periodic simulation efficiency snapshots for mode comparison."""

    def __init__(self, mode: str, project_dir: str, interval_seconds: float = 5.0):
        self.mode = mode
        self.interval = max(1.0, float(interval_seconds))
        self.elapsed = 0.0
        self.total_time = 0.0
        timestamp = dtm.datetime.now().strftime("%Y%m%d_%H%M%S")
        logs_dir = os.path.join(project_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        self.filepath = os.path.join(logs_dir, f"efficiency_{mode}_{timestamp}.csv")
        self._file = open(self.filepath, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        self._writer.writerow(
            [
                "sim_time",
                "mode",
                "vehicles_alive",
                "pedestrians_alive",
                "vehicles_spawned",
                "vehicles_exited",
                "pedestrians_spawned",
                "pedestrians_exited",
                "vehicle_throughput_per_min",
                "pedestrian_throughput_per_min",
            ]
        )
        self._file.flush()

    def _throughput_per_min(self, count: int) -> float:
        if self.total_time <= 0.0:
            return 0.0
        return (count / self.total_time) * 60.0

    def step(self, world, dt: float, sim_time: float) -> None:
        self.total_time += float(dt)
        self.elapsed += float(dt)
        if self.elapsed < self.interval:
            return
        self.elapsed = 0.0

        vehicles_exited = int(world.stats.get("vehicles_exited", 0))
        pedestrians_exited = int(world.stats.get("pedestrians_exited", 0))
        vehicle_tpm = self._throughput_per_min(vehicles_exited)
        ped_tpm = self._throughput_per_min(pedestrians_exited)

        self._writer.writerow(
            [
                f"{sim_time:.2f}",
                self.mode,
                len(world.vehicles),
                len(world.pedestrians),
                int(world.stats.get("vehicles_spawned", 0)),
                vehicles_exited,
                int(world.stats.get("pedestrians_spawned", 0)),
                pedestrians_exited,
                f"{vehicle_tpm:.2f}",
                f"{ped_tpm:.2f}",
            ]
        )
        self._file.flush()

    def close(self) -> None:
        if not self._file.closed:
            self._file.close()
