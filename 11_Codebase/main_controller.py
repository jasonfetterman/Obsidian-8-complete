import time
import threading

from motion_planner import MotionPlanner
from sensor_fusion import SensorFusion
from path_planner import PathPlanner
from swarm_comms import SwarmComms
from power_monitor import PowerMonitor
from mesh_heartbeat import MeshHeartbeat

from pi_watchdog.heartbeat_monitor import HeartbeatMonitor

# ===== SYSTEM MODES =====
MODE_IDLE = "IDLE"
MODE_TELEOP = "TELEOP"
MODE_AUTONOMOUS = "AUTONOMOUS"
MODE_EMERGENCY = "EMERGENCY_STOP"


class ObsidianController:
    def __init__(self):
        print("[INIT] Starting OBSIDIAN-8 Controller")

        # Core systems
        self.sensor_fusion = SensorFusion()
        self.motion_planner = MotionPlanner()
        self.path_planner = PathPlanner()

        # Comms
        self.swarm = SwarmComms()
        self.mesh = MeshHeartbeat()

        # Health
        self.power = PowerMonitor()
        self.watchdog = HeartbeatMonitor()

        # State
        self.mode = MODE_IDLE
        self.running = True

        # Thread control
        self.lock = threading.Lock()

    # =========================
    # MODE CONTROL
    # =========================
    def set_mode(self, new_mode):
        with self.lock:
            print(f"[MODE] Switching to {new_mode}")
            self.mode = new_mode

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):
        print("[SYSTEM] Entering main loop")

        while self.running:
            try:
                self.watchdog.kick()

                # Health check first
                if not self.power.is_power_safe():
                    print("[FAILSAFE] Power unsafe!")
                    self.set_mode(MODE_EMERGENCY)

                if self.watchdog.is_system_unhealthy():
                    print("[FAILSAFE] Watchdog triggered!")
                    self.set_mode(MODE_EMERGENCY)

                # Mode execution
                if self.mode == MODE_IDLE:
                    self.idle_loop()

                elif self.mode == MODE_TELEOP:
                    self.teleop_loop()

                elif self.mode == MODE_AUTONOMOUS:
                    self.autonomous_loop()

                elif self.mode == MODE_EMERGENCY:
                    self.emergency_stop()

                time.sleep(0.02)

            except Exception as e:
                print(f"[CRITICAL ERROR] {e}")
                self.set_mode(MODE_EMERGENCY)

    # =========================
    # MODE LOOPS
    # =========================
    def idle_loop(self):
        # Minimal activity
        self.sensor_fusion.update()

    def teleop_loop(self):
        self.sensor_fusion.update()
        commands = self.swarm.get_teleop_commands()
        self.motion_planner.execute(commands)

    def autonomous_loop(self):
        self.sensor_fusion.update()

        world_state = self.sensor_fusion.get_state()
        path = self.path_planner.compute_path(world_state)
        motion_cmds = self.motion_planner.plan(path)

        self.motion_planner.execute(motion_cmds)

    def emergency_stop(self):
        print("[EMERGENCY] STOPPING ALL SYSTEMS")
        self.motion_planner.halt_all()
        time.sleep(0.1)

    # =========================
    # SHUTDOWN
    # =========================
    def shutdown(self):
        print("[SYSTEM] Shutdown initiated")
        self.running = False
        self.motion_planner.halt_all()


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    controller = ObsidianController()

    try:
        controller.run()
    except KeyboardInterrupt:
        controller.shutdown()
