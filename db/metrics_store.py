<<<<<<< HEAD
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Mapping, Any


class SQLiteMetricsStore:
    """Persistence layer for simulation efficiency samples."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._ensure_schema()

    def _ensure_schema(self) -> None:
=======
import sqlite3
from pathlib import Path

# Small SQLite helper for metric samples.
class SQLiteMetricsStore:
    # Open the database and make sure the table exists.
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        # Create the logs folder if it is still missing.
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._ensure_schema()

    # Create the table once if it is missing.
    def _ensure_schema(self):
>>>>>>> master
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS efficiency_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
<<<<<<< HEAD
                run_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                sim_time REAL NOT NULL,
                vehicles_alive INTEGER NOT NULL,
                pedestrians_alive INTEGER NOT NULL,
                vehicles_spawned INTEGER NOT NULL,
                vehicles_exited INTEGER NOT NULL,
                pedestrians_spawned INTEGER NOT NULL,
                pedestrians_exited INTEGER NOT NULL,
                vehicle_throughput_per_min REAL NOT NULL,
                pedestrian_throughput_per_min REAL NOT NULL,
=======
                run_id TEXT,
                mode TEXT,
                sim_time REAL,
                vehicles_alive INTEGER,
                pedestrians_alive INTEGER,
                vehicles_spawned INTEGER,
                vehicles_exited INTEGER,
                pedestrians_spawned INTEGER,
                pedestrians_exited INTEGER,
                vehicle_throughput_per_min REAL,
                pedestrian_throughput_per_min REAL,
>>>>>>> master
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

<<<<<<< HEAD
    def write_sample(self, sample: Mapping[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO efficiency_samples (
                run_id,
                mode,
                sim_time,
                vehicles_alive,
                pedestrians_alive,
                vehicles_spawned,
                vehicles_exited,
                pedestrians_spawned,
                pedestrians_exited,
                vehicle_throughput_per_min,
                pedestrian_throughput_per_min
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(sample["run_id"]),
                str(sample["mode"]),
                float(sample["sim_time"]),
                int(sample["vehicles_alive"]),
                int(sample["pedestrians_alive"]),
                int(sample["vehicles_spawned"]),
                int(sample["vehicles_exited"]),
                int(sample["pedestrians_spawned"]),
                int(sample["pedestrians_exited"]),
                float(sample["vehicle_throughput_per_min"]),
                float(sample["pedestrian_throughput_per_min"]),
            ),
        )
        self.conn.commit()

    def close(self) -> None:
=======
    # Insert one metric sample into the table.
    def write_sample(self, sample: dict):
        # Named parameters keep the insert readable.
        self.conn.execute(
            """
            INSERT INTO efficiency_samples (
                run_id, mode, sim_time, vehicles_alive, pedestrians_alive,
                vehicles_spawned, vehicles_exited, pedestrians_spawned, pedestrians_exited,
                vehicle_throughput_per_min, pedestrian_throughput_per_min
            ) VALUES (
                :run_id, :mode, :sim_time, :vehicles_alive, :pedestrians_alive,
                :vehicles_spawned, :vehicles_exited, :pedestrians_spawned, :pedestrians_exited,
                :vehicle_throughput_per_min, :pedestrian_throughput_per_min
            )
            """,
            sample,
        )
        self.conn.commit()

    # Shut the database connection at the end.
    def close(self):
>>>>>>> master
        self.conn.close()
