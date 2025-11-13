import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

def draw_simple_robot(ax, state, circle_radius=0.06, arrow_len=0.1):
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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

def draw_robot(ax, pose, steer,
               wheelbase=4.0, track=3.0,
               wheel_len=0.8, wheel_thick=0.3):
    """
    Draw a simple 4-wheeled vehicle.

    pose: (x, y, rot)  -> midpoint between the FRONT wheels, rot in radians
    steer: steering angle (degrees) for BOTH front wheels
           0° means wheel axis is perpendicular to the axle (i.e., straight)
    """

    x, y, rot = pose
    rot += np.pi / 2.0  # convert to vehicle-forward-along-y-axis frame

    # ---- local geometry (origin at front-axle midpoint) ----
    left_x  = -track / 2.0
    right_x =  track / 2.0
    y_front = 0.0
    y_rear  = wheelbase

    # rotation matrix for chassis orientation
    c, s = np.cos(rot), np.sin(rot)
    R = np.array([[c, -s],
                  [s,  c]])

    # ---- draw axle (track) lines + red dots at ends ----
    for y_axle in (y_front, y_rear):
        L_local  = np.array([left_x,  y_axle])
        R_local  = np.array([right_x, y_axle])
        L_global = R @ L_local + np.array([x, y])
        R_global = R @ R_local + np.array([x, y])

        ax.plot([L_global[0], R_global[0]],
                [L_global[1], R_global[1]], 'k-', lw=2)
        ax.plot(L_global[0], L_global[1], 'ro', ms=6)
        ax.plot(R_global[0], R_global[1], 'ro', ms=6)

    # ---- wheels: centers ARE the axle endpoints ----
    # 0° steer = perpendicular to axle => base 90°
    front_wheel_angle = 90.0 + steer
    rear_wheel_angle  = 90.0

    wheels_local = [
        (left_x,  y_front, front_wheel_angle),
        (right_x, y_front, front_wheel_angle),
        (left_x,  y_rear,  rear_wheel_angle),
        (right_x, y_rear,  rear_wheel_angle),
    ]

    def draw_wheel(cx, cy, angle_deg):
        # wheel rectangle centered at (0,0) in its own local frame
        rect = Rectangle((-wheel_len/2, -wheel_thick/2),
                         wheel_len, wheel_thick,
                         ec='k', fc='0.6', zorder=3)

        # Compose transforms:
        #   (1) steer the wheel about its center (deg)
        #   (2) place at axle endpoint in chassis-local coords
        #   (3) rotate whole chassis by rot (rad)
        #   (4) translate to global (x, y)
        t = (Affine2D()
             .rotate_deg(angle_deg)
             .translate(cx, cy)
             .rotate(rot)
             .translate(x, y)
             + ax.transData)
        rect.set_transform(t)
        ax.add_patch(rect)

    for cx, cy, ang in wheels_local:
        draw_wheel(cx, cy, ang)

    # ---- optional center line (front->rear axle midpoints) ----
    P0 = R @ np.array([0.0, y_front]) + np.array([x, y])
    P1 = R @ np.array([0.0, y_rear ]) + np.array([x, y])
    ax.plot([P0[0], P1[0]], [P0[1], P1[1]], 'k--', lw=1)

if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(25,25))

    ax.set_facecolor("white")
    ax.set_aspect('equal')
    #ax.axis('off')

    draw_robot(ax, (0,0,np.pi), steer=30)

    plt.show()
