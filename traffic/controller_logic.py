from .phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW

class TrafficController:
    def __init__(self):
        self.current_phase = NS_GREEN
        self.next_green_phase = None
        self.timer = 0.0
        self.GREEN_TIME = 20.0
        self.YELLOW_TIME = 2.0
        self.ALL_RED_TIME = 1.0
        self.emergency_active = False
        self.emergency_axis = None

    def set_preemption(self, active, axis=None):
        self.emergency_active = active
        self.emergency_axis = axis

    def _start_transition(self):
        if self.current_phase == NS_GREEN:
            self.current_phase = NS_YELLOW
            self.next_green_phase = EW_GREEN
        elif self.current_phase == EW_GREEN:
            self.current_phase = EW_YELLOW
            self.next_green_phase = NS_GREEN
        self.timer = 0.0

    def decide(self, dt, queue_ns, queue_ew):
        if self.emergency_active and self.emergency_axis:
            self.current_phase = NS_GREEN if self.emergency_axis == "NS" else EW_GREEN
            self.timer = 0.0
            return self.current_phase

        self.timer += dt
        if self.current_phase in (NS_GREEN, EW_GREEN):
            if self.timer >= self.GREEN_TIME:
                self._start_transition()
        elif self.current_phase in (NS_YELLOW, EW_YELLOW):
            if self.timer >= self.YELLOW_TIME:
                self.current_phase = ALL_RED
                self.timer = 0.0
        elif self.current_phase == ALL_RED:
            if self.timer >= self.ALL_RED_TIME:
                self.current_phase = self.next_green_phase or NS_GREEN
                self.timer = 0.0
        return self.current_phase

    def switch_phase(self):
        if not self.emergency_active: self._start_transition()
