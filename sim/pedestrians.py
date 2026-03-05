# sim/pedestrians.py
class Pedestrian:
    def __init__(self, x, y, axis):
        self.position = [float(x), float(y)]
        self.axis = axis
        self.speed = 100.0
        self.active = False
        self.finished = False
        self.variant = "ped1"
        self.direction = "N"
        self.velocity = [0.0, 0.0]

        # Curb lines where pedestrians must wait on red.
        self.WAIT_Y_TOP = 405.0
        self.WAIT_Y_BOTTOM = 675.0
        self.WAIT_X_LEFT = 815.0
        self.WAIT_X_RIGHT = 1095.0

    def _hold_at_curb(self):
        if self.axis == "NS":
            if self.velocity[1] > 0 and self.position[1] >= self.WAIT_Y_TOP:
                self.position[1] = self.WAIT_Y_TOP
                return True
            if self.velocity[1] < 0 and self.position[1] <= self.WAIT_Y_BOTTOM:
                self.position[1] = self.WAIT_Y_BOTTOM
                return True
            return False

        if self.axis == "EW":
            if self.velocity[0] > 0 and self.position[0] >= self.WAIT_X_LEFT:
                self.position[0] = self.WAIT_X_LEFT
                return True
            if self.velocity[0] < 0 and self.position[0] <= self.WAIT_X_RIGHT:
                self.position[0] = self.WAIT_X_RIGHT
                return True
            return False

        return False

    def update(self, dt):
        if self.finished:
            return

        # On red, walk to the curb and wait without stepping onto the road.
        if not self.active and self._hold_at_curb():
            return

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        if not (-200 < self.position[0] < 2120 and -200 < self.position[1] < 1280):
            self.finished = True
