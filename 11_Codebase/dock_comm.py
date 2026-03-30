# dock_comm.py
# OBSIDIAN-8 V3 — REV D
# Handles communication with docking station and charger

import serial
import time

# -------------------- SERIAL CONFIG --------------------
# Serial connection to Teensy/Duet for dock-related commands
SERIAL_PORT = '/dev/ttyACM0'  # Adjust as needed
BAUD_RATE = 115200
TIMEOUT = 1  # seconds

# -------------------- DOCK COMMANDS --------------------
CMD_SERVO_ENABLE = "SERVO_ENABLE"
CMD_CHARGE_ENABLE = "CHARGE_ENABLE"
CMD_STATUS = "DOCK_STATUS"

# -------------------- DOCK COMMUNICATION CLASS --------------------
class DockComm:
    def __init__(self, port=SERIAL_PORT, baud=BAUD_RATE):
        self.ser = serial.Serial(port, baud, timeout=TIMEOUT)
        time.sleep(2)  # Wait for serial port to initialize
        print("DockComm initialized.")

    def send_servo_enable(self, enable: bool):
        """Send servo enable/disable command to Teensy/Duet"""
        cmd = f"{CMD_SERVO_ENABLE}:{int(enable)}\n"
        self.ser.write(cmd.encode('utf-8'))
        print(f"[DockComm] Sent: {cmd.strip()}")

    def send_charge_enable(self, enable: bool):
        """Send charger enable/disable command"""
        cmd = f"{CMD_CHARGE_ENABLE}:{int(enable)}\n"
        self.ser.write(cmd.encode('utf-8'))
        print(f"[DockComm] Sent: {cmd.strip()}")

    def request_status(self) -> dict:
        """Request docking status from Teensy/Duet"""
        self.ser.write(f"{CMD_STATUS}?\n".encode('utf-8'))
        line = self.ser.readline().decode('utf-8').strip()
        status = {
            "docked": False,
            "charging": False,
            "fault": False
        }
        try:
            # Expecting response: DOCK_STATUS:docked=1,charging=0,fault=0
            if line.startswith("DOCK_STATUS:"):
                parts = line[len("DOCK_STATUS:"):].split(',')
                for p in parts:
                    key, val = p.split('=')
                    status[key] = bool(int(val))
        except Exception as e:
            print(f"[DockComm] Failed to parse status: {line}, Error: {e}")
        return status

    def close(self):
        self.ser.close()
        print("[DockComm] Serial closed.")


# -------------------- TESTING --------------------
if __name__ == "__main__":
    dock = DockComm()
    dock.send_servo_enable(False)
    time.sleep(1)
    dock.send_charge_enable(True)
    status = dock.request_status()
    print(f"Dock Status: {status}")
    dock.close()
