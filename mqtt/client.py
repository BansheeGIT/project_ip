from __future__ import annotations

import json
from typing import Any, Callable

from .security import FernetSecurity, SecurityError
from .transport import BrokerTransport, LocalBrokerTransport


MessageHandler = Callable[[str, dict], None]
LocalBroker = LocalBrokerTransport


class MqttClient:
    """MQTT client wrapper with optional Fernet payload encryption."""

    def __init__(
        self,
        broker: BrokerTransport,
        client_id: str,
        security: FernetSecurity | None = None,
    ) -> None:
        self.broker = broker
        self.client_id = client_id
        self.security = security

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
                return None

        if isinstance(wire_payload, dict):
            return wire_payload
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
        self.broker.close()
