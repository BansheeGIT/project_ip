# sim/spawner.py
import random
from sim.map import SPAWN_POINTS

EMERGENCY_CHANCE = 0.02

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
            if self.timers[d] > self.RATES[d] * random.uniform(0.8, 1.2):
                if self.spawn_car(d):
                    self.timers[d] = 0.0

            # 2. Спавн людей
            self.ped_timers[d] += dt
            if self.ped_timers[d] > self.PED_RATES[d] * random.uniform(0.7, 1.3):
                self.world.spawn_pedestrian(d)
                self.ped_timers[d] = 0.0

    def spawn_car(self, direction):
        if direction not in SPAWN_POINTS: return False
        x, y = SPAWN_POINTS[direction]
        if not self.world.can_spawn(direction, x, y): return False

        speed = random.randint(180, 220)
        is_emergency = random.random() < EMERGENCY_CHANCE
        
        if is_emergency:
            self.world.spawn_emergency(direction, x, y, speed + 100)
        else:
            self.world.spawn_vehicle(direction, x, y, speed)
        return True