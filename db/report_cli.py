from __future__ import annotations

import argparse

from .report_queries import compare_latest_modes, list_runs


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare fixed vs mqtt-smart runs from SQLite metrics")
    parser.add_argument(
        "--db",
        default="logs/efficiency.sqlite3",
        help="Path to SQLite metrics database",
    )
    args = parser.parse_args()

    runs = list_runs(args.db)
    if not runs:
        print("No runs found")
        return

    print("Latest runs:")
    for run in runs[:10]:
        print(
            f"- {run.run_id} ({run.mode}) samples={run.samples} duration={run.duration_sec:.1f}s "
            f"started={run.started_at}"
        )

    comparison = compare_latest_modes(args.db)
    if comparison is None:
        print("\nNeed at least one fixed and one mqtt-smart run for comparison")
        return

    print("\nComparison (latest fixed vs latest mqtt-smart):")
    print(
        f"fixed final vehicle_tpm={comparison.fixed.final_vehicle_tpm:.2f}, "
        f"ped_tpm={comparison.fixed.final_pedestrian_tpm:.2f}"
    )
    print(
        f"smart final vehicle_tpm={comparison.smart.final_vehicle_tpm:.2f}, "
        f"ped_tpm={comparison.smart.final_pedestrian_tpm:.2f}"
    )
    print(
        f"delta vehicle_tpm={comparison.delta_vehicle_tpm:+.2f}, "
        f"delta ped_tpm={comparison.delta_pedestrian_tpm:+.2f}"
    )


if __name__ == "__main__":
    main()
