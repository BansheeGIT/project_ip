import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DIRECTIONS = ["N", "S", "E", "W"]

# If a vehicle goes past these points, we remove it from the sim.
OUT_OF_BOUNDS = {
    "N": (960, 1100),
    "S": (960, -100),
    "E": (-100, 540),
    "W": (2000, 540),
}

# Cars should stop near these lines when the light is red.
STOP_LINES = {
    "N": {"y": 250}, 
    "S": {"y": 795},
    "W": {"x": 691},
    "E": {"x": 1245},
}

# Traffic light sprite positions on the map.
TRAFFIC_LIGHT_POS = [
    {"axis": "NS", "center": (600, 160)},
    {"axis": "EW", "center": (900, 440)},
]

# A few ready-made window sizes for the GUI.
WINDOW_SIZE_PRESETS = {
    "HD": (1280, 720),
    "FULL_HD": (1920, 1080),
    "QHD": (2560, 1440),
    "UHD_4K": (3840, 2160),
}

# Return a saved window size by name.
def get_window_preset(name):
    # Fall back to HD if the name is unknown.
    return WINDOW_SIZE_PRESETS.get(name.upper(), (1280, 720))
