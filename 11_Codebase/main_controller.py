# main_controller.py — REV F (Ground + Drone Unified Control)

import time
import threading
import serial

from motion_planner import run_motion_loop, set_pose
from motion_scheduler import run_scheduler, reset_gait

from system_logger import log_system, log_fault, log_motion, log_thermal, log_temp
from swarm_comms import SwarmController

SERIAL_PORT = "COM3"
BAUD_RATE = 115200

HEARTBEAT_INTERVAL = 0.02
BASE_POSE = [90.0] * 16

running = True
thermal_state = "NORMAL"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)

# ---------------- SWARM ----------------

swarm = SwarmController()

# Example drone (SITL or real)
# Change IP if using real drone over WiFi
swarm.add_drone("drone1", "udp:127.0.0.1:14550")

# ---------------- SERIAL ----------------

def send_servo_command(servo_id, angle, speed):
    ser.write(f"{servo_id},{angle:.2f},{speed}\n".encode())

# ---------------- SERIAL HANDLER ----------------

def handle_serial_message(msg):
    global thermal_state

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

# ---------------- THREADS ----------------

def serial_listener():
    while running:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                handle_serial_message(line)
        except:
            pass

def heartbeat_loop():
    while running:
        ser.write(b"HB\n")
        time.sleep(HEARTBEAT_INTERVAL)

def motion_send_callback(servo_id, angle):
    if thermal_state == "LATCHED":
        return

    speed = 80 if thermal_state == "NORMAL" else 40
    send_servo_command(servo_id, angle, speed)
    log_motion(servo_id, angle, speed)

# ---------------- SAFETY ----------------

def emergency_stop(latched=False):
    global running

    log_fault("Emergency stop triggered")

    set_pose(BASE_POSE)
    reset_gait()

    # Land all drones immediately
    try:
        swarm.land_all()
    except:
        pass

    if latched:
        running = False
        log_fault("Latched shutdown — restart required")

# ---------------- START ----------------

def start_threads():
    threading.Thread(target=serial_listener, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    threading.Thread(target=run_motion_loop, args=(motion_send_callback,), daemon=True).start()
    threading.Thread(target=run_scheduler, args=(lambda: BASE_POSE.copy(), set_pose), daemon=True).start()

# ---------------- MAIN ----------------

def main():
    global running

    print("=== OBSIDIAN-8 + DRONE CONTROL START ===")
    log_system("System start with drone integration")

    start_threads()

    # Example mission (TEST ONLY)
    time.sleep(3)
    print("[MISSION] Drone takeoff")
    swarm.takeoff_all(2.0)

    time.sleep(10)
    print("[MISSION] Drone landing")
    swarm.land_all()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        emergency_stop()
    finally:
        ser.close()
        log_system("System stopped")
        print("=== STOPPED ===")

if __name__ == "__main__":
    main()
