# mission_coordinator.py — REV C (Directional Drone → Ground Control)

import time
import threading
import math

class MissionCoordinator:
    def __init__(self, swarm, set_pose_callback):
        self.swarm = swarm
        self.set_pose = set_pose_callback

        self.active = False
        self.follow_thread = None

        # Pose presets (tuned for simple directional control)
        self.base_pose = [90.0] * 16

        self.forward_pose = [95.0] * 16
        self.left_turn_pose = [92.0,88.0]*8
        self.right_turn_pose = [88.0,92.0]*8

        # Target tracking
        self.target_lat = None
        self.target_lon = None

        # Last known drone position
        self.prev_lat = None
        self.prev_lon = None

    # ---------------- MISSION ----------------

    def scout_and_follow(self, lat, lon, alt=3.0):
        print("[MISSION] Scout + Directional Follow")

        self.active = True
        self.target_lat = lat
        self.target_lon = lon

        self.swarm.takeoff_all(alt)
        time.sleep(8)
        self.swarm.goto_all(lat, lon, alt)

        self.follow_thread = threading.Thread(target=self._follow_loop, daemon=True)
        self.follow_thread.start()

    # ---------------- FOLLOW LOOP ----------------

    def _follow_loop(self):
        print("[MISSION] Directional follow active")

        while self.active:
            positions = self.swarm.get_positions()

            if not positions:
                time.sleep(0.2)
                continue

            drone_id = list(positions.keys())[0]
            lat, lon, alt = positions[drone_id]

            # Initialize previous position
            if self.prev_lat is None:
                self.prev_lat = lat
                self.prev_lon = lon
                time.sleep(0.2)
                continue

            # Direction vector (drone movement)
            dlat = lat - self.prev_lat
            dlon = lon - self.prev_lon

            self.prev_lat = lat
            self.prev_lon = lon

            # Convert to meters
            dx = dlat * 111000
            dy = dlon * 111000

            distance = math.sqrt(dx*dx + dy*dy)

            print(f"[MISSION] Movement vector: dx={dx:.2f}, dy={dy:.2f}, dist={distance:.2f}")

            # Ignore tiny noise
            if distance < 0.05:
                self.set_pose(self.base_pose)
                time.sleep(0.2)
                continue

            # Determine direction
            if abs(dx) > abs(dy):
                # Forward/back bias
                self.set_pose(self.forward_pose)
            else:
                # Turning
                if dy > 0:
                    self.set_pose(self.left_turn_pose)
                else:
                    self.set_pose(self.right_turn_pose)

            time.sleep(0.2)

    # ---------------- STOP ----------------

    def stop(self):
        print("[MISSION] Stopping mission")

        self.active = False

        try:
            self.swarm.land_all()
        except:
            pass

        self.set_pose(self.base_pose)
