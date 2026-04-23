# main_controller.py — REV B (Full System Integration Controller)

import time
import threading
import serial

from motion_planner import run_motion_loop, set_pose
from motion_scheduler import run_scheduler, reset_gait

# ---------------- CONFIG ----------------

SERIAL_PORT = "COM3"   # UPDATE if needed
BAUD_RATE = 115200

HEARTBEAT_INTERVAL = 0.02  # 50 Hz
THERMAL_POLL_INTERVAL = 0.1

# Default neutral pose (16 servos)
BASE_POSE = [90.0] * 16

# ---------------- STATE ----------------

running = True
thermal_state = "NORMAL"   # NORMAL / WARNING / SHUTDOWN

# ---------------- SERIAL ----------------

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)

def send_servo_command(servo_id, angle):
    # Format: ID,ANGLE,SPEED
    cmd = f"{servo_id},{angle:.2f},80\n"
    ser.write(cmd.encode())

def send_pose(pose):
    for i, angle in enumerate(pose):
        send_servo_command(i, angle)

# ---------------- THERMAL HANDLING ----------------

def handle_thermal_message(msg):
    global thermal_state, running

    if "THERMAL_WARNING" in msg:
        if thermal_state != "WARNING":
            print("[THERMAL] WARNING — reducing motion")
        thermal_state = "WARNING"

    elif "THERMAL_SHUTDOWN" in msg:
        print("[THERMAL] CRITICAL — shutting down")
        thermal_state = "SHUTDOWN"
        emergency_stop()

    elif "THERMAL_RECOVERY" in msg:
        print("[THERMAL] RECOVERED")
        thermal_state = "NORMAL"

# ---------------- SERIAL LISTENER ----------------

def serial_listener():
    global running

    while running:
        try:
            line = ser.readline().decode().strip()
            if line:
                handle_thermal_message(line)
        except:
            pass

# ---------------- HEARTBEAT ----------------

def heartbeat_loop():
    while running:
        ser.write(b"HB\n")
        time.sleep(HEARTBEAT_INTERVAL)

# ---------------- MOTION CALLBACK ----------------

def motion_send_callback(servo_id, angle):
    # Reduce speed if thermal warning
    speed = 80
    if thermal_state == "WARNING":
        speed = 40

    cmd = f"{servo_id},{angle:.2f},{speed}\n"
    ser.write(cmd.encode())

# ---------------- BASE POSE ----------------

def get_base_pose():
    return BASE_POSE.copy()

# ---------------- SAFETY ----------------

def emergency_stop():
    global running
    print("[SYSTEM] Emergency stop triggered")

    # Stop motion planner immediately
    set_pose(BASE_POSE)

    # Stop scheduler loop
    reset_gait()

    running = False

# ---------------- THREADS ----------------

def start_threads():
    threading.Thread(target=serial_listener, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    threading.Thread(
        target=run_motion_loop,
        args=(motion_send_callback,),
        daemon=True
    ).start()
    threading.Thread(
        target=run_scheduler,
        args=(get_base_pose, set_pose),
        daemon=True
    ).start()

# ---------------- MAIN ----------------

def main():
    print("=== OBSIDIAN-8 CONTROL START ===")

    start_threads()

    try:
        while running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[USER] Shutdown requested")
        emergency_stop()

    finally:
        ser.close()
        print("=== SYSTEM STOPPED ===")

# ---------------- ENTRY ----------------

if __name__ == "__main__":
    main()
