"""
main_controller.py
OBSIDIAN-8 V3 — REV D
Main brain and orchestrator for autonomous operation, teleoperation, and swarm control
"""

import threading
import time

# Internal modules
from autonomous_mode import AutonomousMode
from teleop_interface import TeleopInterface
from swarm_comms import SwarmComms
from power_monitor import PowerMonitor
from thermal_monitor import ThermalMonitor
from emergency_stop import EmergencyStop
from dock_manager import DockManager
from charge_control import ChargeControl

class MainController:
    def __init__(self):
        # ---------------- Core Modules ----------------
        print("[MainController] Initializing core modules...")
        self.autonomous = AutonomousMode(camera_sources=[0,1])
        self.teleop = TeleopInterface(self.autonomous.motion_planner)
        self.swarm = SwarmComms(swarm_size=50, listen_port=9000)
        self.power = PowerMonitor()
        self.thermal = ThermalMonitor()
        self.estop = EmergencyStop()
        self.dock = DockManager()
        self.charger = ChargeControl()

        # Operational flags
        self.running = False
        self.mode = "autonomous"  # "autonomous" or "teleop"
        self.lock = threading.Lock()

        # Threads
        self.monitor_thread = None
        self.swarm_thread = None

    # ---------------- Startup / Shutdown ----------------
    def start(self):
        print("[MainController] Starting main controller...")
        self.running = True

        # Start monitoring loops
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.start()

        # Start swarm communication
        self.swarm.start()

        # Start autonomous / teleop
        if self.mode == "autonomous":
            self.autonomous.start()
        elif self.mode == "teleop":
            self.teleop.start()

    def stop(self):
        print("[MainController] Stopping main controller...")
        self.running = False

        self.autonomous.stop()
        self.teleop.stop()
        self.swarm.stop()

        if self.monitor_thread:
            self.monitor_thread.join()
        print("[MainController] Shutdown complete.")

    # ---------------- Main Monitoring Loop ----------------
    def monitor_loop(self):
        """
        Continuously checks:
        - Power levels
        - Thermal states
        - Emergency stop
        - Docking requests
        """
        while self.running:
            # Emergency stop override
            if self.estop.is_triggered():
                print("[MainController] EMERGENCY STOP TRIGGERED! Halting all motion.")
                self.autonomous.motion_planner.execute_trajectory([0]*24)
                time.sleep(0.1)
                continue

            # Power check
            voltage, current = self.power.read_voltage_current()
            if voltage < 20.0:  # example low-voltage threshold
                print(f"[MainController] LOW BATTERY: {voltage}V, initiating dock")
                self.dock.autonomous_dock()
                self.charger.start_charging()

            # Thermal check
            temps = self.thermal.read_temperatures()
            if any(t > 70 for t in temps):
                print(f"[MainController] OVERHEAT: {temps}, pausing motion")
                self.autonomous.motion_planner.execute_trajectory([0]*24)

            # Swarm management
            self.manage_swarm()

            time.sleep(0.1)  # 10 Hz loop

    # ---------------- Swarm Management ----------------
    def manage_swarm(self):
        """
        High-level swarm orchestration:
        - Collect states
        - Send coordinated commands
        - Handle up to 50 bots
        """
        all_states = self.swarm.get_all_states()

        for bot_id, bot_info in all_states.items():
            # Example: maintain distance or formation
            command = {"action": "hold_position"}
            self.swarm.send_command(bot_id, command)

    # ---------------- Mode Switching ----------------
    def set_mode(self, mode):
        """
        mode: "autonomous" or "teleop"
        """
        with self.lock:
            if mode == self.mode:
                return
            # Stop current mode
            if self.mode == "autonomous":
                self.autonomous.stop()
            elif self.mode == "teleop":
                self.teleop.stop()

            # Start new mode
            self.mode = mode
            if self.mode == "autonomous":
                self.autonomous.start()
            elif self.mode == "teleop":
                self.teleop.start()
            print(f"[MainController] Switched to {self.mode} mode")

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    controller = MainController()
    controller.start()
    print("[MainController] Running. Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        controller.stop()
        print("[MainController] Exited")
