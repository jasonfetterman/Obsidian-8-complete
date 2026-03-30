# main_controller.py
# OBSIDIAN-8 V3 — REV D
# High-level orchestrator for motion, sensors, and autonomous/teleop control

import time
from motion_planner import MotionPlanner
from path_planner import PathPlanner
from sensor_fusion import SensorFusion
from swarm_comms import SwarmComms
from autonomous_mode import AutonomousMode
from teleop_interface import TeleopInterface
from dock_comm import DockComm
from charge_control import DockComm as ChargeDock

# -------------------- CONFIG --------------------
CONTROL_LOOP_HZ = 50  # 50 Hz main loop

# -------------------- INITIALIZE SYSTEMS --------------------
print("[Main] Initializing OBSIDIAN-8 V3 systems...")

sensor_fusion = SensorFusion()
motion_planner = MotionPlanner()
path_planner = PathPlanner()
swarm = SwarmComms()
autonomous = AutonomousMode()
teleop = TeleopInterface()
dock = DockComm()
charge = ChargeDock()

# Mode: 'AUTONOMOUS' or 'TELEOP'
mode = 'AUTONOMOUS'

print("[Main] Initialization complete. Entering control loop.")

# -------------------- MAIN LOOP --------------------
try:
    loop_delay = 1.0 / CONTROL_LOOP_HZ
    while True:
        start_time = time.time()

        # Update sensors
        sensor_fusion.update()

        # Determine current mode
        if mode == 'AUTONOMOUS':
            # Plan path and motion
            planned_path = path_planner.plan(sensor_fusion.state)
            motion_cmds = motion_planner.generate(planned_path, sensor_fusion.state)
            autonomous.execute(motion_cmds)
        elif mode == 'TELEOP':
            teleop_cmds = teleop.get_input()
            motion_planner.apply_teleop(teleop_cmds)

        # Swarm communication
        swarm.update_status(sensor_fusion.state)

        # Dock/charge monitoring
        if dock.is_docked():
            charge.send_charge_enable(True)
            motion_planner.halt_motion()
        else:
            charge.send_charge_enable(False)

        # Maintain loop rate
        elapsed = time.time() - start_time
        sleep_time = max(0, loop_delay - elapsed)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("[Main] Shutting down OBSIDIAN-8 V3 systems...")
    motion_planner.halt_motion()
    charge.send_charge_enable(False)
    dock.ser.close()
