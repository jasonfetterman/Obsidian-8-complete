import time
import math


class MotionPlanner:
    def __init__(self):
        # Current state
        self.current_vx = 0.0
        self.current_vy = 0.0
        self.current_w = 0.0  # angular velocity

        self.last_time = time.time()

        # Constraints (TUNE THESE TO YOUR HARDWARE)
        self.max_vel = 1.5          # m/s
        self.max_accel = 1.0        # m/s^2
        self.max_angular = 2.0      # rad/s

        self.emergency = False

    # =========================
    # PLANNING
    # =========================
    def plan(self, path):
        """
        path = list of waypoints or dict
        returns motion command dict
        """
        if not path:
            return {"vx": 0, "vy": 0, "w": 0}

        target = path[0]

        dx = target["x"]
        dy = target["y"]

        distance = math.hypot(dx, dy)

        if distance < 0.05:
            return {"vx": 0, "vy": 0, "w": 0}

        vx = dx / distance * self.max_vel
        vy = dy / distance * self.max_vel

        return {"vx": vx, "vy": vy, "w": 0}

    # =========================
    # EXECUTION
    # =========================
    def execute(self, cmd):
        if self.emergency:
            self.halt_all()
            return

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        if dt <= 0:
            return

        target_vx = self._clamp(cmd.get("vx", 0), self.max_vel)
        target_vy = self._clamp(cmd.get("vy", 0), self.max_vel)
        target_w = self._clamp(cmd.get("w", 0), self.max_angular)

        # Apply acceleration limits
        self.current_vx = self._ramp(self.current_vx, target_vx, dt)
        self.current_vy = self._ramp(self.current_vy, target_vy, dt)
        self.current_w = self._ramp(self.current_w, target_w, dt)

        # Send to hardware layer (stub)
        self._send_to_motors(self.current_vx, self.current_vy, self.current_w)

    # =========================
    # SAFETY
    # =========================
    def halt_all(self):
        self.current_vx = 0
        self.current_vy = 0
        self.current_w = 0
        self._send_to_motors(0, 0, 0)

    def trigger_emergency(self):
        self.emergency = True
        self.halt_all()

    def clear_emergency(self):
        self.emergency = False

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _ramp(self, current, target, dt):
        delta = target - current
        max_delta = self.max_accel * dt

        if abs(delta) > max_delta:
            delta = math.copysign(max_delta, delta)

        return current + delta

    def _clamp(self, value, limit):
        return max(min(value, limit), -limit)

    def _send_to_motors(self, vx, vy, w):
        """
        Replace this with real motor interface
        """
        print(f"[MOTION] vx={vx:.2f} vy={vy:.2f} w={w:.2f}")
