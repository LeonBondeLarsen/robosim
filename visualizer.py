import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from robot import draw_robot
from kinematics import AckermanSteerKinematics
from game_pad import JoystickSteeringReader
from sensor import LightSensor
from control import CircleController
import math

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

# Initialize joystick reader
joystick = JoystickSteeringReader(
    js_index=0,
    axis_throttle=1,  # left stick Y
    axis_steer=0,     # left stick X
    vmax=15.0,
    steer_max_deg=60.0,
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
sensors = []
sensors.append( LightSensor(geometry=(0.5, 1.75, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, 1.25, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, 0.75, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, 0.25, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, -0.25, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, -0.75, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, -1.25, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )
sensors.append( LightSensor(geometry=(0.5, -1.75, 0.5), map_path=bg_path, map_size=(map_width, map_height)) )

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
    # Get sensor readings
    sensor_values = []
    for sensor_id in range(len(sensors)):
        sensor_values.append( sensors[sensor_id].get_sensor_value(kinematics.get_state()) )
    print([f"{x:.2f}" for x in sensor_values])

    # Get control inputs
    if state == 'auto':
        velocity, steer_angle = controller.get_control(sensor_values)
    else:
        velocity, steer_angle = joystick.get_steering()

    # Update kinematics
    kinematics.update(velocity, steer_angle, dt)

    # Redraw the visualization
    clear_visualization()
    draw_robot(ax, kinematics.get_state(), steer_angle)
    for sensor_id in range(len(sensors)):
        sensors[sensor_id].draw_sensor(ax, kinematics.get_state())

# Set up and start the timer
timer = fig.canvas.new_timer(interval=dt * 1000)
timer.add_callback(on_timer)
timer.start()

# Show the plot
try:
    plt.show(block=True)
finally:
    timer.stop()
    plt.ioff()



