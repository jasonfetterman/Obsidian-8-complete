"""
path_planner.py
OBSIDIAN-8 V3 — REV D
Generates safe trajectories and footstep plans based on sensor input
"""

import numpy as np
from motion_planner import MotionPlanner

class PathPlanner:
    def __init__(self, num_legs=8):
        self.motion_planner = MotionPlanner(num_legs=num_legs)
        self.safe_distance = 100.0  # mm, minimum clearance from obstacles

    def plan_step(self, current_pos, obstacles):
        """
        Plan next step for robot body given obstacles
        current_pos: np.array([x, y, z])
        obstacles: list of dict {"pos": [x,y,z], "radius": r}
        Returns: velocity command dict {"forward": , "turn": }
        """
        forward_cmd = 0.0
        turn_cmd = 0.0

        # Simple avoidance logic
        for obs in obstacles:
            obs_pos = np.array(obs["pos"])
            distance = np.linalg.norm(obs_pos - current_pos)
            if distance < self.safe_distance:
                # Obstacle too close, adjust velocity
                forward_cmd = -0.5  # back up
                if obs_pos[1] > current_pos[1]:
                    turn_cmd = -0.3  # turn left
                else:
                    turn_cmd = 0.3   # turn right
                break
        else:
            forward_cmd = 0.5  # normal forward
            turn_cmd = 0.0

        return {"forward": forward_cmd, "turn": turn_cmd}

    def execute_plan(self, current_pos, obstacles):
        """
        High-level execution loop
        """
        cmd = self.plan_step(current_pos, obstacles)
        self.motion_planner.set_velocity(cmd["forward"], cmd["turn"])
        return cmd

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    planner = PathPlanner()
    current_pos = np.array([0.0, 0.0, 0.0])

    # Example obstacles
    obstacles = [{"pos": [150, 0, 0], "radius": 50}]

    try:
        while True:
            cmd = planner.execute_plan(current_pos, obstacles)
            print(f"[PathPlanner] Velocity command: {cmd}")
            # Simulate movement
            current_pos[0] += cmd["forward"] * 10  # mm per loop
    except KeyboardInterrupt:
        print("[PathPlanner] Stopped")
