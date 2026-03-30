# motion_planner.py
# OBSIDIAN-8 V3 — REV D
# Converts planned paths or teleop inputs into joint commands

import math
from pid_controller import PIDController
from kinematics import InverseKinematics

# -------------------- CONFIG --------------------
JOINT_LIMITS = {
    'coxa': (-90, 90),     # degrees
    'femur': (-45, 90),
    'tibia': (-90, 0),
}

PID_PARAMS = {
    'coxa': (1.0, 0.01, 0.05),
    'femur': (1.2, 0.01, 0.05),
    'tibia': (1.0, 0.01, 0.05),
}

CONTROL_RATE_HZ = 200  # Low-level servo update rate

# -------------------- INITIALIZE --------------------
pid_controllers = {
    joint: PIDController(*PID_PARAMS[joint]) for joint in JOINT_LIMITS
}

ik_solver = InverseKinematics()

# -------------------- FUNCTIONS --------------------
def apply_joint_limits(joint_name, angle_deg):
    min_angle, max_angle = JOINT_LIMITS[joint_name]
    return max(min(angle_deg, max_angle), min_angle)

# -------------------- CLASS --------------------
class MotionPlanner:
    def __init__(self):
        self.current_joint_targets = {
            'coxa': 0.0,
            'femur': 0.0,
            'tibia': 0.0
        }

    def generate(self, planned_path, sensor_state):
        """
        Convert path coordinates to joint angles using IK,
        then apply PID to generate smooth joint commands.
        """
        joint_cmds = []
        for foot_position in planned_path:  # planned_path: list of (x, y, z)
            angles = ik_solver.solve(foot_position)
            # Apply joint limits and PID
            angles_limited = {}
            for joint in angles:
                limited = apply_joint_limits(joint, angles[joint])
                pid_output = pid_controllers[joint].compute(limited, self.current_joint_targets[joint])
                angles_limited[joint] = pid_output
                self.current_joint_targets[joint] = pid_output
            joint_cmds.append(angles_limited)
        return joint_cmds

    def apply_teleop(self, teleop_cmds):
        """
        Convert teleop joystick or controller commands into joint targets.
        teleop_cmds: dict with 'coxa', 'femur', 'tibia' deltas
        """
        joint_cmds = {}
        for joint, delta in teleop_cmds.items():
            new_target = self.current_joint_targets[joint] + delta
            new_target = apply_joint_limits(joint, new_target)
            pid_output = pid_controllers[joint].compute(new_target, self.current_joint_targets[joint])
            joint_cmds[joint] = pid_output
            self.current_joint_targets[joint] = pid_output
        return joint_cmds

    def halt_motion(self):
        """
        Stops all motion immediately by sending current joint angles as target
        """
        print("[MotionPlanner] Halting motion, maintaining current joint positions")
        return self.current_joint_targets.copy()
