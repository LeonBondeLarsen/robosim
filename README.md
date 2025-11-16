# Simple robot simulator
To run the simulation, just run the visualizer.py script

## How it works
The simulation runs default every 0.01 second. It goes through:
1. Get sensor data from the sensor module
1. Get velocity and steering angle from the controller or the joystick depending on mode
1. Update the kinematics. This will update the pose of the robot
1. Clear the canvas and draw it all again in the new pose

## Sensor
The sensor module implements a light sensor. The constructor places the sensor in the robots coordinate system and sets the diameter of the sensor. Getting the sensor data will look at a patch of the background image and return the average pixel value in the patch.

## Controller
The controller implements a very simple auto mode causing the robot to run in a circle. The intention is to implement a controller that makes the robot follow a line in the background image

## Game pad
The simulation is controlled from a gamepad. When in manual mode, the joystick controls the robot. When in auto mode the controller takes over. Pressing 'A' on the game pad toggles between manual and auto mode.

## Kinematics
The kinematics module implements a very basic Ackerman steering. Given the velocity and steering angle, it will calculate the new pose of the robot. In the simple version, the robot can be controlled directly, meaning that it does not need to accelerate and the steering angle can change instantaneous. For a more realistic simulation, a more advanced model could be implemented.

## Robot
The visualization of the robot is defined in the robot module. It draws four wheels, the axels, and a line connecting the midpoints of the axels. It then converts the drawings from the robot's coordinate system to global coordinates.

## Visualizer
The visualizer module connects everything. The core process happens in the on_timer function being called every 0.01 seconds. Another thread runs the gamepad loop to always keep the latest state of the joystick. It also registers a callback triggered when a button is pressed for controlling the auto mode.