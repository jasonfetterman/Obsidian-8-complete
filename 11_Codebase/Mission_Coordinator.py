# mission_coordinator.py — REV D (Smooth + Heading + Thermal-Aware Control)

import time
import threading
import math

class MissionCoordinator:
    def __init__(self, swarm, set_pose_callback):
        self.swarm = swarm
        self.set_pose = set_pose_callback

        self.active = False
        self.follow_thread = None

        # Pose state
        self.current_pose = [90.0] * 16
        self.target_pose = [90.0] * 16

        # Movement tuning
        self.base_pose = [90.0] * 16
        self.step_strength = 6.0   # forward intensity
        self.turn_strength = 4.0   # turning intensity

        # Smoothing
        self.smoothing = 0.2

        # Thermal scaling (updated externally later if needed)
        self.thermal_scale = 1.0

        # Tracking
        self.prev_lat = None
        self.prev_lon = None

    # ---------------- MISSION ----------------

    def scout_and_follow(self, lat, lon, alt=3.0):
        print("[MISSION] Smooth Directional Follow")

        self.active = True

        self.swarm.takeoff_all(alt)
        time.sleep(8)
        self.swarm.goto_all(lat, lon, alt)

        self.follow_thread = threading.Thread(target=self._follow_loop, daemon=True)
        self.follow_thread.start()

    # ---------------- FOLLOW LOOP ----------------

    def _follow_loop(self):
        print("[MISSION] Follow loop active")

        while self.active:
            positions = self.swarm.get_positions()

            if not positions:
                time.sleep(0.1)
                continue

            drone_id = list(positions.keys())[0]
            lat, lon, alt = positions[drone_id]

            if self.prev_lat is None:
                self.prev_lat = lat
                self.prev_lon = lon
                time.sleep(0.1)
                continue

            # Movement vector
            dlat = lat - self.prev_lat
            dlon = lon - self.prev_lon

            self.prev_lat = lat
            self.prev_lon = lon

            dx = dlat * 111000
            dy = dlon * 111000

            mag = math.sqrt(dx*dx + dy*dy)

            # Ignore noise
            if mag < 0.03:
                self.target_pose = self.base_pose.copy()
            else:
                # Normalize
                nx = dx / (mag + 1e-6)
                ny = dy / (mag + 1e-6)

                # Compute movement influence
                forward = nx * self.step_strength * self.thermal_scale
                turn = ny * self.turn_strength * self.thermal_scale

                # Build target pose dynamically
                self.target_pose = []

                for i in range(16):
                    base = 90.0

                    # Even joints = forward bias
                    if i % 2 == 0:
                        angle = base + forward
                    else:
                        angle = base - forward

                    # Add turning bias
                    if i < 8:
                        angle += turn
                    else:
                        angle -= turn

                    self.target_pose.append(angle)

            # Smooth transition
            self.current_pose = self._blend(self.current_pose, self.target_pose)

            self.set_pose(self.current_pose)

            time.sleep(0.05)

    # ---------------- SMOOTHING ----------------

    def _blend(self, current, target):
        blended = []
        for c, t in zip(current, target):
            val = c + self.smoothing * (t - c)
            blended.append(val)
        return blended

    # ---------------- THERMAL INPUT ----------------

    def set_thermal_state(self, state):
        """
        Hook for controller:
        NORMAL = full speed
        WARNING = reduced movement
        """
        if state == "NORMAL":
            self.thermal_scale = 1.0
        elif state == "WARNING":
            self.thermal_scale = 0.5
        else:
            self.thermal_scale = 0.0  # shutdown

    # ---------------- STOP ----------------

    def stop(self):
        print("[MISSION] Stopping mission")

        self.active = False

        try:
            self.swarm.land_all()
        except:
            pass

        self.set_pose(self.base_pose)
