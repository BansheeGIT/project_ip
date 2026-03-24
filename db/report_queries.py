from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunInfo:
    run_id: str
    mode: str
    started_at: str
    finished_at: str
    samples: int
    duration_sec: float


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class ModeComparison:
    fixed: RunSummary
    smart: RunSummary
    delta_vehicle_tpm: float
    delta_pedestrian_tpm: float


def _connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def list_runs(db_path: str | Path) -> list[RunInfo]:
    conn = _connect(db_path)
    try:
        try:
            rows = conn.execute(
                """
                SELECT
                    run_id,
                    mode,
                    MIN(created_at) AS started_at,
                    MAX(created_at) AS finished_at,
                    COUNT(*) AS samples,
                    MAX(sim_time) AS duration_sec
                FROM efficiency_samples
                GROUP BY run_id, mode
                ORDER BY MAX(created_at) DESC
                """
            ).fetchall()
        except sqlite3.OperationalError:
            return []

        result = []
        for row in rows:
            result.append(
                RunInfo(
                    run_id=row["run_id"],
                    mode=row["mode"],
                    started_at=row["started_at"],
                    finished_at=row["finished_at"],
                    samples=int(row["samples"]),
                    duration_sec=float(row["duration_sec"] or 0.0),
                )
            )
        return result
    finally:
        conn.close()


def summarize_run(db_path: str | Path, run_id: str) -> RunSummary | None:
    conn = _connect(db_path)
    try:
        try:
            base = conn.execute(
                """
                SELECT
                    run_id,
                    mode,
                    COUNT(*) AS samples,
                    MAX(sim_time) AS duration_sec,
                    AVG(vehicle_throughput_per_min) AS avg_vehicle_tpm,
                    AVG(pedestrian_throughput_per_min) AS avg_pedestrian_tpm,
                    MAX(vehicle_throughput_per_min) AS max_vehicle_tpm,
                    MAX(pedestrian_throughput_per_min) AS max_pedestrian_tpm
                FROM efficiency_samples
                WHERE run_id = ?
                GROUP BY run_id, mode
                """,
                (run_id,),
            ).fetchone()
        except sqlite3.OperationalError:
            return None

        if base is None:
            return None

        final = conn.execute(
            """
            SELECT
                vehicle_throughput_per_min,
                pedestrian_throughput_per_min,
                vehicles_alive,
                pedestrians_alive
            FROM efficiency_samples
            WHERE run_id = ?
            ORDER BY sim_time DESC, id DESC
            LIMIT 1
            """,
            (run_id,),
        ).fetchone()

        if final is None:
            return None

        return RunSummary(
            run_id=base["run_id"],
            mode=base["mode"],
            duration_sec=float(base["duration_sec"] or 0.0),
            samples=int(base["samples"]),
            avg_vehicle_tpm=float(base["avg_vehicle_tpm"] or 0.0),
            avg_pedestrian_tpm=float(base["avg_pedestrian_tpm"] or 0.0),
            max_vehicle_tpm=float(base["max_vehicle_tpm"] or 0.0),
            max_pedestrian_tpm=float(base["max_pedestrian_tpm"] or 0.0),
            final_vehicle_tpm=float(final["vehicle_throughput_per_min"] or 0.0),
            final_pedestrian_tpm=float(final["pedestrian_throughput_per_min"] or 0.0),
            final_vehicles_alive=int(final["vehicles_alive"]),
            final_pedestrians_alive=int(final["pedestrians_alive"]),
        )
    finally:
        conn.close()


def latest_run_for_mode(db_path: str | Path, mode: str) -> RunSummary | None:
    conn = _connect(db_path)
    try:
        try:
            row = conn.execute(
                """
                SELECT run_id
                FROM efficiency_samples
                WHERE mode = ?
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (mode,),
            ).fetchone()
        except sqlite3.OperationalError:
            return None
    finally:
        conn.close()

    if row is None:
        return None

    return summarize_run(db_path, row["run_id"])


def compare_latest_modes(
    db_path: str | Path,
    fixed_mode: str = "fixed",
    smart_mode: str = "mqtt-smart",
) -> ModeComparison | None:
    fixed = latest_run_for_mode(db_path, fixed_mode)
    smart = latest_run_for_mode(db_path, smart_mode)
    if fixed is None or smart is None:
        return None

    return ModeComparison(
        fixed=fixed,
        smart=smart,
        delta_vehicle_tpm=smart.final_vehicle_tpm - fixed.final_vehicle_tpm,
        delta_pedestrian_tpm=smart.final_pedestrian_tpm - fixed.final_pedestrian_tpm,
    )
