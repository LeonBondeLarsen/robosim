import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from robot import draw_robot
from kinematics import TankSteerKinematics, AckermanSteerKinematics
from game_pad import JoystickSteeringReader
from sensor import LightSensor
from control import CircleController
import math

import sensor

# Visualization settings
bg_path = "robot_track_simple_1024.png" # path to background image
dt = 0.01 # Time step
map_width = 25.0
map_height = 25.0
state = 'manual'  # 'manual' or 'auto'

# Initialize kinematics
kinematics = AckermanSteerKinematics()
kinematics.state.x = 0.5
kinematics.state.y = 0.1
kinematics.state.theta = math.pi / 6.0
velocity = 0.0
steer_angle = 0.0

joystick = JoystickSteeringReader(
    js_index=0,
    axis_throttle=1,  # left stick Y
    axis_steer=0,     # left stick X
    vmax=10.0,
    steer_max_deg=40.0,
    deadzone=0.10,
    rate_hz=120
)
def button_callback(button):
    global state
    if button == 0:  # Assuming button 0 toggles mode
        if state == 'auto':
            state = 'manual'
            print("Switched to MANUAL mode")
        else:
            state = 'auto'
            print("Switched to AUTO mode")
joystick.button_callback = button_callback
joystick.start()

# Initialize sensors
left_sensor = LightSensor(geometry=(0, 0.8, 0.5), map_path=bg_path, map_size=(map_width, map_height))
right_sensor = LightSensor(geometry=(0, -0.8, 0.5), map_path=bg_path, map_size=(map_width, map_height))

# Initialize controllers
controller = CircleController(velocity=10.0, steering_angle=30)

# Visualization setup
plt.ion() # Turn on interactive mode
bg = mpimg.imread(bg_path) # Load background image
fig, ax = plt.subplots(figsize=(map_width, map_height)) # Create figure and axis

def clear_visualization():
    ax.clear()
    ax.imshow(bg, extent=[0, map_width, 0, map_height])
    ax.set_xlim(- 5, map_width + 5)
    ax.set_ylim(- 5, map_height + 5)
    ax.axis("off")

clear_visualization()
fig.canvas.draw() # Draw the canvas
draw_robot(ax, kinematics.get_state(),steer_angle)

# Timer callback for updating the robot state and visualization
def on_timer(_=None):
    if state == 'auto':
        velocity, steer_angle = controller.get_control()
    else:
        velocity, steer_angle = joystick.get_steering()

    # Update kinematics
    kinematics.update(velocity, steer_angle, dt)

    # Get sensor reading
    left_sensor_value = left_sensor.get_sensor_value(kinematics.get_state())
    right_sensor_value = right_sensor.get_sensor_value(kinematics.get_state())
    #print(f"Sensors: left: {left_sensor_value:.2f}, right: {right_sensor_value:.2f}")

    # Redraw
    clear_visualization()
    draw_robot(ax, kinematics.get_state(), steer_angle)
    left_sensor.draw_sensor(ax, kinematics.get_state())
    right_sensor.draw_sensor(ax, kinematics.get_state())

# Set up and start the timer
timer = fig.canvas.new_timer(interval=dt * 1000)
timer.add_callback(on_timer)
timer.start()

try:
    plt.show(block=True)
finally:
    timer.stop()
    plt.ioff()



