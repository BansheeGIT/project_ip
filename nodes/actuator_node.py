from __future__ import annotations

from mqtt.client import MqttClient
from mqtt.schemas import validate_signal_payload
from mqtt.topics import TopicRegistry

# Actuator node applies chosen phases to the sim.
class ActuatorNode:
    # The actuator is simple here: remember the latest phase and echo it back.
    # Keep the client links and start listening.
    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics
        self.current_phase = None
        self.last_reason = ""
        
        self.client.subscribe(self.topics.signal_command, self._on_command)

    # Apply one command and publish an "applied" event.
    def _on_command(self, _topic: str, payload: dict) -> None:
        command = validate_signal_payload(payload)
        
        self.current_phase = command.phase
        self.last_reason = command.reason
        
        self.client.publish(self.topics.signal_applied, payload)
