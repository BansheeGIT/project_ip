<<<<<<< HEAD
# sim/pedestrians.py
class Pedestrian:
    def __init__(self, x, y, axis):
        self.position = [float(x), float(y)]
=======
# One moving pedestrian lives in this class.
class Pedestrian:
    # These lines work like curb edges where people wait on red.
    WAIT_Y_TOP = 405.0
    WAIT_Y_BOTTOM = 675.0
    WAIT_X_LEFT = 815.0
    WAIT_X_RIGHT = 1095.0

    # Set the start state for one pedestrian.
    def __init__(self, x, y, axis):
        self.position = [x, y]
>>>>>>> master
        self.axis = axis
        self.speed = 100.0
        self.active = False
        self.finished = False
        self.variant = "ped1"
        self.direction = "N"
        self.velocity = [0.0, 0.0]

<<<<<<< HEAD
        # Curb lines where pedestrians must wait on red.
        self.WAIT_Y_TOP = 405.0
        self.WAIT_Y_BOTTOM = 675.0
        self.WAIT_X_LEFT = 815.0
        self.WAIT_X_RIGHT = 1095.0

    def _hold_at_curb(self):
=======
    # Hold the pedestrian at the curb on red.
    def _hold_at_curb(self):
        # Stop right at the curb until this crossing can move.
>>>>>>> master
        if self.axis == "NS":
            if self.velocity[1] > 0 and self.position[1] >= self.WAIT_Y_TOP:
                self.position[1] = self.WAIT_Y_TOP
                return True
            if self.velocity[1] < 0 and self.position[1] <= self.WAIT_Y_BOTTOM:
                self.position[1] = self.WAIT_Y_BOTTOM
                return True
<<<<<<< HEAD
            return False

        if self.axis == "EW":
=======

        elif self.axis == "EW":
>>>>>>> master
            if self.velocity[0] > 0 and self.position[0] >= self.WAIT_X_LEFT:
                self.position[0] = self.WAIT_X_LEFT
                return True
            if self.velocity[0] < 0 and self.position[0] <= self.WAIT_X_RIGHT:
                self.position[0] = self.WAIT_X_RIGHT
                return True
<<<<<<< HEAD
            return False

        return False

=======

        return False

    # Move the pedestrian one step forward.
>>>>>>> master
    def update(self, dt):
        if self.finished:
            return

<<<<<<< HEAD
        # On red, walk to the curb and wait without stepping onto the road.
=======
        # If the signal says wait, do not step into the road yet.
>>>>>>> master
        if not self.active and self._hold_at_curb():
            return

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
<<<<<<< HEAD
=======
        
        # Once the person leaves the map, the world can forget it.
>>>>>>> master
        if not (-200 < self.position[0] < 2120 and -200 < self.position[1] < 1280):
            self.finished = True
