from __future__ import annotations

from collections import defaultdict
from typing import Callable


MessageHandler = Callable[[str, dict], None]


class LocalBroker:
    """In-process pub/sub broker to emulate MQTT topic routing."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[MessageHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: dict) -> None:
        for handler in list(self._subscribers.get(topic, [])):
            handler(topic, payload)


class MqttClient:
    """Minimal client wrapper used by nodes."""

    def __init__(self, broker: LocalBroker, client_id: str) -> None:
        self.broker = broker
        self.client_id = client_id

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        self.broker.subscribe(topic, handler)

    def publish(self, topic: str, payload: dict) -> None:
        self.broker.publish(topic, payload)
