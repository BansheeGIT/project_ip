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
    parser.add_argument(
        "--mqtt-transport",
        choices=("hivemq", "local"),
        default="hivemq",
        help="Transport used in mqtt-smart mode",
    )
    parser.add_argument(
        "--mqtt-host",
        default="broker.hivemq.com",
        help="MQTT broker host (used for hivemq transport)",
    )
    parser.add_argument(
        "--mqtt-port",
        type=int,
        default=1883,
        help="MQTT broker port (used for hivemq transport)",
    )
    args = parser.parse_args()

    # project_dir = .../simulation (where main.py, sim/, traffic/, mqtt/ live)
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    game = Game(
        sim_width=MAP_WIDTH,
        sim_height=MAP_HEIGHT,
        project_dir=project_dir,
        mode=args.mode,
        mqtt_transport=args.mqtt_transport,
        mqtt_host=args.mqtt_host,
        mqtt_port=args.mqtt_port,
        window_width=1280,
        window_height=720,
    )
    game.run()


if __name__ == "__main__":
    main()
