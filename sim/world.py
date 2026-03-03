# sim/world.py
from __future__ import annotations
import random
from .entities import create_car, create_emergency_vehicle
from sim.pedestrians import Pedestrian 
from .map import MAP_HEIGHT, MAP_WIDTH, STOP_LINES as MAP_STOP_LINES
from traffic.phases import EW_GREEN, NS_GREEN, NS_YELLOW, EW_YELLOW, ALL_RED

class World:
    ACCEL = 180.0
    BRAKE = 320.0

    def __init__(self):
        self.vehicles = []
        self.pedestrians = []
        self.next_id = 1
        self.green_axis = "NS"
        self.current_phase = NS_GREEN
        self.STOP_LINES = {k: float(v["y"] if k in "NS" else v["x"]) for k, v in MAP_STOP_LINES.items()}

        # Спавним машины и людей при запуске, чтобы карта не была пустой
        self.spawn_vehicle("N", 1000, 50, 200)
        self.spawn_vehicle("S", 920, 1000, 200)
        self.spawn_pedestrian("W")
        self.spawn_pedestrian("E")

    def compute_preemption_state(self):
        return False, None

    # --- ПЕШЕХОДЫ ---
    def spawn_pedestrian(self, direction):
        variant = random.choice(["ped1", "ped2", "ped3", "ped4"])
        speed = 100.0
        if direction == "W": pos, axis, vel = [-50, 540], "EW", [speed, 0]
        elif direction == "E": pos, axis, vel = [1970, 540], "EW", [-speed, 0]
        elif direction == "N": pos, axis, vel = [960, -50], "NS", [0, speed]
        elif direction == "S": pos, axis, vel = [960, 1130], "NS", [0, -speed]
        else: return

        ped = Pedestrian(pos[0], pos[1], axis)
        ped.velocity = vel
        ped.variant = variant
        ped.direction = direction
        self.pedestrians.append(ped)

    def update_pedestrians(self, dt, controller):
        phase = controller.current_phase
        for p in self.pedestrians:
            # ПДД: люди идут по зебре вместе с параллельным потоком машин (или когда всем красный)
            if phase == ALL_RED:
                p.active = True
            elif phase in (NS_GREEN, NS_YELLOW) and p.axis == "EW":
                p.active = True # Машинам зеленый сверху-вниз -> можно переходить слева-направо
            elif phase in (EW_GREEN, EW_YELLOW) and p.axis == "NS":
                p.active = True # Машинам зеленый слева-направо -> можно переходить сверху-вниз
            else:
                p.active = False
            p.update(dt)
        self.pedestrians = [p for p in self.pedestrians if not p.finished]

    # --- МАШИНЫ ---
    def has_passed_stop_line(self, v):
        """Проверяет, проехала ли машина светофор. Если да — должна закончить маневр!"""
        d = v["direction"]
        if d == "N": return v["y"] > self.STOP_LINES["N"]
        if d == "S": return v["y"] < self.STOP_LINES["S"]
        if d == "E": return v["x"] < self.STOP_LINES["E"]
        if d == "W": return v["x"] > self.STOP_LINES["W"]
        return False

    def _get_distance_to_stop_line(self, v):
        d = v["direction"]
        if d == "N": return self.STOP_LINES["N"] - v["y"]
        if d == "S": return v["y"] - self.STOP_LINES["S"]
        if d == "E": return v["x"] - self.STOP_LINES["E"]
        if d == "W": return self.STOP_LINES["W"] - v["x"]
        return 0

    def _get_distance_to_car_ahead(self, v):
        """Определяет расстояние до впереди идущей машины, чтобы не врезаться."""
        min_gap = float("inf")
        for other in self.vehicles:
            if other["id"] == v["id"] or other["direction"] != v["direction"]: continue
            if v["direction"] == "N" and other["y"] > v["y"]: gap = other["y"] - v["y"]
            elif v["direction"] == "S" and other["y"] < v["y"]: gap = v["y"] - other["y"]
            elif v["direction"] == "E" and other["x"] < v["x"]: gap = v["x"] - other["x"]
            elif v["direction"] == "W" and other["x"] > v["x"]: gap = other["x"] - v["x"]
            else: continue
            
            gap -= 90 # Вычитаем длину машины
            if gap < min_gap: min_gap = gap
        return min_gap

    def step(self, dt):
        for v in self.vehicles:
            axis = "NS" if v["direction"] in ("N", "S") else "EW"
            target_speed = float(v["speed_val"])
            
            # 1. Светофор: тормозим ПЕРЕД линией, если красный. Если проехали — едем дальше.
            if self.green_axis != axis and not self.has_passed_stop_line(v):
                dist_to_stop = self._get_distance_to_stop_line(v)
                if dist_to_stop < 180: # Плавное торможение перед линией
                    target_speed = target_speed * max(0.0, (dist_to_stop - 15) / 165)
            
            # 2. Очередь: если впереди машина, тормозим
            dist_ahead = self._get_distance_to_car_ahead(v)
            if dist_ahead < 20.0:
                target_speed = 0.0
                
            # 3. Пешеходы: экстренное торможение, если человек на зебре
            for p in self.pedestrians:
                if 820 <= p.position[0] <= 1100 and 410 <= p.position[1] <= 670:
                    target_speed = 0.0

            # Плавное применение скорости
            curr = v.get("current_speed", 0.0)
            if curr < target_speed: curr = min(curr + self.ACCEL * dt, target_speed)
            else: curr = max(curr - self.BRAKE * dt, target_speed)
            
            v["current_speed"] = curr
            spd = curr
            if v["direction"] == "N": v["velocity"] = [0, spd]
            elif v["direction"] == "S": v["velocity"] = [0, -spd]
            elif v["direction"] == "E": v["velocity"] = [-spd, 0]
            elif v["direction"] == "W": v["velocity"] = [spd, 0]
            
            v["position"][0] += v["velocity"][0] * dt
            v["position"][1] += v["velocity"][1] * dt
            v["x"], v["y"] = v["position"][0], v["position"][1]
            v["is_stopped"] = curr <= 0.5

        # Удаление объектов, которые далеко уехали
        self.vehicles = [v for v in self.vehicles if -200 <= v["x"] <= 2120 and -200 <= v["y"] <= 1280]

    def can_spawn(self, direction, x, y):
        for v in self.vehicles:
            if abs(v["x"] - x) < 120 and abs(v["y"] - y) < 120: return False
        return True

    def spawn_vehicle(self, direction, x, y, speed):
        self.next_id += 1
        v = create_car(self.next_id, x, y, 0, 0, direction)
        v.update({"speed_val": speed, "position": [x, y], "current_speed": speed, "x": x, "y": y})
        self.vehicles.append(v)

    def spawn_emergency(self, direction, x, y, speed, sirens_on=True):
        self.next_id += 1
        v = create_emergency_vehicle(self.next_id, x, y, 0, 0, direction)
        v.update({"speed_val": speed, "position": [x, y], "current_speed": speed, "x": x, "y": y, "sirens_on": sirens_on})
        self.vehicles.append(v)