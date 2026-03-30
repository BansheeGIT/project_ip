from __future__ import annotations

from collections import deque

from mqtt.client import MqttClient
from mqtt.topics import TopicRegistry


# Monitor node keeps a short list of smart actions.
class MonitorNode:
    # UI only needs a short smart-action history.
    # Keep the links and the history size.
    def __init__(self, client: MqttClient, topics: TopicRegistry, max_events: int = 10) -> None:
        self.client = client
        self.topics = topics
        self.events = deque(maxlen=max_events)
        
        self.client.subscribe(self.topics.signal_applied, self._on_applied)

    # Push one applied event into the history.
    def _on_applied(self, _topic: str, payload: dict) -> None:
        self.events.append(payload)

    # Give back the reason from the newest event.
    def latest_reason(self) -> str:
        if not self.events:
            return ""
            
        return self.events[-1].get("reason", "")
