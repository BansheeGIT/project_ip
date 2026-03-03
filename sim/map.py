MAP_WIDTH = 1920
MAP_HEIGHT = 1080
CENTER = (960, 540)
# Signed changes: Codex

# Per-direction lane centers used by spawner and world alignment.
LANE_CENTERS = {
    # N drives downward (from top), S drives upward (from bottom).
    # Keep each direction on the visual center of its lane.
    "N": {"x": 1000},
    "S": {"x": 920},
    "W": {"y": 580},
    "E": {"y": 500},
}

# Spawn anchors for inbound traffic (just outside map bounds).
SPAWN_POINTS = {
    "N": (1000, -100),
    "S": (920, 1180),
    "W": (-100, 580),
    "E": (2020, 500),
}

# Vehicle and spacing constants (pixels).
VEHICLE_LENGTH = 90
VEHICLE_WIDTH = 50
LANE_TOLERANCE = 22
FOLLOW_GAP = 45
MIN_SPAWN_GAP = 65
DESPAWN_MARGIN = 220

STOP_LINES = {
    "N": {"y": 280}, 
    "S": {"y": 795},
    "W": {"x": 691},
    "E": {"x": 1245},
}

CAMERA_ZONES = {
    "N": (880, 300, 1040, 430),
    "S": (880, 650, 1040, 800),
    "W": (650, 480, 820, 600),
    "E": (1100, 480, 1300, 600),
}

TRAFFIC_LIGHTS = {
    "NS": (820, 400),  # Западный (для W->E)
    "EW": (1100, 680), # Южный (для S->N)
}

def in_rect(pos, rect):
    x, y = pos
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

