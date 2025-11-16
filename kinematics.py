import math
import numpy as np

class State(object):
    """
    Represents the state of the robot. Since it is in 2D space, it has x, y 
    coordinates and an orientation theta.
    """
    def __init__(self, x=0.0, y=0.0, theta=math.pi/2):
        self.x = x
        self.y = y
        self.theta = theta

class Kinematics(object):
    """
    Base class for all kinematic models. This defines the interface that all
    kinematic models must implement. The update method updates the state of the
    robot based on the input commands. The get_state method returns the current
    state of the robot.
    """
    def __init__(self):
        self.state = State()

    def update(self):
        raise NotImplementedError
    
    def get_state(self):
        raise NotImplementedError

class TankSteerKinematics(Kinematics):
    """
    Kinematics model for a tank-steering robot. The input is the linear velocity
    and angular velocity.
    """
    def __init__(self):
        super().__init__()

    def update(self, linear_velocity, angular_velocity, dt=0.1):
        self.state.x += linear_velocity * dt * math.cos(self.state.theta)
        self.state.y += linear_velocity * dt * math.sin(self.state.theta)
        self.state.theta += angular_velocity * dt


    def get_state(self):
        return (self.state.x, self.state.y, self.state.theta)
    

class AckermanSteerKinematics(Kinematics):
    """
    Kinematics model for an Ackerman-steering robot. The input is the linear
    velocity and steering angle.
    """
    def __init__(self, L=4.0):
        super().__init__()
        self.L = L

    def update(self, linear_velocity, steering_angle, dt=0.1):
        self.state.x += linear_velocity * dt * math.cos(self.state.theta)
        self.state.y += linear_velocity * dt * math.sin(self.state.theta)
        self.state.theta += (linear_velocity / self.L) * math.tan(np.deg2rad(steering_angle)) * dt


    def get_state(self):
        return (self.state.x, self.state.y, self.state.theta)