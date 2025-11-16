
class Controller():
    """
    Base class for all controllers. This defines the interface that all
    controllers must implement.
    """
    def __init__(self):
        pass

    def get_control(self):
        pass


class CircleController(Controller):
    """
    Controller for circular motion. This is just an example to show the principle
    of implementing a controller. It moves the robot in a circle by setting a
    constant speed and steering angle. A more advanced controller would use sensor
    values to adjust the speed and steering angle dynamically.
    """
    def __init__(self, velocity, steering_angle):
        super().__init__()
        self.speed = velocity
        self.turn_rate = steering_angle

    def get_control(self, sensor_values):
        return self.speed, self.turn_rate

