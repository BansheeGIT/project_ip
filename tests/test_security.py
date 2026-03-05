import pytest

from mqtt.client import LocalBroker, MqttClient
from mqtt.schemas import validate_camera_payload
from mqtt.topics import camera_snapshot_topic
from nodes.actuator_node import ActuatorNode
from nodes.controller_node import ControllerNode
from traffic.phases import EW_GREEN


def test_camera_payload_validation_requires_fields():
    with pytest.raises(ValueError):
        validate_camera_payload({"lane": "N"})


def test_smart_controller_prioritizes_siren_axis():
    broker = LocalBroker()
    client = MqttClient(broker, "test")
    controller = ControllerNode(client)
    actuator = ActuatorNode(client)

    base = {
        "timestamp": 1.0,
        "vehicle_count": 1,
        "stopped_vehicle_count": 0,
        "pedestrian_count": 0,
        "emergency_vehicle_count": 0,
        "emergency_siren_count": 0,
    }

    for lane in ("N", "S", "E", "W"):
        payload = dict(base)
        payload["lane"] = lane
        if lane == "E":
            payload["emergency_vehicle_count"] = 1
            payload["emergency_siren_count"] = 1
        client.publish(camera_snapshot_topic(lane), payload)

    phase = controller.decide(dt=0.1, timestamp=1.0)
    assert phase == EW_GREEN
    assert actuator.current_phase == EW_GREEN
