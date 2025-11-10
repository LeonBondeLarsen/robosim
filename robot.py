import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

def draw_robot(ax, state, circle_radius=0.06, arrow_len=0.1):
    """
    Draws a robot as a red circle with a black heading arrow using only patches.
    state = (x, y, theta), where theta is in radians.
    """
    x, y, theta = state

    # Draw circle body
    circle = Circle(
        (x, y), circle_radius,
        facecolor='none', 
        edgecolor='red',
        lw=2,
        zorder=5
    )
    ax.add_patch(circle)

    # Compute arrow base position (starts at the center of the circle)
    dx = arrow_len * np.cos(theta)
    dy = arrow_len * np.sin(theta)

    # Draw directional arrow
    arrow = FancyArrow(
        x, y, dx, dy,
        width=0.01,               # thickness of shaft
        length_includes_head=True,
        head_width=0.03,
        head_length=0.05,
        color='black',
        lw=2,
        zorder=5
    )
    ax.add_patch(arrow)


if __name__ == "__main__":
    import matplotlib.image as mpimg

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_facecolor("white")
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw a few robots
    draw_robot(ax, state=(0.2, 0.3, np.deg2rad(30)))
    draw_robot(ax, state=(0.6, 0.7, np.deg2rad(200)))

    plt.show()
