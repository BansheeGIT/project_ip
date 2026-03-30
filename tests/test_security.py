import pytest

from mqtt.client import LocalBroker, MqttClient
from mqtt.security import FernetSecurity, is_fernet_available
from mqtt.schemas import validate_camera_payload
from mqtt.topics import TopicRegistry, camera_snapshot_topic
from nodes.actuator_node import ActuatorNode
from nodes.controller_node import ControllerNode
from traffic.phases import EW_GREEN

# Missing camera fields should raise an error.
def test_camera_payload_validation_requires_fields():
    with pytest.raises(ValueError):
        validate_camera_payload({"lane": "N"})

# One siren should be enough to change the smart decision.
def test_smart_controller_prioritizes_siren_axis():
    broker = LocalBroker()
    topics = TopicRegistry(prefix="test/security")
    client = MqttClient(broker, "test")
    controller = ControllerNode(client, topics)
    actuator = ActuatorNode(client, topics)

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
        client.publish(topics.camera_snapshot(lane), payload)

    phase = controller.decide(dt=0.1, timestamp=1.0)
    assert phase == EW_GREEN
    assert actuator.current_phase == EW_GREEN

@pytest.mark.skipif(not is_fernet_available(), reason="cryptography is not installed")
# Same key should let encrypted messages round-trip.
def test_encrypted_publish_subscribe_roundtrip():
    broker = LocalBroker()
    key = FernetSecurity.generate_key()
    security = FernetSecurity(key=key)
    publisher = MqttClient(broker, "publisher", security=security)
    subscriber = MqttClient(broker, "subscriber", security=security)

    received = []
    subscriber.subscribe("demo/topic", lambda _topic, payload: received.append(payload))
    publisher.publish("demo/topic", {"value": 42, "ok": True})

    assert received == [{"value": 42, "ok": True}]

@pytest.mark.skipif(not is_fernet_available(), reason="cryptography is not installed")
# Wrong keys should drop the encrypted message.
def test_encrypted_message_dropped_with_wrong_key():
    broker = LocalBroker()
    key_a = FernetSecurity.generate_key()
    key_b = FernetSecurity.generate_key()
    publisher = MqttClient(broker, "publisher", security=FernetSecurity(key=key_a))
    subscriber = MqttClient(broker, "subscriber", security=FernetSecurity(key=key_b))

    received = []
    subscriber.subscribe("demo/topic", lambda _topic, payload: received.append(payload))
    publisher.publish("demo/topic", {"value": "secret"})

    assert received == []
