import json
from collections import defaultdict
from typing import Callable

import paho.mqtt.client as mqtt


DEFAULT_MQTT_HOST = "broker.hivemq.com"
DEFAULT_MQTT_PORT = 1883
DEFAULT_KEEPALIVE = 60


class MqttClient:
    # Network MQTT client backed by broker.hivemq.com.
    def __init__(
        self,
        client_id: str,
        security=None,
        host: str = DEFAULT_MQTT_HOST,
        port: int = DEFAULT_MQTT_PORT,
        keepalive: int = DEFAULT_KEEPALIVE,
    ):
        self.client_id = client_id
        self.security = security
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self._handlers: dict[str, list[Callable[[str, dict], None]]] = defaultdict(list)

        self._client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect_async(self.host, self.port, self.keepalive)
        self._client.loop_start()

    # Turn a Python dict into the wire format.
    def _encode_payload(self, payload: dict) -> bytes:
        if self.security:
            return self.security.encrypt_payload(payload)
        return json.dumps(payload).encode("utf-8")

    # Turn the wire format back into a Python dict.
    def _decode_payload(self, wire_payload):
        if self.security:
            try:
                return self.security.decrypt_payload(wire_payload)
            except Exception:
                return None

        if isinstance(wire_payload, dict):
            return wire_payload

        if isinstance(wire_payload, bytes):
            wire_payload = wire_payload.decode("utf-8")

        try:
            return json.loads(wire_payload)
        except Exception:
            return None

    def _on_connect(self, _client, _userdata, _flags, rc):
        if rc != 0:
            return
        for topic in self._handlers:
            self._client.subscribe(topic)

    def _on_message(self, _client, _userdata, msg):
        payload = self._decode_payload(msg.payload)
        if payload is None:
            return

        for handler in list(self._handlers.get(msg.topic, [])):
            handler(msg.topic, payload)

    # Subscribe and auto-decode messages for the caller.
    def subscribe(self, topic, handler):
        self._handlers[topic].append(handler)
        self._client.subscribe(topic)

    # Encode and publish one message.
    def publish(self, topic, payload: dict):
        self._client.publish(topic, self._encode_payload(payload))

    # Close the broker link.
    def close(self):
        self._client.loop_stop()
        self._client.disconnect()
