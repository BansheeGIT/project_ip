from .phases import ALL_RED, EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW


# Fixed-time light logic lives here.
class TrafficController:
    # Plain fixed controller, no smart scoring here.
    # It begins with north-south green.
    GREEN_TIME = 20.0
    YELLOW_TIME = 2.0
    ALL_RED_TIME = 1.0

    # Save current light state and emergency info here.
    def __init__(self):
        self.current_phase = NS_GREEN
        self.next_green_phase = None
        self.timer = 0.0
        
        self.emergency_active = False
        self.emergency_axis = None

    # Tell the controller if emergency override is active.
    def set_preemption(self, active, axis=None):
        self.emergency_active = active
        self.emergency_axis = axis

    # Start the move to the other green side.
    def _start_transition(self):
        # Green never jumps straight to the other green.
        if self.current_phase == NS_GREEN:
            self.current_phase, self.next_green_phase = NS_YELLOW, EW_GREEN
        elif self.current_phase == EW_GREEN:
            self.current_phase, self.next_green_phase = EW_YELLOW, NS_GREEN
            
        self.timer = 0.0

    # Pick the next light state for this step.
    def decide(self, dt, queue_ns, queue_ew): 
        # queue_ns and queue_ew stay here so both controllers share one API.
        if self.emergency_active and self.emergency_axis:
            target = NS_GREEN if self.emergency_axis == "NS" else EW_GREEN
            if self.current_phase != target:
                self.current_phase = target
            self.timer = 0.0
            return self.current_phase

        self.timer += dt
        # This part is just a tiny state machine for light changes.

        if self.current_phase in (NS_GREEN, EW_GREEN) and self.timer >= self.GREEN_TIME:
            self._start_transition()
            
        elif self.current_phase in (NS_YELLOW, EW_YELLOW) and self.timer >= self.YELLOW_TIME:
            self.current_phase = ALL_RED
            self.timer = 0.0
            
        elif self.current_phase == ALL_RED and self.timer >= self.ALL_RED_TIME:
            self.current_phase = self.next_green_phase or NS_GREEN
            self.timer = 0.0

        return self.current_phase

    # Manually force a phase switch when allowed.
    def switch_phase(self):
        if not self.emergency_active:
            self._start_transition()
