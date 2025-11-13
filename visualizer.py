import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from robot import draw_robot
from kinematics import Kinematics
import math

# Constant declarations
bg_path = "robot_track_simple_1024.png"
dt = 0.01
map_width = 25.0
map_height = 25.0

# Initialize kinematics
kinematics = Kinematics()
kinematics.state.x = 0.5
kinematics.state.y = 0.1
kinematics.state.theta = 0

# Visualization setup
plt.ion() # Turn on interactive mode
bg = mpimg.imread(bg_path) # Load background image
fig, ax = plt.subplots(figsize=(map_width, map_height)) # Create figure and axis
ax.set_xlim(map_width - 5, map_width + 5)
ax.set_ylim(map_height - 5, map_height + 5)
ax.imshow(bg, extent=[0, map_width, 0, map_height]) # Display background image
ax.axis("off") # Turn off axis
fig.canvas.draw() # Draw the canvas
background = fig.canvas.copy_from_bbox(ax.bbox) # Save background for easy redraw
draw_robot(ax, kinematics.get_state(),25)

# Timer callback for updating the robot state and visualization
def on_timer(_=None):

    # Update kinematics
    kinematics.update(10, 0, dt)

    # Redraw
    ax.clear()
    ax.imshow(bg, extent=[0, map_width, 0, map_height])
    ax.set_xlim(- 5, map_width + 5)
    ax.set_ylim(- 5, map_height + 5)
    #ax.axis("off")
    draw_robot(ax, kinematics.get_state(),25)

# Set up and start the timer
timer = fig.canvas.new_timer(interval=dt * 1000)
timer.add_callback(on_timer)
timer.start()

try:
    plt.show(block=True)
finally:
    timer.stop()
    plt.ioff()



