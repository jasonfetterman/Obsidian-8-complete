"""
motion_planner.py
OBSIDIAN-8 V3 — REV D
Converts high-level velocity and trajectory commands into leg-level motions
"""

import numpy as np
from kinematics import LegKinematics
from servo_driver import ServoDriver

class MotionPlanner:
    def __init__(self, num_legs=8):
        self.num_legs = num_legs
        self.leg_kin = [LegKinematics(leg_id=i) for i in range(num_legs)]
        self.servo_driver = ServoDriver()
        self.current_velocity = {"forward": 0.0, "turn": 0.0}

    def set_velocity(self, forward, turn):
        """
        Sets desired robot velocity
        forward: float [-1,1] forward/backward
        turn: float [-1,1] left/right
        """
        self.current_velocity["forward"] = np.clip(forward, -1.0, 1.0)
        self.current_velocity["turn"] = np.clip(turn, -1.0, 1.0)
        self.plan_motion()

    def plan_motion(self):
        """
        Convert current velocity into leg target positions
        """
        # Example gait calculation: simplified tripod gait for octopod
        for i, leg in enumerate(self.leg_kin):
            # Compute leg swing/stance based on forward and turn velocity
            # Forward motion scales X-axis, turn scales Y-axis
            swing_offset = self.current_velocity["forward"] * 50.0  # mm
            turn_offset = self.current_velocity["turn"] * (-1 if i%2==0 else 1) * 30.0  # mm
            target_xyz = leg.default_position + np.array([swing_offset, turn_offset, 0.0])
            
            # Inverse kinematics to joint angles
            joint_angles = leg.inverse_kinematics(target_xyz)
            
            # Send angles to servo driver
            self.servo_driver.set_leg_angles(leg.leg_id, joint_angles)

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    planner = MotionPlanner()
    try:
        while True:
            # Example: move forward at 50% speed, slight left turn
            planner.set_velocity(0.5, -0.2)
    except KeyboardInterrupt:
        print("[MotionPlanner] Stopped")
