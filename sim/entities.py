import random

<<<<<<< HEAD

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

=======
CAR_VARIANTS = [
    "grey_car", "red_car", "blue_car", "green_car", 
    "light_blue_car", "pink_car", "purple_car"
]

# Normal cars use this data shape.
def create_car(id, x, y, vx, vy, direction):
    """Create a car, picking a random skin from the available list."""
    # Pick the look here so the renderer knows which sprite to use.
    variant = random.choice(CAR_VARIANTS)
    
>>>>>>> master
    return {
        "type": "car",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "max_speed": 0.0,
        "current_speed": 0.0,
        "should_stop": False,
        "is_stopped": False,
<<<<<<< HEAD
        "direction": DIRECTIONS,
        "variant": random.choice(variants),
    }


def create_emergency_vehicle(id, x, y, vx, vy, DIRECTIONS, sirens_on=None):
    """Create an emergency vehicle (ambulance)."""
    if sirens_on is None:
        # Preemption uses rushing emergency vehicles by default.
        sirens_on = True

=======
        "direction": direction,
        "variant": variant, 
    }

# Emergency cars use this data shape.
def create_emergency_vehicle(id, x, y, vx, vy, direction, sirens_on=True):
    # Emergency cars always use the ambulance sprite.
>>>>>>> master
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
<<<<<<< HEAD
        "direction": DIRECTIONS,
        "variant": "ambulance",
    }


def create_pedestrian(id, x, y, vx, vy, DIRECTIONS):
    """Create a pedestrian."""
=======
        "direction": direction,
        "variant": "ambulance",
    }

# Pedestrians use this data shape.
def create_pedestrian(id, x, y, vx, vy, direction):
    """Create a pedestrian, picking one of the 4 variations."""
    # Same idea here, just with four simple people sprites.
    variant = random.choice(["ped1", "ped2", "ped3", "ped4"])
    
>>>>>>> master
    return {
        "type": "pedestrian",
        "id": id,
        "position": [x, y],
        "velocity": [vx, vy],
        "should_stop": False,
        "is_stopped": False,
<<<<<<< HEAD
        "direction": DIRECTIONS,
        "variant": "pedestrian_1",
=======
        "direction": direction,
        "variant": variant, 
>>>>>>> master
    }
