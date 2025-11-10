import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from robot import draw_robot
from kinematics import Kinematics

# Constant declarations
bg_path = "robot_track_simple_1024.png"
dt = 0.01

# Initialize kinematics
kinematics = Kinematics()
kinematics.state.x = 0.5
kinematics.state.y = 0.1
kinematics.state.theta = 0.0

# Visualization setup
plt.ion() # Turn on interactive mode
bg = mpimg.imread(bg_path) # Load background image
fig, ax = plt.subplots(figsize=(10, 10)) # Create figure and axis
ax.imshow(bg, extent=[0, 1, 0, 1]) # Display background image
ax.axis("off") # Turn off axis
fig.canvas.draw() # Draw the canvas
background = fig.canvas.copy_from_bbox(ax.bbox) # Save background for easy redraw
draw_robot(ax, kinematics.get_state())

# Timer callback for updating the robot state and visualization
def on_timer(_=None):

    # Update kinematics
    kinematics.update(0.5, 2, dt)

    # Redraw
    ax.clear()
    ax.imshow(bg, extent=[0, 1, 0, 1])
    ax.axis("off")
    draw_robot(ax, kinematics.get_state())

# Set up and start the timer
timer = fig.canvas.new_timer(interval=dt * 1000)
timer.add_callback(on_timer)
timer.start()

try:
    plt.show(block=True)
finally:
    timer.stop()
    plt.ioff()



