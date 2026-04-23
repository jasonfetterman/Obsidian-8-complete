# main_controller.py — REV D (Fully Integrated + Logging + Thermal Latch Safe)

import time
import threading
import serial

from motion_planner import run_motion_loop, set_pose
from motion_scheduler import run_scheduler, reset_gait

from system_logger import log_thermal, log_motion, log_system, log_fault

# ---------------- CONFIG ----------------

SERIAL_PORT = "COM3"   # UPDATE THIS
BAUD_RATE = 115200

HEARTBEAT_INTERVAL = 0.02

BASE_POSE = [90.0] * 16

# ---------------- STATE ----------------

running = True
thermal_state = "NORMAL"  # NORMAL / WARNING / LATCHED

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)

# ---------------- SERIAL ----------------

def send_servo_command(servo_id, angle, speed):
    cmd = f"{servo_id},{angle:.2f},{speed}\n"
    ser.write(cmd.encode())

# ---------------- THERMAL ----------------

def handle_thermal_message(msg):
    global thermal_state

    if "THERMAL_WARNING" in msg:
        if thermal_state != "WARNING":
            print("[THERMAL] WARNING — throttling")
        thermal_state = "WARNING"
        log_thermal("WARNING")

    elif "THERMAL_SHUTDOWN_LATCHED" in msg:
        print("[THERMAL] CRITICAL — LATCHED SHUTDOWN")
        thermal_state = "LATCHED"
        log_thermal("SHUTDOWN_LATCHED")
        emergency_stop(latched=True)

    elif "THERMAL_MANUAL_RESET" in msg:
        print("[THERMAL] MANUAL RESET")
        thermal_state = "NORMAL"
        log_thermal("MANUAL_RESET")

# ---------------- SERIAL LISTENER ----------------

def serial_listener():
    global running
    while running:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                handle_thermal_message(line)
        except:
            pass

# ---------------- HEARTBEAT ----------------

def heartbeat_loop():
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

    speed = 80
    if thermal_state == "WARNING":
        speed = 40

    send_servo_command(servo_id, angle, speed)
    log_motion(servo_id, angle, speed)

# ---------------- BASE POSE ----------------

def get_base_pose():
    return BASE_POSE.copy()

# ---------------- SAFETY ----------------

def emergency_stop(latched=False):
    global running

    log_fault("Emergency stop triggered")

    print("[SYSTEM] Emergency stop")

    set_pose(BASE_POSE)
    reset_gait()

    if latched:
        log_fault("System latched — restart required")
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
    global running

    print("=== OBSIDIAN-8 CONTROL START ===")
    log_system("Controller started")

    start_threads()

    try:
        while running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[USER] Shutdown requested")
        emergency_stop()

    finally:
        ser.close()
        log_system("Controller stopped")
        print("=== SYSTEM STOPPED ===")

# ---------------- ENTRY ----------------

if __name__ == "__main__":
    main()
