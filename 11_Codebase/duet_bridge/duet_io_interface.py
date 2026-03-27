"""
OBSIDIAN-8 V3
duet_io_interface.py
Revision: V3.2
Status: Authoritative

Purpose:
Python interface for interacting with the Duet controller.
Handles actuator commands, servo banks, IO feedback, and ensures
safe operation via watchdog and error handling.

Dependencies:
- Python 3.10+
- requests (for Duet HTTP API)
- logging
- threading
"""

import requests
import time
import threading
import logging

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("DuetIOInterface")

# -------------------------
# Duet Controller Settings
# -------------------------
DUET_IP = "192.168.1.50"  # Replace with actual controller IP
DUET_PORT = 80
BASE_URL = f"http://{DUET_IP}:{DUET_PORT}"

# Polling interval in seconds
STATUS_POLL_INTERVAL = 0.5

# Watchdog timeout in seconds
WATCHDOG_TIMEOUT = 2.0

# -------------------------
# Exception Definitions
# -------------------------
class DuetConnectionError(Exception):
    pass

class DuetCommandError(Exception):
    pass

# -------------------------
# Duet IO Interface Class
# -------------------------
class DuetIOInterface:
    def __init__(self):
        self.status = {}
        self._watchdog_timer = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._poll_thread = threading.Thread(target=self._poll_status_loop)
        self._poll_thread.daemon = True
        self._poll_thread.start()
        logger.info("Duet IO Interface initialized.")

    # ---------------------
    # Watchdog Methods
    # ---------------------
    def _reset_watchdog(self):
        with self._lock:
            if self._watchdog_timer:
                self._watchdog_timer.cancel()
            self._watchdog_timer = threading.Timer(WATCHDOG_TIMEOUT, self._watchdog_triggered)
            self._watchdog_timer.start()

    def _watchdog_triggered(self):
        logger.error("Watchdog timeout triggered! Halting all actuators.")
        self.halt_all_actuators()

    # ---------------------
    # Polling Status
    # ---------------------
    def _poll_status_loop(self):
        while not self._stop_event.is_set():
            try:
                self.update_status()
            except Exception as e:
                logger.warning(f"Failed to poll Duet status: {e}")
            time.sleep(STATUS_POLL_INTERVAL)

    def update_status(self):
        try:
            r = requests.get(f"{BASE_URL}/rr_status?type=3")
            if r.status_code != 200:
                raise DuetConnectionError(f"Status request failed: {r.status_code}")
            self.status = r.json()
            self._reset_watchdog()
        except requests.RequestException as e:
            raise DuetConnectionError(f"Connection error: {e}")

    # ---------------------
    # Actuator Commands
    # ---------------------
    def send_command(self, gcode: str):
        """Send a G-code command to Duet."""
        try:
            r = requests.post(f"{BASE_URL}/rr_gcode?gcode={gcode}")
            if r.status_code != 200:
                raise DuetCommandError(f"G-code failed: {gcode}, {r.status_code}")
            result = r.json()
            if result.get("status") != "ok":
                raise DuetCommandError(f"G-code execution error: {result}")
            logger.debug(f"Command sent successfully: {gcode}")
        except requests.RequestException as e:
            raise DuetConnectionError(f"Connection error during command: {e}")

    def halt_all_actuators(self):
        """Immediately stop all motion safely."""
        logger.info("Halting all actuators via emergency stop.")
        try:
            self.send_command("M410")  # Duet Emergency Stop (Immediate Halt)
        except DuetCommandError as e:
            logger.error(f"Emergency stop failed: {e}")

    # ---------------------
    # Servo Control Helpers
    # ---------------------
    def set_servo_position(self, servo_id: int, angle: float):
        """Move a servo to a specific angle."""
        gcode = f"M280 P{servo_id} S{angle}"
        self.send_command(gcode)

    # ---------------------
    # Shutdown Interface
    # ---------------------
    def shutdown(self):
        """Cleanly shutdown interface and polling loop."""
        logger.info("Shutting down Duet IO Interface.")
        self._stop_event.set()
        if self._watchdog_timer:
            self._watchdog_timer.cancel()
        self._poll_thread.join()

# -------------------------
# Example Usage (Test)
# -------------------------
if __name__ == "__main__":
    duet = DuetIOInterface()
    try:
        logger.info("Setting servo 0 to 90 degrees.")
        duet.set_servo_position(0, 90)
        time.sleep(2)
        logger.info("Halting actuators for safety test.")
        duet.halt_all_actuators()
    finally:
        duet.shutdown()
