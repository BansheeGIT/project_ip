from __future__ import annotations

from sim.map import CAMERA_ZONES, in_rect
from mqtt.client import MqttClient
from mqtt.topics import LANES, TopicRegistry


# Sensor node turns world objects into lane counts.
class SensorNode:
    # Save MQTT links used for camera snapshots.
    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics

    # Publish one summary for each lane.
    def publish_snapshots(self, world, timestamp: float) -> None:
        # Each lane gets one small camera-like summary.
        for lane in LANES:
            zone = CAMERA_ZONES[lane]

            vehicles = []
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
            
            self.client.publish(self.topics.camera_snapshot(lane), payload)
