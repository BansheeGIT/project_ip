import pytest

from mqtt.client import MqttClient
from mqtt.security import FernetSecurity, is_fernet_available
from mqtt.schemas import validate_camera_payload
from mqtt.topics import TopicRegistry
from nodes.actuator_node import ActuatorNode
from nodes.controller_node import ControllerNode
from traffic.phases import EW_GREEN


class _FakePahoMessage:
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload


class _FakePahoBroker:
    def __init__(self):
        self.clients = []

    def register(self, client):
        self.clients.append(client)

    def publish(self, topic, payload):
        for client in self.clients:
            if topic in client.subscriptions and client.on_message:
                client.on_message(client, None, _FakePahoMessage(topic, payload))


class _FakePahoClient:
    def __init__(self, client_id=None, protocol=None):
        self.client_id = client_id
        self.protocol = protocol
        self.subscriptions = set()
        self.on_connect = None
        self.on_message = None
        self._broker = _FakePahoBrokerSingleton.INSTANCE

    def connect(self, host, port, keepalive):
        self._broker.register(self)
        if self.on_connect:
            self.on_connect(self, None, None, 0)

    def connect_async(self, host, port, keepalive):
        self.connect(host, port, keepalive)

    def loop_start(self):
        return None

    def subscribe(self, topic):
        self.subscriptions.add(topic)

    def publish(self, topic, payload):
        self._broker.publish(topic, payload)

    def loop_stop(self):
        return None

    def disconnect(self):
        return None


class _FakePahoBrokerSingleton:
    INSTANCE = _FakePahoBroker()


@pytest.fixture(autouse=True)
def _patch_mqtt_client(monkeypatch):
    import mqtt.client as mqtt_client_module

    # Fresh broker per test case.
    _FakePahoBrokerSingleton.INSTANCE = _FakePahoBroker()
    monkeypatch.setattr(mqtt_client_module.mqtt, "Client", _FakePahoClient)


# Missing camera fields should raise an error.
def test_camera_payload_validation_requires_fields():
    with pytest.raises(ValueError):
        validate_camera_payload({"lane": "N"})


# One siren should be enough to change the smart decision.
def test_smart_controller_prioritizes_siren_axis():
    topics = TopicRegistry(prefix="test/security")
    client = MqttClient(client_id="test")
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
    key = FernetSecurity.generate_key()
    security = FernetSecurity(key=key)
    publisher = MqttClient(client_id="publisher", security=security)
    subscriber = MqttClient(client_id="subscriber", security=security)

    received = []
    subscriber.subscribe("demo/topic", lambda _topic, payload: received.append(payload))
    publisher.publish("demo/topic", {"value": 42, "ok": True})

    assert received == [{"value": 42, "ok": True}]


@pytest.mark.skipif(not is_fernet_available(), reason="cryptography is not installed")
# Wrong keys should drop the encrypted message.
def test_encrypted_message_dropped_with_wrong_key():
    key_a = FernetSecurity.generate_key()
    key_b = FernetSecurity.generate_key()
    publisher = MqttClient(client_id="publisher", security=FernetSecurity(key=key_a))
    subscriber = MqttClient(client_id="subscriber", security=FernetSecurity(key=key_b))

    received = []
    subscriber.subscribe("demo/topic", lambda _topic, payload: received.append(payload))
    publisher.publish("demo/topic", {"value": "secret"})

    assert received == []
