<<<<<<< HEAD
# sim/spawner.py
=======
>>>>>>> master
import random
from sim.map import SPAWN_POINTS

EMERGENCY_CHANCE = 0.02
EMERGENCY_SIREN_CHANCE = 0.55

<<<<<<< HEAD
class Spawner:
    def __init__(self, world):
        self.world = world
        self.timers = {"N": 0.0, "S": 0.0, "E": 0.0, "W": 0.0}
        self.ped_timers = {"N": 0.0, "S": 0.0, "E": 0.0, "W": 0.0}
        
        # Интервалы появления (в секундах)
        self.RATES = {"N": 2.5, "S": 3.0, "E": 4.0, "W": 3.0}
        self.PED_RATES = {"N": 5.0, "S": 5.0, "E": 6.0, "W": 6.0}

    def step(self, dt):
        """Главный цикл спавнера."""
        for d in ("N", "S", "E", "W"):
            # 1. Спавн машин
            self.timers[d] += dt
=======
# This adds new cars and people over time.
class Spawner:
    # Start the timers and keep default spawn rates here.
    def __init__(self, world):
        self.world = world
        # Each direction gets its own timer.
        self.timers = {"N": 0.0, "S": 0.0, "E": 0.0, "W": 0.0}
        self.ped_timers = {"N": 0.0, "S": 0.0, "E": 0.0, "W": 0.0}
        
        self.RATES = {"N": 2.5, "S": 3.0, "E": 4.0, "W": 3.0}
        self.PED_RATES = {"N": 5.0, "S": 5.0, "E": 6.0, "W": 6.0}

    # Tick all spawn timers for one frame.
    def step(self, dt):
        for d in ("N", "S", "E", "W"):
            self.timers[d] += dt
            # Add a little random shift so traffic feels less robotic.
            
>>>>>>> master
            if self.timers[d] > self.RATES[d] * random.uniform(0.8, 1.2):
                if self.spawn_car(d):
                    self.timers[d] = 0.0

<<<<<<< HEAD
            # 2. Спавн людей
=======
>>>>>>> master
            self.ped_timers[d] += dt
            if self.ped_timers[d] > self.PED_RATES[d] * random.uniform(0.7, 1.3):
                self.world.spawn_pedestrian(d)
                self.ped_timers[d] = 0.0

<<<<<<< HEAD
    def spawn_car(self, direction):
        if direction not in SPAWN_POINTS: return False
        x, y = SPAWN_POINTS[direction]
        if not self.world.can_spawn(direction, x, y): return False

        speed = random.randint(180, 220)
        is_emergency = random.random() < EMERGENCY_CHANCE
=======
    # Try to spawn one car in one direction.
    def spawn_car(self, direction):
        if direction not in SPAWN_POINTS:
            return False
            
        x, y = SPAWN_POINTS[direction]
        if not self.world.can_spawn(direction, x, y):
            return False

        speed = random.randint(180, 220)
        is_emergency = random.random() < EMERGENCY_CHANCE
        # Ambulances are rare, and not all of them use sirens.
>>>>>>> master
        
        if is_emergency:
            sirens_on = random.random() < EMERGENCY_SIREN_CHANCE
            bonus_speed = 100 if sirens_on else 40
            self.world.spawn_emergency(direction, x, y, speed + bonus_speed, sirens_on=sirens_on)
        else:
            self.world.spawn_vehicle(direction, x, y, speed)
<<<<<<< HEAD
        return True

    def spawn(self, direction):
        """Backward-compatible alias used by UI manual spawn controls."""
=======
            
        return True

    # Keep a short name for old UI code.
    def spawn(self, direction):
        # Short alias used by the UI buttons.
>>>>>>> master
        return self.spawn_car(direction)
