from pathlib import Path

from db.metrics_store import SQLiteMetricsStore
from db.report_queries import compare_latest_modes, list_runs, summarize_run

<<<<<<< HEAD

def _write(store: SQLiteMetricsStore, **kwargs):
    store.write_sample(kwargs)


=======
# Tiny helper for writing one test sample.
def _write(store: SQLiteMetricsStore, **kwargs):
    store.write_sample(kwargs)

# Report helpers should compare fixed and smart runs.
>>>>>>> master
def test_report_queries_compare_modes(tmp_path: Path):
    db_path = tmp_path / "efficiency.sqlite3"
    store = SQLiteMetricsStore(db_path)

    _write(
        store,
        run_id="fixed-a",
        mode="fixed",
        sim_time=10.0,
        vehicles_alive=12,
        pedestrians_alive=4,
        vehicles_spawned=20,
        vehicles_exited=8,
        pedestrians_spawned=10,
        pedestrians_exited=6,
        vehicle_throughput_per_min=48.0,
        pedestrian_throughput_per_min=36.0,
    )
    _write(
        store,
        run_id="fixed-a",
        mode="fixed",
        sim_time=20.0,
        vehicles_alive=10,
        pedestrians_alive=3,
        vehicles_spawned=30,
        vehicles_exited=20,
        pedestrians_spawned=14,
        pedestrians_exited=10,
        vehicle_throughput_per_min=60.0,
        pedestrian_throughput_per_min=30.0,
    )

    _write(
        store,
        run_id="smart-a",
        mode="mqtt-smart",
        sim_time=10.0,
        vehicles_alive=11,
        pedestrians_alive=5,
        vehicles_spawned=22,
        vehicles_exited=12,
        pedestrians_spawned=10,
        pedestrians_exited=5,
        vehicle_throughput_per_min=72.0,
        pedestrian_throughput_per_min=30.0,
    )
    _write(
        store,
        run_id="smart-a",
        mode="mqtt-smart",
        sim_time=20.0,
        vehicles_alive=8,
        pedestrians_alive=4,
        vehicles_spawned=32,
        vehicles_exited=26,
        pedestrians_spawned=16,
        pedestrians_exited=12,
        vehicle_throughput_per_min=78.0,
        pedestrian_throughput_per_min=36.0,
    )
    store.close()

    runs = list_runs(db_path)
    assert len(runs) == 2

    fixed_summary = summarize_run(db_path, "fixed-a")
    assert fixed_summary is not None
    assert fixed_summary.final_vehicle_tpm == 60.0

    comparison = compare_latest_modes(db_path)
    assert comparison is not None
    assert comparison.smart.run_id == "smart-a"
    assert comparison.fixed.run_id == "fixed-a"
    assert comparison.delta_vehicle_tpm == 18.0
