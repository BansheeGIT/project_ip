from __future__ import annotations

import random

from sim.pedestrians import Pedestrian
from traffic.phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW

from .entities import create_car, create_emergency_vehicle
from .map import FOLLOW_GAP, STOP_LINES as MAP_STOP_LINES, VEHICLE_LENGTH, VEHICLE_WIDTH

<<<<<<< HEAD

class World:
=======
# World object keeps cars and pedestrians together.
class World:
    # World keeps all moving objects and updates them each frame.
>>>>>>> master
    ACCEL = 180.0
    BRAKE = 320.0
    PREEMPTION_DISTANCE = 420.0
    SIGNAL_BRAKE_DISTANCE = 180.0
    LOOKAHEAD_DISTANCE = 240.0
    SAFE_BUMPER_GAP = 18.0
    DESPAWN_X_MIN = -200.0
    DESPAWN_X_MAX = 2120.0
    DESPAWN_Y_MIN = -200.0
    DESPAWN_Y_MAX = 1280.0
    CROSSWALK_X_MIN = 650.0
    CROSSWALK_X_MAX = 1270.0
    CROSSWALK_Y_MIN = 360.0
    CROSSWALK_Y_MAX = 720.0

<<<<<<< HEAD
=======
    # Get the world ready and add a few starter objects.
>>>>>>> master
    def __init__(self):
        self.vehicles = []
        self.pedestrians = []
        self.next_id = 1
        self.next_ped_id = 1
        self.green_axis = "NS"
        self.current_phase = NS_GREEN
        self.stats = {
            "vehicles_spawned": 0,
            "vehicles_exited": 0,
            "pedestrians_spawned": 0,
            "pedestrians_exited": 0,
        }
<<<<<<< HEAD
        self.STOP_LINES = {
            key: float(value["y"] if key in "NS" else value["x"])
            for key, value in MAP_STOP_LINES.items()
        }

        # Seed the world so the map is not empty at startup.
=======
        # Flatten the stop-line data so movement code can read one number fast.
        self.STOP_LINES = {
            key: value["y"] if key in "NS" else value["x"]
            for key, value in MAP_STOP_LINES.items()
        }

        # Add a few starter objects so the map is not empty.
>>>>>>> master
        self.spawn_vehicle("N", 920, 50, 200)
        self.spawn_vehicle("S", 1000, 1000, 200)
        self.spawn_pedestrian("W")
        self.spawn_pedestrian("E")

<<<<<<< HEAD
    def compute_preemption_state(self):
=======
    # See if a siren car should take over the lights.
    def compute_preemption_state(self):
        # Look for the nearest siren car before the stop line.
>>>>>>> master
        nearest_axis = None
        nearest_distance = float("inf")

        for vehicle in self.vehicles:
<<<<<<< HEAD
            if vehicle.get("type") != "emergency" or not vehicle.get("sirens_on", False):
=======
            if vehicle.get("type") != "emergency" or not vehicle.get("sirens_on"):
>>>>>>> master
                continue
            if self.has_passed_stop_line(vehicle):
                continue

<<<<<<< HEAD
            distance = max(0.0, float(self._get_distance_to_stop_line(vehicle)))
=======
            distance = max(0.0, self._get_distance_to_stop_line(vehicle))
>>>>>>> master
            if distance > self.PREEMPTION_DISTANCE:
                continue

            if distance < nearest_distance:
                nearest_distance = distance
<<<<<<< HEAD
                nearest_axis = "NS" if vehicle.get("direction") in ("N", "S") else "EW"
=======
                nearest_axis = "NS" if vehicle["direction"] in ("N", "S") else "EW"
>>>>>>> master

        if nearest_axis is None:
            return False, None
        return True, nearest_axis

<<<<<<< HEAD
    def spawn_pedestrian(self, direction):
=======
    # Make one pedestrian with a start side and speed.
    def spawn_pedestrian(self, direction):
        # Pick a side, a crossing axis, and a start velocity.
>>>>>>> master
        variant = random.choice(["ped1", "ped2", "ped3", "ped4"])
        speed = 100.0
        horizontal_crosswalk_y = random.choice([320, 640])
        vertical_crosswalk_x = random.choice([810, 1200])

<<<<<<< HEAD
        # Spawn on sidewalks, not inside the roadway.
=======
>>>>>>> master
        if direction == "W":
            pos, axis, vel = [760, horizontal_crosswalk_y], "EW", [speed, 0]
        elif direction == "E":
            pos, axis, vel = [1160, horizontal_crosswalk_y], "EW", [-speed, 0]
        elif direction == "N":
            pos, axis, vel = [vertical_crosswalk_x, 350], "NS", [0, speed]
        elif direction == "S":
            pos, axis, vel = [vertical_crosswalk_x, 730], "NS", [0, -speed]
        else:
            return

        ped = Pedestrian(pos[0], pos[1], axis)
        ped.id = self.next_ped_id
        self.next_ped_id += 1
        ped.velocity = vel
        ped.variant = variant
        ped.direction = direction
<<<<<<< HEAD
        self.pedestrians.append(ped)
        self.stats["pedestrians_spawned"] += 1

    def update_pedestrians(self, dt, phase=None):
        phase = self.current_phase if phase is None else phase
        for pedestrian in self.pedestrians:
            if phase == ALL_RED:
                pedestrian.active = True
            elif phase in (NS_GREEN, NS_YELLOW) and pedestrian.axis == "NS":
                pedestrian.active = True
            elif phase in (EW_GREEN, EW_YELLOW) and pedestrian.axis == "EW":
                pedestrian.active = True
            else:
                pedestrian.active = False
            pedestrian.update(dt)
=======
        
        self.pedestrians.append(ped)
        self.stats["pedestrians_spawned"] += 1

    # Move pedestrians for the current light phase.
    def update_pedestrians(self, dt, phase=None):
        # Pedestrians move only when their axis is allowed to cross.
        phase = self.current_phase if phase is None else phase
        
        for ped in self.pedestrians:
            if phase == ALL_RED:
                ped.active = True
            elif phase in (NS_GREEN, NS_YELLOW) and ped.axis == "NS":
                ped.active = True
            elif phase in (EW_GREEN, EW_YELLOW) and ped.axis == "EW":
                ped.active = True
            else:
                ped.active = False
                
            ped.update(dt)
>>>>>>> master

        kept = [ped for ped in self.pedestrians if not ped.finished]
        self.stats["pedestrians_exited"] += len(self.pedestrians) - len(kept)
        self.pedestrians = kept

<<<<<<< HEAD
    def has_passed_stop_line(self, vehicle):
        direction = vehicle["direction"]
        if direction == "N":
            return vehicle["y"] > self.STOP_LINES["N"]
        if direction == "S":
            return vehicle["y"] < self.STOP_LINES["S"]
        if direction == "E":
            return vehicle["x"] < self.STOP_LINES["E"]
        if direction == "W":
            return vehicle["x"] > self.STOP_LINES["W"]
        return False

    def _get_distance_to_stop_line(self, vehicle):
        direction = vehicle["direction"]
        if direction == "N":
            return self.STOP_LINES["N"] - vehicle["y"]
        if direction == "S":
            return vehicle["y"] - self.STOP_LINES["S"]
        if direction == "E":
            return vehicle["x"] - self.STOP_LINES["E"]
        if direction == "W":
            return self.STOP_LINES["W"] - vehicle["x"]
        return 0.0

    def _get_distance_to_car_ahead(self, vehicle):
=======
    # Check whether a car already crossed its stop line.
    def has_passed_stop_line(self, vehicle):
        direction = vehicle["direction"]
        if direction == "N": return vehicle["y"] > self.STOP_LINES["N"]
        if direction == "S": return vehicle["y"] < self.STOP_LINES["S"]
        if direction == "E": return vehicle["x"] < self.STOP_LINES["E"]
        if direction == "W": return vehicle["x"] > self.STOP_LINES["W"]
        return False

    # Distance from the car to its stop line.
    def _get_distance_to_stop_line(self, vehicle):
        direction = vehicle["direction"]
        if direction == "N": return self.STOP_LINES["N"] - vehicle["y"]
        if direction == "S": return vehicle["y"] - self.STOP_LINES["S"]
        if direction == "E": return vehicle["x"] - self.STOP_LINES["E"]
        if direction == "W": return self.STOP_LINES["W"] - vehicle["x"]
        return 0.0

    # Nearest car ahead in the same lane.
    def _get_distance_to_car_ahead(self, vehicle):
        # Check only cars in the same lane and direction.
>>>>>>> master
        min_gap = float("inf")
        for other in self.vehicles:
            if other["id"] == vehicle["id"] or other["direction"] != vehicle["direction"]:
                continue
<<<<<<< HEAD
=======
                
>>>>>>> master
            if vehicle["direction"] == "N" and other["y"] > vehicle["y"]:
                gap = other["y"] - vehicle["y"]
            elif vehicle["direction"] == "S" and other["y"] < vehicle["y"]:
                gap = vehicle["y"] - other["y"]
            elif vehicle["direction"] == "E" and other["x"] < vehicle["x"]:
                gap = vehicle["x"] - other["x"]
            elif vehicle["direction"] == "W" and other["x"] > vehicle["x"]:
                gap = other["x"] - vehicle["x"]
            else:
                continue

<<<<<<< HEAD
            # Approximate lead car length.
            gap -= 90
            if gap < min_gap:
                min_gap = gap
        return min_gap

    def _is_pedestrian_in_crosswalk(self, pedestrian):
        px, py = pedestrian.position
        return (
            self.CROSSWALK_X_MIN <= px <= self.CROSSWALK_X_MAX
            and self.CROSSWALK_Y_MIN <= py <= self.CROSSWALK_Y_MAX
        )

    def _pedestrian_blocks_vehicle(self, vehicle, pedestrian):
        if not getattr(pedestrian, "active", False):
            return False
        if not self._is_pedestrian_in_crosswalk(pedestrian):
=======
            gap -= 90
            # Subtract the lead car length so the gap is bumper to bumper.
            if gap < min_gap:
                min_gap = gap
                
        return min_gap

    # See whether a pedestrian is inside the crosswalk area.
    def _is_pedestrian_in_crosswalk(self, pedestrian):
        px, py = pedestrian.position
        return (self.CROSSWALK_X_MIN <= px <= self.CROSSWALK_X_MAX 
                and self.CROSSWALK_Y_MIN <= py <= self.CROSSWALK_Y_MAX)

    # Decide if this pedestrian should block this car.
    def _pedestrian_blocks_vehicle(self, vehicle, pedestrian):
        if not pedestrian.active or not self._is_pedestrian_in_crosswalk(pedestrian):
>>>>>>> master
            return False

        px, py = pedestrian.position
        lane_half_width = VEHICLE_WIDTH / 2.0 + 6.0
        direction = vehicle["direction"]

<<<<<<< HEAD
=======
        # Only a simple lane overlap check here.
>>>>>>> master
        if direction == "N":
            same_lane = abs(px - vehicle["x"]) <= lane_half_width
            return same_lane and py >= vehicle["y"] and (py - vehicle["y"]) <= self.LOOKAHEAD_DISTANCE
        if direction == "S":
            same_lane = abs(px - vehicle["x"]) <= lane_half_width
            return same_lane and py <= vehicle["y"] and (vehicle["y"] - py) <= self.LOOKAHEAD_DISTANCE
        if direction == "E":
            same_lane = abs(py - vehicle["y"]) <= lane_half_width
            return same_lane and px <= vehicle["x"] and (vehicle["x"] - px) <= self.LOOKAHEAD_DISTANCE
        if direction == "W":
            same_lane = abs(py - vehicle["y"]) <= lane_half_width
            return same_lane and px >= vehicle["x"] and (px - vehicle["x"]) <= self.LOOKAHEAD_DISTANCE
        return False

<<<<<<< HEAD
    def _apply_signal_limit(self, vehicle, target_speed):
=======
    # Lower the target speed when the light is red.
    def _apply_signal_limit(self, vehicle, target_speed):
        # On red, slow down as the car gets near the stop line.
>>>>>>> master
        axis = "NS" if vehicle["direction"] in ("N", "S") else "EW"
        if self.green_axis == axis or self.has_passed_stop_line(vehicle):
            return target_speed

        distance = self._get_distance_to_stop_line(vehicle)
        if distance <= 10.0:
            return 0.0
        if distance < self.SIGNAL_BRAKE_DISTANCE:
            ratio = max(0.0, (distance - 10.0) / (self.SIGNAL_BRAKE_DISTANCE - 10.0))
            return min(target_speed, target_speed * ratio)
        return target_speed

<<<<<<< HEAD
    def _apply_following_limit(self, vehicle, target_speed):
        distance = self._get_distance_to_car_ahead(vehicle)
        desired_gap = max(FOLLOW_GAP, VEHICLE_LENGTH + self.SAFE_BUMPER_GAP)
=======
    # Lower the target speed if another car is too close.
    def _apply_following_limit(self, vehicle, target_speed):
        # Keep some space to the car in front.
        distance = self._get_distance_to_car_ahead(vehicle)
        desired_gap = max(FOLLOW_GAP, VEHICLE_LENGTH + self.SAFE_BUMPER_GAP)
        
>>>>>>> master
        if distance < desired_gap * 0.35:
            return 0.0
        if distance < desired_gap:
            return min(target_speed, target_speed * max(0.0, distance / desired_gap))
        return target_speed

<<<<<<< HEAD
    def _apply_pedestrian_limit(self, vehicle, target_speed):
        for pedestrian in self.pedestrians:
            if self._pedestrian_blocks_vehicle(vehicle, pedestrian):
                return 0.0
        return target_speed

    def _clamp_vehicle_to_stop_line_on_red(self, vehicle, prev_x, prev_y):
        axis = "NS" if vehicle["direction"] in ("N", "S") else "EW"
        if self.green_axis == axis:
            return
=======
    # Stop the car if a pedestrian is in its path.
    def _apply_pedestrian_limit(self, vehicle, target_speed):
        # One active pedestrian in the path is enough to stop the car.
        for ped in self.pedestrians:
            if self._pedestrian_blocks_vehicle(vehicle, ped):
                return 0.0
        return target_speed

    # Clamp a car back to the line if it drifted over on red.
    def _clamp_vehicle_to_stop_line_on_red(self, vehicle, prev_x, prev_y):
        # Extra safety: do not let a red-light car slide past the line.
        axis = "NS" if vehicle["direction"] in ("N", "S") else "EW"
        if self.green_axis == axis:
            return
            
>>>>>>> master
        if self.has_passed_stop_line({"direction": vehicle["direction"], "x": prev_x, "y": prev_y}):
            return

        direction = vehicle["direction"]
        if direction == "N" and vehicle["y"] > self.STOP_LINES["N"]:
<<<<<<< HEAD
            vehicle["y"] = self.STOP_LINES["N"]
            vehicle["position"][1] = vehicle["y"]
            vehicle["current_speed"] = 0.0
            vehicle["velocity"][1] = 0.0
        elif direction == "S" and vehicle["y"] < self.STOP_LINES["S"]:
            vehicle["y"] = self.STOP_LINES["S"]
            vehicle["position"][1] = vehicle["y"]
            vehicle["current_speed"] = 0.0
            vehicle["velocity"][1] = 0.0
        elif direction == "E" and vehicle["x"] < self.STOP_LINES["E"]:
            vehicle["x"] = self.STOP_LINES["E"]
            vehicle["position"][0] = vehicle["x"]
            vehicle["current_speed"] = 0.0
            vehicle["velocity"][0] = 0.0
        elif direction == "W" and vehicle["x"] > self.STOP_LINES["W"]:
            vehicle["x"] = self.STOP_LINES["W"]
            vehicle["position"][0] = vehicle["x"]
            vehicle["current_speed"] = 0.0
            vehicle["velocity"][0] = 0.0

    def _distance_axis_value(self, vehicle, direction):
        if direction in ("N", "S"):
            return vehicle["y"]
        return vehicle["x"]

    def _enforce_min_vehicle_gap(self):
        min_gap = VEHICLE_LENGTH + self.SAFE_BUMPER_GAP
        grouped = {direction: [] for direction in ("N", "S", "E", "W")}
=======
            vehicle["y"] = vehicle["position"][1] = self.STOP_LINES["N"]
            vehicle["current_speed"] = vehicle["velocity"][1] = 0.0
        elif direction == "S" and vehicle["y"] < self.STOP_LINES["S"]:
            vehicle["y"] = vehicle["position"][1] = self.STOP_LINES["S"]
            vehicle["current_speed"] = vehicle["velocity"][1] = 0.0
        elif direction == "E" and vehicle["x"] < self.STOP_LINES["E"]:
            vehicle["x"] = vehicle["position"][0] = self.STOP_LINES["E"]
            vehicle["current_speed"] = vehicle["velocity"][0] = 0.0
        elif direction == "W" and vehicle["x"] > self.STOP_LINES["W"]:
            vehicle["x"] = vehicle["position"][0] = self.STOP_LINES["W"]
            vehicle["current_speed"] = vehicle["velocity"][0] = 0.0

    # Main axis position used when sorting cars.
    def _distance_axis_value(self, vehicle, direction):
        return vehicle["y"] if direction in ("N", "S") else vehicle["x"]

    # Push cars apart if they ended up too close.
    def _enforce_min_vehicle_gap(self):
        # After movement, push trailing cars back if they got too close.
        min_gap = VEHICLE_LENGTH + self.SAFE_BUMPER_GAP
        grouped = {direction: [] for direction in ("N", "S", "E", "W")}
        
>>>>>>> master
        for vehicle in self.vehicles:
            direction = vehicle.get("direction")
            if direction in grouped:
                grouped[direction].append(vehicle)

<<<<<<< HEAD
        # For N/W larger coordinate means further ahead, for S/E smaller is ahead.
        for direction, vehicles in grouped.items():
            reverse = direction in ("N", "W")
            ordered = sorted(vehicles, key=lambda v: self._distance_axis_value(v, direction), reverse=reverse)
=======
        for direction, vehicles in grouped.items():
            reverse = direction in ("N", "W")
            ordered = sorted(vehicles, key=lambda v: self._distance_axis_value(v, direction), reverse=reverse)
            
>>>>>>> master
            for idx in range(1, len(ordered)):
                lead = ordered[idx - 1]
                trail = ordered[idx]
                lead_pos = self._distance_axis_value(lead, direction)
                trail_pos = self._distance_axis_value(trail, direction)

                if direction in ("N", "W"):
                    allowed = lead_pos - min_gap
                    if trail_pos > allowed:
                        if direction == "N":
<<<<<<< HEAD
                            trail["y"] = allowed
                            trail["position"][1] = allowed
                        else:
                            trail["x"] = allowed
                            trail["position"][0] = allowed
=======
                            trail["y"] = trail["position"][1] = allowed
                        else:
                            trail["x"] = trail["position"][0] = allowed
>>>>>>> master
                        trail["current_speed"] = min(trail.get("current_speed", 0.0), lead.get("current_speed", 0.0))
                else:
                    allowed = lead_pos + min_gap
                    if trail_pos < allowed:
                        if direction == "S":
<<<<<<< HEAD
                            trail["y"] = allowed
                            trail["position"][1] = allowed
                        else:
                            trail["x"] = allowed
                            trail["position"][0] = allowed
                        trail["current_speed"] = min(trail.get("current_speed", 0.0), lead.get("current_speed", 0.0))

    def step(self, dt):
        # Rules are applied in deterministic order: signal -> lead car -> pedestrians.
        for vehicle in self.vehicles:
            target_speed = float(vehicle["speed_val"])
=======
                            trail["y"] = trail["position"][1] = allowed
                        else:
                            trail["x"] = trail["position"][0] = allowed
                        trail["current_speed"] = min(trail.get("current_speed", 0.0), lead.get("current_speed", 0.0))

    # Move all cars for one frame.
    def step(self, dt):
        # Target speed comes from a few simple limits.
        for vehicle in self.vehicles:
            target_speed = vehicle["speed_val"]
>>>>>>> master
            target_speed = self._apply_signal_limit(vehicle, target_speed)
            target_speed = self._apply_following_limit(vehicle, target_speed)
            target_speed = self._apply_pedestrian_limit(vehicle, target_speed)

            current_speed = vehicle.get("current_speed", 0.0)
            if current_speed < target_speed:
                current_speed = min(current_speed + self.ACCEL * dt, target_speed)
            else:
                current_speed = max(current_speed - self.BRAKE * dt, target_speed)

            vehicle["current_speed"] = current_speed
<<<<<<< HEAD
            if vehicle["direction"] == "N":
                vehicle["velocity"] = [0, current_speed]
            elif vehicle["direction"] == "S":
                vehicle["velocity"] = [0, -current_speed]
            elif vehicle["direction"] == "E":
                vehicle["velocity"] = [-current_speed, 0]
            elif vehicle["direction"] == "W":
                vehicle["velocity"] = [current_speed, 0]
=======
            
            # Turn one speed value into a direction vector.
            if vehicle["direction"] == "N": vehicle["velocity"] = [0, current_speed]
            elif vehicle["direction"] == "S": vehicle["velocity"] = [0, -current_speed]
            elif vehicle["direction"] == "E": vehicle["velocity"] = [-current_speed, 0]
            elif vehicle["direction"] == "W": vehicle["velocity"] = [current_speed, 0]
>>>>>>> master

            prev_x, prev_y = vehicle["x"], vehicle["y"]
            vehicle["position"][0] += vehicle["velocity"][0] * dt
            vehicle["position"][1] += vehicle["velocity"][1] * dt
            vehicle["x"], vehicle["y"] = vehicle["position"][0], vehicle["position"][1]
<<<<<<< HEAD
            self._clamp_vehicle_to_stop_line_on_red(vehicle, prev_x, prev_y)
            vehicle["is_stopped"] = vehicle["current_speed"] <= 0.5

        # Final safety pass to prevent bumper-to-bumper overlaps.
        self._enforce_min_vehicle_gap()

        kept = [
            vehicle
            for vehicle in self.vehicles
            if self.DESPAWN_X_MIN <= vehicle["x"] <= self.DESPAWN_X_MAX
            and self.DESPAWN_Y_MIN <= vehicle["y"] <= self.DESPAWN_Y_MAX
        ]
        self.stats["vehicles_exited"] += len(self.vehicles) - len(kept)
        self.vehicles = kept

    def can_spawn(self, direction, x, y):
=======
            
            self._clamp_vehicle_to_stop_line_on_red(vehicle, prev_x, prev_y)
            vehicle["is_stopped"] = vehicle["current_speed"] <= 0.5

        self._enforce_min_vehicle_gap()

        # Drop vehicles that left the map area.
        kept = [
            v for v in self.vehicles
            if self.DESPAWN_X_MIN <= v["x"] <= self.DESPAWN_X_MAX
            and self.DESPAWN_Y_MIN <= v["y"] <= self.DESPAWN_Y_MAX
        ]
        
        self.stats["vehicles_exited"] += len(self.vehicles) - len(kept)
        self.vehicles = kept

    # Check if the spawn point has enough free space.
    def can_spawn(self, direction, x, y):
        # Do not spawn on top of another car.
>>>>>>> master
        for vehicle in self.vehicles:
            if abs(vehicle["x"] - x) < 120 and abs(vehicle["y"] - y) < 120:
                return False
        return True

<<<<<<< HEAD
    def spawn_vehicle(self, direction, x, y, speed):
        self.next_id += 1
        vehicle = create_car(self.next_id, x, y, 0, 0, direction)
        vehicle.update(
            {"speed_val": speed, "position": [x, y], "current_speed": speed, "x": x, "y": y}
        )
        self.vehicles.append(vehicle)
        self.stats["vehicles_spawned"] += 1

    def spawn_emergency(self, direction, x, y, speed, sirens_on=True):
        self.next_id += 1
        vehicle = create_emergency_vehicle(self.next_id, x, y, 0, 0, direction)
        vehicle.update(
            {
                "speed_val": speed,
                "position": [x, y],
                "current_speed": speed,
                "x": x,
                "y": y,
                "sirens_on": sirens_on,
            }
        )
=======
    # Create and add one normal car.
    def spawn_vehicle(self, direction, x, y, speed):
        # Store both a position list and x/y fields because older code uses both.
        self.next_id += 1
        vehicle = create_car(self.next_id, x, y, 0, 0, direction)
        vehicle.update({
            "speed_val": speed, 
            "position": [x, y], 
            "current_speed": speed, 
            "x": x, 
            "y": y
        })
        self.vehicles.append(vehicle)
        self.stats["vehicles_spawned"] += 1

    # Create and add one emergency car.
    def spawn_emergency(self, direction, x, y, speed, sirens_on=True):
        # This keeps the usual car fields plus siren data.
        self.next_id += 1
        vehicle = create_emergency_vehicle(self.next_id, x, y, 0, 0, direction)
        vehicle.update({
            "speed_val": speed,
            "position": [x, y],
            "current_speed": speed,
            "x": x,
            "y": y,
            "sirens_on": sirens_on,
        })
>>>>>>> master
        self.vehicles.append(vehicle)
        self.stats["vehicles_spawned"] += 1
