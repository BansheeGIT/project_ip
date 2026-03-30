import json
from collections import defaultdict

# Tiny fake broker for one local sim.
class LocalBroker:
    # Start with an empty topic table.
    def __init__(self):
        self._subscribers = defaultdict(list)

    # This stays here so the fake broker looks real enough.
    def start(self):
        pass

    # Add one handler to one topic.
    def subscribe(self, topic, handler):
        self._subscribers[topic].append(handler)

    # Send one payload to every handler on that topic.
    def publish(self, topic, payload):
        # Use a copy in case a handler changes subscriptions mid-loop.
        for handler in list(self._subscribers.get(topic, [])):
            handler(topic, payload)

    # Remove all local subscriptions.
    def close(self):
        self._subscribers.clear()

# This helper sends and receives MQTT-like messages.
class MqttClient:
    # Security is optional. If it exists, payloads are encrypted first.
    # Keep broker, id, and optional security helper close by.
    def __init__(self, broker, client_id, security=None):
        self.broker = broker
        self.client_id = client_id
        self.security = security

    # Turn a Python dict into the wire format.
    def _encode_payload(self, payload: dict):
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
            
        try:
            return json.loads(wire_payload)
        except Exception:
            return None

    # Subscribe and auto-decode messages for the caller.
    def subscribe(self, topic, handler):
        # This small wrapper hides decode problems from the caller.
        def wrapped(_topic, wire_payload):
            # Decode before the real handler sees the message.
            payload = self._decode_payload(wire_payload)
            if payload is not None:
                handler(_topic, payload)

        self.broker.subscribe(topic, wrapped)

    # Encode and publish one message.
    def publish(self, topic, payload: dict):
        self.broker.publish(topic, self._encode_payload(payload))

    # Close the broker link.
    def close(self):
        self.broker.close()
