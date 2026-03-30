import random

CAR_VARIANTS = [
    "grey_car", "red_car", "blue_car", "green_car", 
    "light_blue_car", "pink_car", "purple_car"
]

# Normal cars use this data shape.
def create_car(id, x, y, vx, vy, direction):
    """Create a car, picking a random skin from the available list."""
    # Pick the look here so the renderer knows which sprite to use.
    variant = random.choice(CAR_VARIANTS)
    
    return {
        "type": "car",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "max_speed": 0.0,
        "current_speed": 0.0,
        "should_stop": False,
        "is_stopped": False,
        "direction": direction,
        "variant": variant, 
    }

# Emergency cars use this data shape.
def create_emergency_vehicle(id, x, y, vx, vy, direction, sirens_on=True):
    # Emergency cars always use the ambulance sprite.
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
        "direction": direction,
        "variant": "ambulance",
    }

# Pedestrians use this data shape.
def create_pedestrian(id, x, y, vx, vy, direction):
    """Create a pedestrian, picking one of the 4 variations."""
    # Same idea here, just with four simple people sprites.
    variant = random.choice(["ped1", "ped2", "ped3", "ped4"])
    
    return {
        "type": "pedestrian",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "should_stop": False,
        "is_stopped": False,
        "direction": direction,
        "variant": variant, 
    }
