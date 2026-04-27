# main_controller.py — REV I (Modular Structure: Obsidian + Air + Mission + Thermal)

import time
import threading
import serial

# -------- CORE (Obsidian-8) --------

from core_obsidian_8.motion.motion_planner import run_motion_loop, set_pose
from core_obsidian_8.motion.motion_scheduler import run_scheduler, reset_gait
from core_obsidian_8.sensors.imu_interface import IMUInterface

# -------- SHARED --------

from shared_infrastructure.logging.system_logger import (
log_system,
log_fault,
log_motion,
log_thermal,
log_temp
)

from shared_infrastructure.communication.swarm_comms import SwarmController

# -------- AIR SYSTEMS --------

# (kept inside mission layer via swarm for now)

# -------- MISSION CONTROL --------

from mission_control.mission_coordinator import MissionCoordinator

# ---------------- CONFIG ----------------

SERIAL_PORT = "COM3"
BAUD_RATE = 115200

HEARTBEAT_INTERVAL = 0.02
BASE_POSE = [90.0] * 16

# SITL test coordinate

MISSION_LAT = -35.363261
MISSION_LON = 149.165230

# ---------------- STATE ----------------

running = True
thermal_state = "NORMAL"

imu = IMUInterface()

# ---------------- SERIAL ----------------

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)

# ---------------- SWARM ----------------

swarm = SwarmController()
swarm.add_drone("drone1", "udp:127.0.0.1:14550")

# ---------------- MISSION ----------------

mission = MissionCoordinator(
swarm_controller=swarm,
motion_callback=set_pose,
imu=imu
)

# ---------------- LOW LEVEL CONTROL ----------------

def send_servo_command(servo_id, angle, speed):
ser.write(f"{servo_id},{angle:.2f},{speed}\n".encode())

# ---------------- SERIAL HANDLER ----------------

def handle_serial_message(msg):
global thermal_state

```
if msg.startswith("TEMP:"):
    try:
        s, b, c = map(float, msg.replace("TEMP:", "").split(","))
        log_temp(s, b, c)
    except:
        pass

elif "THERMAL_WARNING" in msg:
    thermal_state = "WARNING"
    log_thermal("WARNING")

elif "THERMAL_SHUTDOWN_LATCHED" in msg:
    thermal_state = "LATCHED"
    log_thermal("SHUTDOWN_LATCHED")
    emergency_stop(latched=True)

elif "THERMAL_MANUAL_RESET" in msg:
    thermal_state = "NORMAL"
    log_thermal("MANUAL_RESET")

# --- SYNC THERMAL STATE INTO MISSION LAYER ---
try:
    mission.set_thermal_state(thermal_state)
except:
    pass
```

# ---------------- THREADS ----------------

def serial_listener():
global running
while running:
try:
line = ser.readline().decode(errors="ignore").strip()
if line:
handle_serial_message(line)
except:
pass

def heartbeat_loop():
global running
while running:
try:
ser.write(b"HB\n")
except:
pass
time.sleep(HEARTBEAT_INTERVAL)

# ---------------- MOTION CALLBACK ----------------

def motion_send_callback(servo_id, angle):
if thermal_state == "LATCHED":
return

```
speed = 80 if thermal_state == "NORMAL" else 40

send_servo_command(servo_id, angle, speed)
log_motion(servo_id, angle, speed)
```

# ---------------- SAFETY ----------------

def emergency_stop(latched=False):
global running

```
log_fault("Emergency stop triggered")

# Stop motion safely
set_pose(BASE_POSE)
reset_gait()

# Stop mission + land drones
try:
    mission.stop()
except:
    pass

if latched:
    running = False
    log_fault("Latched shutdown — restart required")
```

# ---------------- THREAD START ----------------

def start_threads():
threading.Thread(target=serial_listener, daemon=True).start()
threading.Thread(target=heartbeat_loop, daemon=True).start()

```
threading.Thread(
    target=run_motion_loop,
    args=(motion_send_callback,),
    daemon=True
).start()

threading.Thread(
    target=run_scheduler,
    args=(lambda: BASE_POSE.copy(), set_pose),
    daemon=True
).start()
```

# ---------------- MAIN ----------------

def main():
global running

```
print("=== OBSIDIAN-8 SYSTEM START ===")
log_system("System start (modular architecture)")

start_threads()

# --- START MISSION ---
time.sleep(3)

print("[MAIN] Starting coordinated mission")
mission.scout_and_follow(MISSION_LAT, MISSION_LON)

try:
    while running:
        time.sleep(1)

except KeyboardInterrupt:
    emergency_stop()

finally:
    try:
        ser.close()
    except:
        pass

    log_system("System stopped")
    print("=== STOPPED ===")
```

# ---------------- ENTRY ----------------

if **name** == "**main**":
main()
