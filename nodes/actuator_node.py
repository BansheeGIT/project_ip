from __future__ import annotations

from mqtt.client import MqttClient
from mqtt.schemas import validate_signal_payload
from mqtt.topics import SIGNAL_APPLIED, SIGNAL_COMMAND


class ActuatorNode:
    """Applies signal commands to the simulation world."""

    def __init__(self, client: MqttClient) -> None:
        self.client = client
        self.current_phase = None
        self.last_reason = ""
        self.client.subscribe(SIGNAL_COMMAND, self._on_command)

    def _on_command(self, _topic: str, payload: dict) -> None:
        command = validate_signal_payload(payload)
        self.current_phase = command.phase
        self.last_reason = command.reason
        self.client.publish(
            SIGNAL_APPLIED,
            {
                "timestamp": command.timestamp,
                "mode": command.mode,
                "phase": command.phase,
                "reason": command.reason,
            },
        )
