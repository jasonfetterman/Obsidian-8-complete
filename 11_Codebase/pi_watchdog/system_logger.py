"""
OBSIDIAN-8 V3
system_logger.py
Revision: V3.2
Status: Authoritative

Purpose:
Centralized logging service for Pi Watchdog and OBSIDIAN-8 V3 subsystems.
Records heartbeat events, kill-line triggers, actuator commands, and
sensor errors. Ensures structured log retention for diagnostics and audits.

Dependencies:
- Python 3.10+
- logging
- threading
- time
- os
"""

import logging
import threading
import time
import os

# -------------------------
# Logger Configuration
# -------------------------
LOG_DIR = "/var/log/obsidian8"  # Adjust path as needed
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pi_watchdog.log")

logger = logging.getLogger("SystemLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# -------------------------
# System Logger Class
# -------------------------
class SystemLogger:
    def __init__(self):
        self._lock = threading.Lock()
        logger.info("SystemLogger initialized.")

    # ---------------------
    # Info Logging
    # ---------------------
    def info(self, message):
        with self._lock:
            logger.info(message)

    # ---------------------
    # Warning Logging
    # ---------------------
    def warning(self, message):
        with self._lock:
            logger.warning(message)

    # ---------------------
    # Error Logging
    # ---------------------
    def error(self, message):
        with self._lock:
            logger.error(message)

    # ---------------------
    # Critical Logging
    # ---------------------
    def critical(self, message):
        with self._lock:
            logger.critical(message)

    # ---------------------
    # Structured Event Logging
    # ---------------------
    def log_heartbeat(self, source, status="OK"):
        self.info(f"[HEARTBEAT] Source: {source}, Status: {status}")

    def log_kill_line_event(self, action):
        self.warning(f"[KILL_LINE] Action: {action}")

    def log_actuator_command(self, servo_id, angle):
        self.info(f"[ACTUATOR] Servo {servo_id} → {angle}°")

    def log_sensor_error(self, sensor, error):
        self.error(f"[SENSOR] {sensor}: {error}")

# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    sys_logger = SystemLogger()
    try:
        sys_logger.log_heartbeat("pi_watchdog_node")
        sys_logger.log_actuator_command(0, 90)
        sys_logger.log_kill_line_event("ENGAGED")
        sys_logger.log_sensor_error("IMU", "No response")
    except KeyboardInterrupt:
        pass
