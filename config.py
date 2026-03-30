import os
<<<<<<< HEAD
# Signed changes: Abdil

# Базовые настройки путей - Abdil
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Направления движения - Abdil
DIRECTIONS = ["N", "S", "E", "W"]

# Границы карты (чтобы удалять машины, если они уехали за край) - Abdil
# Формат: "Направление": (координата_удаления, другая_координата) - Abdil
OUT_OF_BOUNDS = {
    "N": (960, 1100),  # Уехал вниз за пределы экрана (Y > 1080) - Abdil
    "S": (960, -100),  # Уехал вверх (Y < 0) - Abdil
    "E": (-100, 540),  # Уехал влево (X < 0) - Abdil
    "W": (2000, 540),  # Уехал вправо (X > 1920) - Abdil
}

# Координаты стоп-линий (где останавливаться на красный) - Abdil
=======

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
>>>>>>> master
STOP_LINES = {
    "N": {"y": 250}, 
    "S": {"y": 795},
    "W": {"x": 691},
    "E": {"x": 1245},
}

<<<<<<< HEAD
# Traffic light sprite anchors (kept in one shared place).
TRAFFIC_LIGHT_POS = [
    {
        "axis": "NS",
        "center": (600, 160),
    },
    {
        "axis": "EW",
        "center": (900, 440),
    },
]

# Common desktop window presets for simulation display scaling. - Abdil
=======
# Traffic light sprite positions on the map.
TRAFFIC_LIGHT_POS = [
    {"axis": "NS", "center": (600, 160)},
    {"axis": "EW", "center": (900, 440)},
]

# A few ready-made window sizes for the GUI.
>>>>>>> master
WINDOW_SIZE_PRESETS = {
    "HD": (1280, 720),
    "FULL_HD": (1920, 1080),
    "QHD": (2560, 1440),
    "UHD_4K": (3840, 2160),
}

<<<<<<< HEAD

def get_window_preset(name: str) -> tuple[int, int]:
    """Returns a preset window size by name (e.g., HD, FULL_HD, QHD, UHD_4K)."""
    normalized = name.strip().upper().replace("-", "_").replace(" ", "_")
    if normalized not in WINDOW_SIZE_PRESETS:
        available = ", ".join(WINDOW_SIZE_PRESETS.keys())
        raise KeyError(f"Unknown window preset '{name}'. Available: {available}")
    return WINDOW_SIZE_PRESETS[normalized]
=======
# Return a saved window size by name.
def get_window_preset(name):
    # Fall back to HD if the name is unknown.
    return WINDOW_SIZE_PRESETS.get(name.upper(), (1280, 720))
>>>>>>> master
