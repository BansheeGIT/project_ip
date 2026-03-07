from __future__ import annotations

from mqtt.client import MqttClient
from mqtt.schemas import validate_signal_payload
from mqtt.topics import TopicRegistry


class ActuatorNode:
    """Applies signal commands to the simulation world."""

    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics
        self.current_phase = None
        self.last_reason = ""
        self.client.subscribe(self.topics.signal_command, self._on_command)

    def _on_command(self, _topic: str, payload: dict) -> None:
        command = validate_signal_payload(payload)
        self.current_phase = command.phase
        self.last_reason = command.reason
        self.client.publish(
            self.topics.signal_applied,
            {
                "timestamp": command.timestamp,
                "mode": command.mode,
                "phase": command.phase,
                "reason": command.reason,
            },
        )
