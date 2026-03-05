# app/run.py
from __future__ import annotations

import argparse
import os

from sim.map import MAP_WIDTH, MAP_HEIGHT
from .game import Game


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart traffic light simulation")
    parser.add_argument(
        "--mode",
        choices=("fixed", "mqtt-smart"),
        default="fixed",
        help="Control mode: fixed timing or mqtt smart control",
    )
    args = parser.parse_args()

    # project_dir = .../simulation (where main.py, sim/, traffic/, mqtt/ live)
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    game = Game(
        sim_width=MAP_WIDTH,
        sim_height=MAP_HEIGHT,
        project_dir=project_dir,
        mode=args.mode,
        window_width=1280,
        window_height=720,
    )
    game.run()


if __name__ == "__main__":
    main()
