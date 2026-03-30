from __future__ import annotations

from sim.map import CAMERA_ZONES, in_rect
from mqtt.client import MqttClient
from mqtt.topics import LANES, TopicRegistry


<<<<<<< HEAD
class SensorNode:
    """Smart camera node that scans lane rectangles and publishes telemetry."""

=======
# Sensor node turns world objects into lane counts.
class SensorNode:
    # Save MQTT links used for camera snapshots.
>>>>>>> master
    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics

<<<<<<< HEAD
    def publish_snapshots(self, world, timestamp: float) -> None:
=======
    # Publish one summary for each lane.
    def publish_snapshots(self, world, timestamp: float) -> None:
        # Each lane gets one small camera-like summary.
>>>>>>> master
        for lane in LANES:
            zone = CAMERA_ZONES[lane]

            vehicles = []
<<<<<<< HEAD
            for vehicle in world.vehicles:
                if vehicle.get("direction") != lane:
                    continue
                if in_rect((vehicle["x"], vehicle["y"]), zone):
                    vehicles.append(vehicle)

            pedestrians = [
                ped
                for ped in world.pedestrians
                if in_rect((ped.position[0], ped.position[1]), zone)
            ]

            payload = {
                "lane": lane,
                "timestamp": float(timestamp),
                "vehicle_count": len(vehicles),
                "stopped_vehicle_count": sum(1 for v in vehicles if v.get("is_stopped", False)),
                "pedestrian_count": len(pedestrians),
                "emergency_vehicle_count": sum(1 for v in vehicles if v.get("type") == "emergency"),
                "emergency_siren_count": sum(
                    1
                    for v in vehicles
                    if v.get("type") == "emergency" and v.get("sirens_on", False)
                ),
            }
=======
            for v in world.vehicles:
                if v.get("direction") != lane:
                    continue
                if in_rect((v["x"], v["y"]), zone):
                    vehicles.append(v)

            pedestrians = [
                p for p in world.pedestrians
                if in_rect((p.position[0], p.position[1]), zone)
            ]

            # Send counts, not whole objects.
            payload = {
                "lane": lane,
                "timestamp": timestamp,
                "vehicle_count": len(vehicles),
                "stopped_vehicle_count": sum(1 for v in vehicles if v.get("is_stopped")),
                "pedestrian_count": len(pedestrians),
                "emergency_vehicle_count": sum(1 for v in vehicles if v.get("type") == "emergency"),
                "emergency_siren_count": sum(
                    1 for v in vehicles 
                    if v.get("type") == "emergency" and v.get("sirens_on")
                ),
            }
            
>>>>>>> master
            self.client.publish(self.topics.camera_snapshot(lane), payload)
