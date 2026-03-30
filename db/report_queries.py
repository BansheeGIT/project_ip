import sqlite3
from dataclasses import dataclass

@dataclass
# One short row about a saved run.
class RunInfo:
    run_id: str
    mode: str
    started_at: str
    finished_at: str
    samples: int
    duration_sec: float

@dataclass
# Main numbers for one finished run.
class RunSummary:
    run_id: str
    mode: str
    duration_sec: float
    samples: int
    avg_vehicle_tpm: float
    avg_pedestrian_tpm: float
    max_vehicle_tpm: float
    max_pedestrian_tpm: float
    final_vehicle_tpm: float
    final_pedestrian_tpm: float
    final_vehicles_alive: int
    final_pedestrians_alive: int

@dataclass
# Newest fixed and smart runs stay together here.
class ModeComparison:
    fixed: RunSummary
    smart: RunSummary
    delta_vehicle_tpm: float
    delta_pedestrian_tpm: float

# Open SQLite and return rows by column name.
def _connect(db_path):
    # Row objects let us read SQL results by column name.
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Return a short list of runs found in the database.
def list_runs(db_path) -> list[RunInfo]:
    try:
        with _connect(db_path) as conn:
            rows = conn.execute(
                """
                SELECT run_id, mode, MIN(created_at) AS started_at, MAX(created_at) AS finished_at,
                       COUNT(*) AS samples, MAX(sim_time) AS duration_sec
                FROM efficiency_samples
                GROUP BY run_id, mode
                ORDER BY MAX(created_at) DESC
                """
            ).fetchall()
            
            return [
                RunInfo(
                    run_id=row["run_id"],
                    mode=row["mode"],
                    started_at=row["started_at"],
                    finished_at=row["finished_at"],
                    samples=row["samples"],
                    duration_sec=row["duration_sec"] or 0.0,
                ) for row in rows
            ]
    except sqlite3.OperationalError:
        return []

# Build one summary object for a chosen run id.
def summarize_run(db_path, run_id) -> RunSummary | None:
    try:
        with _connect(db_path) as conn:
            base = conn.execute(
                """
                SELECT run_id, mode, COUNT(*) AS samples, MAX(sim_time) AS duration_sec,
                       AVG(vehicle_throughput_per_min) AS avg_vehicle_tpm,
                       AVG(pedestrian_throughput_per_min) AS avg_pedestrian_tpm,
                       MAX(vehicle_throughput_per_min) AS max_vehicle_tpm,
                       MAX(pedestrian_throughput_per_min) AS max_pedestrian_tpm
                FROM efficiency_samples
                WHERE run_id = ? GROUP BY run_id, mode
                """, (run_id,)
            ).fetchone()

            if not base:
                return None

            # The last sample is treated as the final state of the run.
            final = conn.execute(
                """
                SELECT vehicle_throughput_per_min, pedestrian_throughput_per_min,
                       vehicles_alive, pedestrians_alive
                FROM efficiency_samples
                WHERE run_id = ? ORDER BY sim_time DESC, id DESC LIMIT 1
                """, (run_id,)
            ).fetchone()

            return RunSummary(
                run_id=base["run_id"], mode=base["mode"],
                duration_sec=base["duration_sec"] or 0.0, samples=base["samples"],
                avg_vehicle_tpm=base["avg_vehicle_tpm"] or 0.0,
                avg_pedestrian_tpm=base["avg_pedestrian_tpm"] or 0.0,
                max_vehicle_tpm=base["max_vehicle_tpm"] or 0.0,
                max_pedestrian_tpm=base["max_pedestrian_tpm"] or 0.0,
                final_vehicle_tpm=final["vehicle_throughput_per_min"] or 0.0,
                final_pedestrian_tpm=final["pedestrian_throughput_per_min"] or 0.0,
                final_vehicles_alive=final["vehicles_alive"],
                final_pedestrians_alive=final["pedestrians_alive"],
            )
    except sqlite3.OperationalError:
        return None

# Pick the newest run for one mode.
def latest_run_for_mode(db_path, mode) -> RunSummary | None:
    try:
        with _connect(db_path) as conn:
            row = conn.execute(
                "SELECT run_id FROM efficiency_samples WHERE mode = ? ORDER BY created_at DESC, id DESC LIMIT 1",
                (mode,)
            ).fetchone()
            
            if not row:
                return None
            return summarize_run(db_path, row["run_id"])
    except sqlite3.OperationalError:
        return None

# Compare the newest fixed run with the newest smart run.
def compare_latest_modes(db_path, fixed_mode="fixed", smart_mode="mqtt-smart") -> ModeComparison | None:
    # Compare only the newest run from each mode.
    fixed = latest_run_for_mode(db_path, fixed_mode)
    smart = latest_run_for_mode(db_path, smart_mode)
    
    if not fixed or not smart:
        return None

    return ModeComparison(
        fixed=fixed, smart=smart,
        delta_vehicle_tpm=smart.final_vehicle_tpm - fixed.final_vehicle_tpm,
        delta_pedestrian_tpm=smart.final_pedestrian_tpm - fixed.final_pedestrian_tpm,
    )
