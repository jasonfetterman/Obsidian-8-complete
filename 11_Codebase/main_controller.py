# main_controller.py
# OBSIDIAN-8 V3 — REV D
# Central controller with persistent map integration

import threading
import time
from autonomous_mode import AutonomousMode
from teleop_interface import TeleopInterface
from motion_planner import MotionPlanner
from swarm_comms import SwarmComms
from map_manager import MapManager

class MainController:
    def __init__(self, node_id="OB8-Node1"):
        # Initialize MapManager
        self.map_manager = MapManager(map_dir="maps/world", grid_size=4000, resolution=0.05)

        # Mode: "autonomous" or "teleop"
        self.mode = "autonomous"

        # Subsystems
        self.autonomous = AutonomousMode(node_id=node_id, map_manager=self.map_manager)
        self.teleop = TeleopInterface()
        self.motion_planner = MotionPlanner()
        self.swarm = self.autonomous.swarm  # shared swarm instance

        self.running = True

    def mode_switch_loop(self):
        """Monitor input to switch modes"""
        while self.running:
            new_mode = self.teleop.get_mode()
            if new_mode != self.mode:
                print(f"[MainController] Switching mode: {self.mode} -> {new_mode}")
                self.mode = new_mode
            time.sleep(0.1)

    def control_loop(self):
        """Main 50Hz control loop"""
        while self.running:
            if self.mode == "autonomous":
                # Get perception and mapped objects
                tracked_objects = self.autonomous.process_vision()
                foot_state = self.autonomous.foot_state

                # Compute leg commands with memory-aware path planning
                commands = self.motion_planner.compute_gait(tracked_objects, foot_state)

                # TODO: Send commands to servo_driver.cpp

            elif self.mode == "teleop":
                commands = self.teleop.get_commands()
                # TODO: Send commands to servo_driver.cpp

            # Handle swarm messages
            messages = self.swarm.get_messages()
            for msg in messages:
                print("[Swarm] Received:", msg)

            time.sleep(0.02)  # 50 Hz

    def run(self):
        """Start main controller"""
        mode_thread = threading.Thread(target=self.mode_switch_loop)
        mode_thread.start()

        try:
            self.control_loop()
        finally:
            self.shutdown()
            mode_thread.join()

    def shutdown(self):
        self.running = False
        self.autonomous.shutdown()
        self.teleop.shutdown()
        self.map_manager.shutdown()
        print("[MainController] Shutdown complete.")


# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    controller = MainController(node_id="OB8-Node1")
    controller.run()
