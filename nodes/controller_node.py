from __future__ import annotations

from mqtt.client import MqttClient
from mqtt.schemas import validate_camera_payload
from mqtt.topics import LANES, TopicRegistry
from traffic.phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW

# Smart controller node chooses phases from camera data.
class ControllerNode:
    # This one makes smart decisions from camera snapshots.
    GREEN_TIME = 14.0
    YELLOW_TIME = 2.0
    ALL_RED_TIME = 1.0
    PEDESTRIAN_WEIGHT = 0.35

    # Keep MQTT links and blank lane data.
    def __init__(self, client: MqttClient, topics: TopicRegistry) -> None:
        self.client = client
        self.topics = topics
        self.current_phase = NS_GREEN
        self.next_green_phase = None
        self.timer = 0.0
        
        # Blank lane data lets scoring work before real messages come in.
        self._latest_by_lane = {
            lane: {
                "lane": lane,
                "timestamp": 0.0,
                "vehicle_count": 0,
                "stopped_vehicle_count": 0,
                "pedestrian_count": 0,
                "emergency_vehicle_count": 0,
                "emergency_siren_count": 0,
            }
            for lane in LANES
        }

        for lane in LANES:
            self.client.subscribe(self.topics.camera_snapshot(lane), self._on_camera_snapshot)

    # Latest camera message wins for a lane.
    def _on_camera_snapshot(self, _topic: str, payload: dict) -> None:
        # Older payloads get replaced by newer ones.
        snapshot = validate_camera_payload(payload)
        self._latest_by_lane[snapshot.lane] = payload

    # Turn one axis into one score number.
    def _axis_score(self, axis: str) -> float:
        # More cars, stopped cars, and pedestrians push the score up.
        lanes = ("N", "S") if axis == "NS" else ("E", "W")
        score = 0.0
        for lane in lanes:
            data = self._latest_by_lane[lane]
            score += data["vehicle_count"]
            score += data["stopped_vehicle_count"] * 0.6
            score += data["pedestrian_count"] * self.PEDESTRIAN_WEIGHT
        return score

    # Count active sirens on one axis.
    def _axis_has_siren(self, axis: str) -> int:
        # Any siren on an axis can take control right away.
        lanes = ("N", "S") if axis == "NS" else ("E", "W")
        return sum(self._latest_by_lane[lane]["emergency_siren_count"] for lane in lanes)

    # Begin the safe move to the other green phase.
    def _start_transition(self) -> None:
        # Green goes to yellow first, then to all-red, then the next green.
        if self.current_phase == NS_GREEN:
            self.current_phase = NS_YELLOW
            self.next_green_phase = EW_GREEN
        elif self.current_phase == EW_GREEN:
            self.current_phase = EW_YELLOW
            self.next_green_phase = NS_GREEN
        self.timer = 0.0

    # Publish the chosen phase and the reason for it.
    def _emit(self, timestamp: float, reason: str) -> str:
        self.client.publish(
            self.topics.signal_command,
            {
                "timestamp": timestamp,
                "mode": "mqtt-smart",
                "phase": self.current_phase,
                "reason": reason,
            },
        )
        return self.current_phase

    # Decide which phase should be active now.
    def decide(self, dt: float, timestamp: float) -> str:
        siren_ns = self._axis_has_siren("NS")
        siren_ew = self._axis_has_siren("EW")

        # Sirens beat the normal scoring logic.
        if siren_ns or siren_ew:
            target = NS_GREEN if siren_ns >= siren_ew else EW_GREEN
            if self.current_phase != target:
                self.current_phase = target
                self.next_green_phase = None
                self.timer = 0.0
                return self._emit(timestamp, "siren_priority")
            
            self.timer = 0.0
            return self._emit(timestamp, "siren_hold")

        self.timer += dt
        
        # Without sirens, we switch only when the timer says it is time.
        if self.current_phase in (NS_GREEN, EW_GREEN):
            if self.timer >= self.GREEN_TIME:
                ns_score = self._axis_score("NS")
                ew_score = self._axis_score("EW")
                desired_green = NS_GREEN if ns_score >= ew_score else EW_GREEN
                
                if desired_green != self.current_phase:
                    self._start_transition()
                    return self._emit(timestamp, "score_switch")
                
                self.timer = 0.0
                return self._emit(timestamp, "score_hold")
                
        elif self.current_phase in (NS_YELLOW, EW_YELLOW):
            if self.timer >= self.YELLOW_TIME:
                self.current_phase = ALL_RED
                self.timer = 0.0
                return self._emit(timestamp, "yellow_to_all_red")
                
        elif self.current_phase == ALL_RED:
            if self.timer >= self.ALL_RED_TIME:
                self.current_phase = self.next_green_phase or NS_GREEN
                self.timer = 0.0
                return self._emit(timestamp, "all_red_to_green")

        return self._emit(timestamp, "steady")
