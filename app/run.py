import argparse
import os

from sim.map import MAP_WIDTH, MAP_HEIGHT
from .game import Game


# Run the app from the command line.
def main():
    # Only choose the control mode here. The Game object builds the rest.
    parser = argparse.ArgumentParser(description="Smart traffic light simulation")
    parser.add_argument("--mode", choices=["fixed", "mqtt-smart"], default="fixed")
    args = parser.parse_args()

    # This helps other modules find assets and logs from one place.
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    game = Game(
        sim_width=MAP_WIDTH,
        sim_height=MAP_HEIGHT,
        project_dir=project_dir,
        mode=args.mode
    )
    game.run()


if __name__ == "__main__":
    main()
