"""
OBSIDIAN-8 V3
servo_bridge.py
Revision: V3.2
Status: Authoritative

Purpose:
Python interface to control servo banks on OBSIDIAN-8 V3.
Handles command queuing, safety enforcement, position interpolation,
and integration with the Duet IO Interface.

Dependencies:
- Python 3.10+
- threading
- time
- logging
- duet_io_interface (from duet_bridge)
"""

import threading
import time
import logging
from duet_io_interface import DuetIOInterface

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ServoBridge")

# -------------------------
# Servo Bridge Class
# -------------------------
class ServoBridge:
    def __init__(self, servo_ids):
        """
        Initialize ServoBridge with a list of servo IDs.
        """
        self.duet = DuetIOInterface()
        self.servo_ids = servo_ids
        self._lock = threading.Lock()
        self._command_queue = []
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._process_queue)
        self._worker_thread.daemon = True
        self._worker_thread.start()
        logger.info(f"ServoBridge initialized for servos: {servo_ids}")

    # ---------------------
    # Queue Commands
    # ---------------------
    def move_servo(self, servo_id, target_angle, duration=0.5):
        """
        Queue a servo movement command.
        :param servo_id: int
        :param target_angle: float, degrees
        :param duration: float, seconds for interpolation
        """
        if servo_id not in self.servo_ids:
            logger.warning(f"Servo ID {servo_id} not recognized.")
            return

        with self._lock:
            self._command_queue.append({
                "servo_id": servo_id,
                "target_angle": target_angle,
                "duration": duration
            })
        logger.debug(f"Queued move command: servo {servo_id} → {target_angle}° over {duration}s")

    # ---------------------
    # Command Processing
    # ---------------------
    def _process_queue(self):
        while not self._stop_event.is_set():
            if self._command_queue:
                with self._lock:
                    cmd = self._command_queue.pop(0)
                self._execute_command(cmd)
            else:
                time.sleep(0.01)  # avoid busy wait

    def _execute_command(self, cmd):
        servo_id = cmd["servo_id"]
        target = cmd["target_angle"]
        duration = cmd["duration"]

        try:
            # Retrieve current position (placeholder: assume instant move)
            current_angle = 0.0  # TODO: integrate real feedback if available

            # Interpolate if duration > 0
            steps = max(int(duration / 0.05), 1)
            for step in range(1, steps + 1):
                intermediate_angle = current_angle + (target - current_angle) * (step / steps)
                self.duet.set_servo_position(servo_id, intermediate_angle)
                time.sleep(duration / steps)
            logger.info(f"Servo {servo_id} moved to {target}°")
        except Exception as e:
            logger.error(f"Failed to move servo {servo_id}: {e}")
            # Halt actuators if critical error
            self.duet.halt_all_actuators()

    # ---------------------
    # Shutdown
    # ---------------------
    def shutdown(self):
        logger.info("Shutting down ServoBridge.")
        self._stop_event.set()
        self._worker_thread.join()
        self.duet.shutdown()


# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    servos = [0, 1, 2, 3]  # Example servo IDs
    bridge = ServoBridge(servos)

    try:
        bridge.move_servo(0, 90, duration=1.0)
        bridge.move_servo(1, 45, duration=0.5)
        time.sleep(2)
    finally:
        bridge.shutdown()
