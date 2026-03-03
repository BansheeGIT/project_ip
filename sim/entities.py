import random


def create_car(id, x, y, vx, vy, DIRECTIONS):
    """Create a normal car with a random skin."""
    variants = [
        "grey_car",
        "red_car",
        "blue_car",
        "green_car",
        "light_blue car",
        "pink_car",
        "purple_car",
    ]

    return {
        "type": "car",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "max_speed": 0.0,
        "current_speed": 0.0,
        "should_stop": False,
        "is_stopped": False,
        "direction": DIRECTIONS,
        "variant": random.choice(variants),
    }


def create_emergency_vehicle(id, x, y, vx, vy, DIRECTIONS, sirens_on=None):
    """Create an emergency vehicle (ambulance)."""
    if sirens_on is None:
        # Preemption uses rushing emergency vehicles by default.
        sirens_on = True

    return {
        "type": "emergency",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "max_speed": 0.0,
        "current_speed": 0.0,
        "should_stop": False,
        "is_stopped": False,
        "sirens_on": sirens_on,
        "direction": DIRECTIONS,
        "variant": "ambulance",
    }


def create_pedestrian(id, x, y, vx, vy, DIRECTIONS):
    """Create a pedestrian."""
    return {
        "type": "pedestrian",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "should_stop": False,
        "is_stopped": False,
        "direction": DIRECTIONS,
        "variant": "pedestrian_1",
    }
