<<<<<<< HEAD
from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, Callable

from .security import FernetSecurity, SecurityError


MessageHandler = Callable[[str, dict], None]
WireHandler = Callable[[str, Any], None]


class LocalBroker:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[WireHandler]] = defaultdict(list)

    def start(self) -> None:
        return

    def subscribe(self, topic: str, handler: WireHandler) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: Any) -> None:
        for handler in list(self._subscribers.get(topic, [])):
            handler(topic, payload)

    def close(self) -> None:
        self._subscribers.clear()


class MqttClient:
    """MQTT wrapper with optional Fernet payload encryption."""

    def __init__(
        self,
        broker: Any,
        client_id: str,
        security: FernetSecurity | None = None,
    ) -> None:
=======
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
>>>>>>> master
        self.broker = broker
        self.client_id = client_id
        self.security = security

<<<<<<< HEAD
    def _encode_payload(self, payload: dict) -> bytes:
        if self.security is not None:
            return self.security.encrypt_payload(payload)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    def _decode_payload(self, wire_payload: Any) -> dict | None:
        if self.security is not None:
            if not isinstance(wire_payload, (bytes, bytearray)):
                return None
            try:
                return self.security.decrypt_payload(bytes(wire_payload))
            except SecurityError:
=======
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
>>>>>>> master
                return None

        if isinstance(wire_payload, dict):
            return wire_payload
<<<<<<< HEAD
        if isinstance(wire_payload, bytearray):
            wire_payload = bytes(wire_payload)
        if isinstance(wire_payload, bytes):
            try:
                decoded = json.loads(wire_payload.decode("utf-8"))
            except Exception:
                return None
            return decoded if isinstance(decoded, dict) else None
        if isinstance(wire_payload, str):
            try:
                decoded = json.loads(wire_payload)
            except Exception:
                return None
            return decoded if isinstance(decoded, dict) else None
        return None

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        def wrapped(_topic: str, wire_payload: Any) -> None:
            payload = self._decode_payload(wire_payload)
            if payload is None:
                return
            handler(_topic, payload)

        self.broker.subscribe(topic, wrapped)

    def publish(self, topic: str, payload: dict) -> None:
        self.broker.publish(topic, self._encode_payload(payload))

    def close(self) -> None:
=======
            
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
>>>>>>> master
        self.broker.close()
