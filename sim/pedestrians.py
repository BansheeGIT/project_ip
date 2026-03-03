# sim/pedestrians.py
class Pedestrian:
    def __init__(self, x, y, axis):
        self.position = [float(x), float(y)]
        self.axis = axis
        self.speed = 100.0
        self.active, self.finished = False, False
        self.variant, self.direction = "ped1", "N"
        self.velocity = [0.0, 0.0]
        self.WAIT_Y_TOP, self.WAIT_Y_BOTTOM = 405, 675 
        self.WAIT_X_LEFT, self.WAIT_X_RIGHT = 815, 1095 

    def update(self, dt):
        if self.finished: return
        if not self.active:
            if self.axis == "NS":
                if self.velocity[1] > 0 and 395 <= self.position[1] <= 405: return
                if self.velocity[1] < 0 and 675 <= self.position[1] <= 685: return
            elif self.axis == "EW":
                if self.velocity[0] > 0 and 805 <= self.position[0] <= 815: return
                if self.velocity[0] < 0 and 1095 <= self.position[0] <= 1105: return

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        if not (-200 < self.position[0] < 2120 and -200 < self.position[1] < 1280):
            self.finished = True