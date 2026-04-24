# system_logger.py — REV B (Adds Temperature Logging)

import os
from datetime import datetime

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"obsidian8_log_{timestamp}.csv")

with open(LOG_FILE, "w") as f:
    f.write("time,event_type,details\n")

def log_event(event_type, details):
    now = datetime.now().strftime("%H:%M:%S.%f")
    with open(LOG_FILE, "a") as f:
        f.write(f"{now},{event_type},{details}\n")

def log_thermal(state):
    log_event("THERMAL", state)

def log_temp(servo, battery, buck):
    log_event("TEMP", f"servo={servo:.2f} battery={battery:.2f} buck={buck:.2f}")

def log_motion(servo_id, angle, speed):
    log_event("MOTION", f"id={servo_id} angle={angle:.2f} speed={speed}")

def log_system(msg):
    log_event("SYSTEM", msg)

def log_fault(msg):
    log_event("FAULT", msg)
