from config import TRAFFIC_LIGHT_POS

MAP_WIDTH = 1920
MAP_HEIGHT = 1080
CENTER = (960, 540)

<<<<<<< HEAD
# Lane centers for right-hand traffic.
LANE_CENTERS = {
    # N enters from top and moves downward, so it uses the right lane (screen-left).
    "N": {"x": 920},
    # S enters from bottom and moves upward, so it uses the right lane (screen-right).
=======
# Main map numbers live here so sim and UI match.

LANE_CENTERS = {
    "N": {"x": 920},
>>>>>>> master
    "S": {"x": 1000},
    "W": {"y": 580},
    "E": {"y": 500},
}

<<<<<<< HEAD
# Spawn anchors for inbound traffic.
=======
# New cars start from these points outside the visible road.
>>>>>>> master
SPAWN_POINTS = {
    "N": (920, -100),
    "S": (1000, 1180),
    "W": (-100, 580),
    "E": (2020, 500),
}

<<<<<<< HEAD
# Vehicle and spacing constants (pixels).
=======
# Basic sizes and safe distances used by the movement code.
>>>>>>> master
VEHICLE_LENGTH = 90
VEHICLE_WIDTH = 50
LANE_TOLERANCE = 22
FOLLOW_GAP = 45
MIN_SPAWN_GAP = 65
DESPAWN_MARGIN = 220

<<<<<<< HEAD
=======
# Cars stop around these map lines on red.
>>>>>>> master
STOP_LINES = {
    "N": {"y": 280},
    "S": {"y": 795},
    "W": {"x": 691},
    "E": {"x": 1245},
}

<<<<<<< HEAD
=======
# Camera zones are plain rectangles on the map.
>>>>>>> master
CAMERA_ZONES = {
    "N": (880, 300, 1040, 430),
    "S": (880, 650, 1040, 800),
    "W": (650, 480, 820, 600),
    "E": (1100, 480, 1300, 600),
}

TRAFFIC_LIGHTS = TRAFFIC_LIGHT_POS.copy()

<<<<<<< HEAD

def in_rect(pos, rect):
=======
# True if the point is inside the rectangle.
def in_rect(pos, rect):
    # Tiny helper so this check stays in one place.
>>>>>>> master
    x, y = pos
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2
