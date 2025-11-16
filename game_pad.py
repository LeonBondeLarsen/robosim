import threading
import time
import math
import pygame

class JoystickSteeringReader:
    """
    Reads joystick input and maps it to linear velocity and steering angle.
    Runs in a separate thread, polling at a specified rate."""
    def __init__(self,
                 js_index=0,
                 axis_throttle=1,     # left stick Y on most gamepads
                 axis_steer=0,        # left stick X on most gamepads
                 vmax=5.0,            # m/s (or arbitrary units)
                 steer_max_deg=40.0,  # degrees
                 deadzone=0.10,       # ignore small stick noise
                 rate_hz=120):        # polling rate
        self.js_index = js_index
        self.axis_throttle = axis_throttle
        self.axis_steer = axis_steer
        self.vmax = float(vmax)
        self.steer_max_deg = float(steer_max_deg)
        self.deadzone = float(deadzone)
        self.period = 1.0 / float(rate_hz)
        self.button_callback = None 

        self._thread = None
        self._running = False
        self._lock = threading.Lock()
        self._lin_vel = 0.0
        self._steer_deg = 0.0

        # pygame objects
        self._js = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        # Init pygame/joystick here (inside start) so class is self-contained
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() <= self.js_index:
            raise RuntimeError(f"No joystick at index {self.js_index} (found {pygame.joystick.get_count()})")

        self._js = pygame.joystick.Joystick(self.js_index)
        self._js.init()

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        # Don’t quit pygame globally in case others use it; just leave devices inited.

    def join(self):
        if self._thread is not None:
            self._thread.join()

    def get_steering(self):
        """Return (linear_velocity, steering_angle_deg). Thread-safe."""
        with self._lock:
            return self._lin_vel, self._steer_deg

    # ----------------- internals -----------------

    def _loop(self):
        # High-resolution timer loop
        next_t = time.perf_counter()
        while self._running:
            # Pump events so pygame updates its internal state
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONUP:
                    if self.button_callback is not None:
                        self.button_callback(event.button)

            # Read axes
            try:
                raw_throttle = self._safe_axis(self.axis_throttle)  # range [-1, 1]
                raw_steer    = self._safe_axis(self.axis_steer)     # range [-1, 1]
            except Exception:
                # If joystick disappears, zero outputs
                raw_throttle = 0.0
                raw_steer = 0.0

            # Apply deadzone & scale
            t = self._apply_deadzone(raw_throttle, self.deadzone)
            s = self._apply_deadzone(raw_steer, self.deadzone)

            # Many controllers report forward as negative Y, so invert throttle:
            t = -t

            # Map to requested ranges
            lin_vel   = self._clamp(t * self.vmax, -self.vmax, self.vmax)
            steer_deg = self._clamp(-s * self.steer_max_deg, -self.steer_max_deg, self.steer_max_deg)

            with self._lock:
                self._lin_vel = lin_vel
                self._steer_deg = steer_deg

            # Sleep to maintain rate
            next_t += self.period
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                # If we fell behind, reset the schedule
                next_t = time.perf_counter()

    def _safe_axis(self, idx):
        if self._js is None:
            return 0.0
        n = self._js.get_numaxes()
        if idx < 0 or idx >= n:
            return 0.0
        return float(self._js.get_axis(idx))

    @staticmethod
    def _apply_deadzone(val, dz):
        """Scaled deadzone: keep direction, remove small noise, rescale to full range."""
        v = float(val)
        a = abs(v)
        if a <= dz:
            return 0.0
        # Remap [dz,1] -> [0,1] smoothly
        return math.copysign((a - dz) / (1.0 - dz), v)

    @staticmethod
    def _clamp(x, lo, hi):
        return max(lo, min(hi, x))


# ----------------- Example usage -----------------
if __name__ == "__main__":
    reader = JoystickSteeringReader(
        js_index=0,
        axis_throttle=1,  # left stick Y
        axis_steer=0,     # left stick X
        vmax=5.0,
        steer_max_deg=40.0,
        deadzone=0.10,
        rate_hz=120
    )
    reader.start()

    try:
        while True:
            v, a = reader.get_steering()
            print(f"lin_vel={v:+.2f}, steer={a:+.1f}°")
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
