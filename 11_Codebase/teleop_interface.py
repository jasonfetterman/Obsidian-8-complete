"""
teleop_interface.py
OBSIDIAN-8 V3 — REV D
Provides remote manual control via joystick or network commands
"""

import pygame
import threading
import time
from motion_planner import MotionPlanner

class TeleopInterface:
    def __init__(self, robot_id="OBS8-01"):
        # Initialize joystick
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"[Teleop] Using joystick: {self.joystick.get_name()}")
        else:
            print("[Teleop] No joystick detected, network control only")
        
        self.robot_id = robot_id
        self.motion_planner = MotionPlanner()
        self.running = False

    def read_joystick(self):
        """
        Read joystick axes and buttons, return command dict
        """
        pygame.event.pump()
        axes = {}
        buttons = {}
        if self.joystick:
            axes = {i: self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())}
            buttons = {i: self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())}
        return {"axes": axes, "buttons": buttons}

    def network_command(self, cmd):
        """
        Accept network-based commands (dict) and convert to motion
        Example cmd: {"forward": 0.5, "turn": -0.2}
        """
        # Convert to motion planner commands
        self.motion_planner.set_velocity(cmd.get("forward",0), cmd.get("turn",0))

    def teleop_loop(self):
        self.running = True
        try:
            while self.running:
                # Read joystick input
                cmd = self.read_joystick()
                if cmd["axes"]:
                    # Map axes to robot velocity
                    forward = -cmd["axes"].get(1, 0)  # Y axis inverted
                    turn = cmd["axes"].get(0, 0)      # X axis
                    self.motion_planner.set_velocity(forward, turn)

                # Add network command reading here if needed
                # Example: self.network_command(received_network_cmd)

                time.sleep(0.02)  # 50 Hz
        finally:
            pygame.quit()
            print("[Teleop] Stopped")

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    teleop = TeleopInterface(robot_id="OBS8-01")
    try:
        teleop.teleop_loop()
    except KeyboardInterrupt:
        print("[Teleop] Stopped by user")
