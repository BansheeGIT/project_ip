from sim.map import MAP_WIDTH, MAP_HEIGHT, CAMERA_ZONES, STOP_LINES, in_rect

def test_map_dimensions():
    assert MAP_WIDTH == 1920
    assert MAP_HEIGHT == 1080

def test_camera_zone_north():
    assert in_rect((900, 350), CAMERA_ZONES["N"]) is True
    assert in_rect((900, 200), CAMERA_ZONES["N"]) is False

def test_stop_lines_order():
    assert STOP_LINES["N"]["y"] < STOP_LINES["S"]["y"]
