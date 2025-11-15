import numpy as np
from PIL import Image
from matplotlib.patches import Circle

class LightSensor:
    def __init__(self, geometry, map_path, map_size):
        """
        geometry: (x_local, y_local, diameter)
            Sensor position and view diameter in robot coordinates (world units).
        map_path: path to the PNG map image.
        map_size: (map_width, map_height) in the same world units used for robot poses.
        """
        self.x_local, self.y_local, self.diameter = geometry
        self.radius = self.diameter / 2.0

        # Load map as grayscale [0,1]
        img = Image.open(map_path).convert("L")
        self.map = np.array(img, dtype=np.float32) / 255.0
        self.height, self.width = self.map.shape

        # World-to-pixel scale factors
        self.map_width, self.map_height = map_size
        self.scale_x = self.width / self.map_width
        self.scale_y = self.height / self.map_height

    def get_sensor_value(self, pose):
        """
        pose: (x, y, rot)
            Robot pose in world coordinates (same system as map_size).
        Returns:
            Average light intensity [0.0, 1.0] within the sensor’s view circle.
        """
        x_robot, y_robot, rot = pose

        # Transform local sensor position -> world
        c, s = np.cos(rot), np.sin(rot)
        x_sensor = x_robot + c * self.x_local - s * self.y_local
        y_sensor = y_robot + s * self.x_local + c * self.y_local

        # Convert world coordinates -> pixel coordinates
        # Assuming map (0,0) = bottom-left of world corresponds to image bottom-left
        # If your image origin is top-left (as in imshow), invert y
        cx = x_sensor * self.scale_x
        cy = (self.map_height - y_sensor) * self.scale_y  # flip y for image index

        # Sensor radius in pixels
        r_px = self.radius * self.scale_x  # assume isotropic pixels

        # Bounding box in pixel indices
        x_min = int(np.floor(cx - r_px))
        x_max = int(np.ceil(cx + r_px))
        y_min = int(np.floor(cy - r_px))
        y_max = int(np.ceil(cy + r_px))

        # Clip to image bounds
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(self.width - 1, x_max)
        y_max = min(self.height - 1, y_max)
        
        if x_min > x_max or y_min > y_max:
            return 0.0  # Sensor is out of bounds

        # Create coordinate grids
        ys, xs = np.mgrid[y_min:y_max+1, x_min:x_max+1]
        mask = (xs - cx)**2 + (ys - cy)**2 <= r_px**2

        region = self.map[ys, xs]
        if np.any(mask):
            return float(region[mask].mean())
        else:
            return 0.0
    def draw_sensor(self, ax, pose):
        """
        Draw a red circle on a Matplotlib Axes showing the sensor position.
        pose: (x, y, rot) in world coordinates.
        """
        x_robot, y_robot, rot = pose
        c, s = np.cos(rot), np.sin(rot)
        x_sensor = x_robot + c * self.x_local - s * self.y_local
        y_sensor = y_robot + s * self.x_local + c * self.y_local

        circle = Circle(
            (x_sensor, y_sensor),
            radius=self.radius,
            edgecolor='red',
            facecolor='none',
            lw=2,
            zorder=5
        )
        ax.add_patch(circle)