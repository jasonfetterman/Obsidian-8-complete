# motion_planner.py
# OBSIDIAN-8 V3 — REV D
# Converts perception, foot sensors, and memory maps into leg gait commands

import numpy as np
from path_planner import PathPlanner

class MotionPlanner:
    def __init__(self, map_manager=None):
        # Initialize path planner
        self.map_manager = map_manager
        self.path_planner = PathPlanner(map_manager=map_manager)

        # Gait parameters
        self.step_height = 0.05  # meters
        self.step_length = 0.1   # meters
        self.swing_time = 0.3    # seconds per leg
        self.num_legs = 8
        self.current_leg_phase = np.zeros(self.num_legs)

    def compute_gait(self, tracked_objects, foot_state):
        """
        tracked_objects: dict {object_id: (x, y)}
        foot_state: list of bools indicating foot contact (True = on ground)
        Returns: dict of leg target positions / velocities
        """
        # Compute adjusted leg positions using path planner (includes map memory)
        leg_positions = self.path_planner.plan(tracked_objects)

        # Generate gait commands per leg
        leg_commands = {}
        for leg in range(self.num_legs):
            # Determine swing or stance
            if foot_state[leg]:
                # stance phase: keep foot on ground
                leg_commands[leg] = {
                    "phase": "stance",
                    "x": leg_positions[leg][0],
                    "y": leg_positions[leg][1],
                    "z": 0.0
                }
            else:
                # swing phase: lift foot
                leg_commands[leg] = {
                    "phase": "swing",
                    "x": leg_positions[leg][0],
                    "y": leg_positions[leg][1],
                    "z": self.step_height
                }

            # Increment leg phase for timing
            self.current_leg_phase[leg] += 0.02  # assumes 50 Hz update

        return leg_commands
