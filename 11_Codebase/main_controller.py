"""
main_controller.py
OBSIDIAN-8 V3 — REV F
Mobile Command Node with Multi-Unit (Ground + Air) Control
"""

import threading
import time
import uuid

# Internal modules
from autonomous_mode import AutonomousMode
from teleop_interface import TeleopInterface
from swarm_comms import SwarmComms
from power_monitor import PowerMonitor
from thermal_monitor import ThermalMonitor
from emergency_stop import EmergencyStop
from dock_manager import DockManager
from charge_control import ChargeControl


# =========================
# UNIT TYPES
# =========================
UNIT_GROUND = "GROUND"
UNIT_DRONE = "DRONE"

ROLE_SCOUT = "SCOUT"
ROLE_HEAVY = "HEAVY"
ROLE_RELAY = "RELAY"
ROLE_RECON = "RECON"


class MainController:
    def __init__(self):
        print("[MainController] Initializing command node...")

        # Core systems
        self.autonomous = AutonomousMode(camera_sources=[0, 1])
        self.teleop = TeleopInterface(self.autonomous.motion_planner)
        self.swarm = SwarmComms(swarm_size=50, listen_port=9000)
        self.power = PowerMonitor()
        self.thermal = ThermalMonitor()
        self.estop = EmergencyStop()
        self.dock = DockManager()
        self.charger = ChargeControl()

        # System state
        self.running = False
        self.mode = "autonomous"
        self.lock = threading.Lock()

        # Unit registry (THE BIG ADD)
        self.units = {}  # unit_id -> metadata

        # Threads
        self.monitor_thread = None

    # =========================
    # UNIT MANAGEMENT
    # =========================
    def register_unit(self, unit_type, role):
        unit_id = str(uuid.uuid4())

        self.units[unit_id] = {
            "type": unit_type,
            "role": role,
            "status": "idle",
            "last_seen": time.time()
        }

        print(f"[UNIT] Registered {unit_type}:{role} -> {unit_id}")
        return unit_id

    def get_units_by_type(self, unit_type):
        return {uid: u for uid, u in self.units.items() if u["type"] == unit_type}

    def get_units_by_role(self, role):
        return {uid: u for uid, u in self.units.items() if u["role"] == role}

    # =========================
    # TASKING SYSTEM
    # =========================
    def assign_task(self, unit_id, task):
        if unit_id not in self.units:
            return

        self.units[unit_id]["status"] = "assigned"

        command = {
            "type": "COMMAND",
            "target": unit_id,
            "task": task
        }

        self.swarm.send_command(unit_id, command)

    def deploy_recon_drone(self):
        drones = self.get_units_by_type(UNIT_DRONE)

        for uid, drone in drones.items():
            if drone["role"] == ROLE_RECON and drone["status"] == "idle":
                print(f"[DRONE] Deploying recon drone {uid}")

                self.assign_task(uid, {
                    "action": "recon_scan",
                    "altitude": 10,
                    "radius": 20
                })
                return

    # =========================
    # START/STOP
    # =========================
    def start(self):
        print("[MainController] Starting...")
        self.running = True

        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()

        self.swarm.start()

        if self.mode == "autonomous":
            self.autonomous.start()
        else:
            self.teleop.start()

    def stop(self):
        print("[MainController] Stopping...")
        self.running = False

        self.autonomous.stop()
        self.teleop.stop()
        self.swarm.stop()
        self.power.shutdown()

        if self.monitor_thread:
            self.monitor_thread.join()

    # =========================
    # MAIN LOOP
    # =========================
    def monitor_loop(self):
        while self.running:
            try:
                # Emergency stop
                if self.estop.is_triggered():
                    print("[EMERGENCY] STOP")
                    self.autonomous.motion_planner.execute_trajectory([0] * 24)
                    time.sleep(0.1)
                    continue

                # Power safety
                status = self.power.get_status()
                if not self.power.is_power_safe():
                    print("[POWER] LOW — docking")
                    self.dock.autonomous_dock()
                    self.charger.start_charging()

                # Thermal safety
                temps = self.thermal.read_temperatures()
                if any(t > 70 for t in temps):
                    print("[THERMAL] OVERHEAT")
                    self.autonomous.motion_planner.execute_trajectory([0] * 24)

                # Example autonomous trigger
                self.evaluate_environment()

                time.sleep(0.1)

            except Exception as e:
                print(f"[ERROR] {e}")

    # =========================
    # DECISION LAYER
    # =========================
    def evaluate_environment(self):
        """
        Placeholder for real logic:
        - obstacle detection
        - uncertainty detection
        - mission triggers
        """

        # Example: randomly trigger drone recon
        if int(time.time()) % 20 == 0:
            self.deploy_recon_drone()

    # =========================
    # ENTRY
    # =========================
if __name__ == "__main__":
    controller = MainController()

    # Example units (simulate your ecosystem)
    controller.register_unit(UNIT_DRONE, ROLE_RECON)
    controller.register_unit(UNIT_GROUND, ROLE_SCOUT)

    controller.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
