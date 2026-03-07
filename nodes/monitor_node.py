from __future__ import annotations

from collections import deque

from mqtt.client import MqttClient
from mqtt.topics import TopicRegistry


class MonitorNode:
    """Collects latest signal events for debugging/telemetry panel."""

    def __init__(self, client: MqttClient, topics: TopicRegistry, max_events: int = 10) -> None:
        self.client = client
        self.topics = topics
        self.events = deque(maxlen=max_events)
        self.client.subscribe(self.topics.signal_applied, self._on_applied)

    def _on_applied(self, _topic: str, payload: dict) -> None:
        self.events.append(payload)

    def latest_reason(self) -> str:
        if not self.events:
            return ""
        return str(self.events[-1].get("reason", ""))
