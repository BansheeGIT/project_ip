from __future__ import annotations

import csv
import datetime as dtm
import os
import uuid
from typing import Tuple

from db.metrics_store import SQLiteMetricsStore


<<<<<<< HEAD
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
=======
# Count stopped cars on each traffic axis.
def count_queues(world) -> Tuple[int, int]:
    # A queue here just means stopped cars grouped by axis.
    queue_ns = 0
    queue_ew = 0

    for v in world.vehicles:
        if not v.get("is_stopped"):
            continue
            
        direction = v.get("direction")
        if direction in ("N", "S"):
            queue_ns += 1
        elif direction in ("E", "W"):
>>>>>>> master
            queue_ew += 1

    return queue_ns, queue_ew


<<<<<<< HEAD
class EfficiencyLogger:
    """Writes periodic simulation efficiency snapshots for mode comparison."""

    def __init__(self, mode: str, project_dir: str, interval_seconds: float = 5.0):
        self.mode = mode
        self.run_id = f"{mode}-{uuid.uuid4().hex[:8]}"
        self.interval = max(1.0, float(interval_seconds))
        self.elapsed = 0.0
        self.total_time = 0.0
        timestamp = dtm.datetime.now().strftime("%Y%m%d_%H%M%S")
        logs_dir = os.path.join(project_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        self.filepath = os.path.join(logs_dir, f"efficiency_{mode}_{timestamp}.csv")
        self.db_path = os.path.join(logs_dir, "efficiency.sqlite3")
        self.store = SQLiteMetricsStore(self.db_path)
        self._file = open(self.filepath, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
=======
# This writes sim stats to CSV and SQLite.
class EfficiencyLogger:
    # Start one new logging session.
    def __init__(self, mode: str, project_dir: str, interval_seconds: float = 5.0):
        self.mode = mode
        # Give each run its own id so later reports can compare them.
        self.run_id = f"{mode}-{uuid.uuid4().hex[:8]}"
        self.interval = max(1.0, interval_seconds)
        self.elapsed = 0.0
        self.total_time = 0.0
        
        timestamp = dtm.datetime.now().strftime("%Y%m%d_%H%M%S")
        logs_dir = os.path.join(project_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        self.filepath = os.path.join(logs_dir, f"efficiency_{mode}_{timestamp}.csv")
        self.db_path = os.path.join(logs_dir, "efficiency.sqlite3")
        self.store = SQLiteMetricsStore(self.db_path)
        
        self._file = open(self.filepath, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        
        # Write the CSV header once at the start.
>>>>>>> master
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

<<<<<<< HEAD
=======
    # Convert an exit count into a per-minute number.
>>>>>>> master
    def _throughput_per_min(self, count: int) -> float:
        if self.total_time <= 0.0:
            return 0.0
        return (count / self.total_time) * 60.0

<<<<<<< HEAD
    def step(self, world, dt: float, sim_time: float) -> None:
        self.total_time += float(dt)
        self.elapsed += float(dt)
=======
    # Write one sample when the timer is ready.
    def step(self, world, dt: float, sim_time: float) -> None:
        self.total_time += dt
        self.elapsed += dt
        
        # Only save a sample every few seconds, not every frame.
>>>>>>> master
        if self.elapsed < self.interval:
            return
        self.elapsed = 0.0

<<<<<<< HEAD
        vehicles_exited = int(world.stats.get("vehicles_exited", 0))
        pedestrians_exited = int(world.stats.get("pedestrians_exited", 0))
        vehicle_tpm = self._throughput_per_min(vehicles_exited)
        ped_tpm = self._throughput_per_min(pedestrians_exited)
=======
        vehicles_exited = world.stats.get("vehicles_exited", 0)
        pedestrians_exited = world.stats.get("pedestrians_exited", 0)
        
        vehicle_tpm = self._throughput_per_min(vehicles_exited)
        ped_tpm = self._throughput_per_min(pedestrians_exited)
        
>>>>>>> master
        sample = {
            "run_id": self.run_id,
            "mode": self.mode,
            "sim_time": sim_time,
            "vehicles_alive": len(world.vehicles),
            "pedestrians_alive": len(world.pedestrians),
<<<<<<< HEAD
            "vehicles_spawned": int(world.stats.get("vehicles_spawned", 0)),
            "vehicles_exited": vehicles_exited,
            "pedestrians_spawned": int(world.stats.get("pedestrians_spawned", 0)),
=======
            "vehicles_spawned": world.stats.get("vehicles_spawned", 0),
            "vehicles_exited": vehicles_exited,
            "pedestrians_spawned": world.stats.get("pedestrians_spawned", 0),
>>>>>>> master
            "pedestrians_exited": pedestrians_exited,
            "vehicle_throughput_per_min": vehicle_tpm,
            "pedestrian_throughput_per_min": ped_tpm,
        }

        self._writer.writerow(
            [
                f"{sim_time:.2f}",
                self.mode,
                sample["vehicles_alive"],
                sample["pedestrians_alive"],
                sample["vehicles_spawned"],
                vehicles_exited,
                sample["pedestrians_spawned"],
                pedestrians_exited,
                f"{vehicle_tpm:.2f}",
                f"{ped_tpm:.2f}",
            ]
        )
        self._file.flush()
        self.store.write_sample(sample)

<<<<<<< HEAD
=======
    # Close files and DB handles.
>>>>>>> master
    def close(self) -> None:
        if not self._file.closed:
            self._file.close()
        self.store.close()
