from __future__ import annotations

from sim.map import CAMERA_ZONES, in_rect
from mqtt.client import MqttClient
from mqtt.topics import LANES, TopicRegistry


class SensorNode:
    """Smart camera node that scans lane rectangles and publishes telemetry."""

    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics

    def publish_snapshots(self, world, timestamp: float) -> None:
        for lane in LANES:
            zone = CAMERA_ZONES[lane]

            vehicles = []
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
            self.client.publish(self.topics.camera_snapshot(lane), payload)
