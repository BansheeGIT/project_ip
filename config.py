import os
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
STOP_LINES = {
    "N": {"y": 250}, 
    "S": {"y": 795},
    "W": {"x": 691},
    "E": {"x": 1245},
}

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
WINDOW_SIZE_PRESETS = {
    "HD": (1280, 720),
    "FULL_HD": (1920, 1080),
    "QHD": (2560, 1440),
    "UHD_4K": (3840, 2160),
}


def get_window_preset(name: str) -> tuple[int, int]:
    """Returns a preset window size by name (e.g., HD, FULL_HD, QHD, UHD_4K)."""
    normalized = name.strip().upper().replace("-", "_").replace(" ", "_")
    if normalized not in WINDOW_SIZE_PRESETS:
        available = ", ".join(WINDOW_SIZE_PRESETS.keys())
        raise KeyError(f"Unknown window preset '{name}'. Available: {available}")
    return WINDOW_SIZE_PRESETS[normalized]
