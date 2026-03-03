# app/run.py
from __future__ import annotations

import os

from sim.map import MAP_WIDTH, MAP_HEIGHT
from .game import Game


def main() -> None:
    # project_dir = .../simulation (where main.py, sim/, traffic/, mqtt/ live)
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    game = Game(
        sim_width=MAP_WIDTH,
        sim_height=MAP_HEIGHT,
        project_dir=project_dir,
        window_width=1280,
        window_height=720,
    )
    game.run()


if __name__ == "__main__":
    main()
