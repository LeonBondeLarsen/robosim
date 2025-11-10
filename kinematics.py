import math

class State(object):
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta

class Kinematics(object):
    def __init__(self):
        self.state = State()

    def update(self, linear_velocity, angular_velocity, dt=0.1):
        self.state.x += linear_velocity * dt * math.cos(self.state.theta)
        self.state.y += linear_velocity * dt * math.sin(self.state.theta)
        self.state.theta += angular_velocity * dt


    def get_state(self):
        return (self.state.x, self.state.y, self.state.theta)