
class Controller():
    def __init__(self):
        pass

    def get_control(self):
        pass


class CircleController(Controller):
    def __init__(self, velocity, steering_angle):
        super().__init__()
        self.speed = velocity
        self.turn_rate = steering_angle

    def get_control(self):
        return self.speed, self.turn_rate

