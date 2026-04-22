# motion_planner.py — REV B (High-Torque Safe Motion Planning)

import time
import math

# ---------------- CONFIG ----------------

SERVO_COUNT = 8

# Limits
ANGLE_MIN = 0
ANGLE_MAX = 180

# Motion constraints
MAX_SPEED_DEG_PER_SEC = 90      # global cap
MAX_ACCEL_DEG_PER_SEC2 = 180    # acceleration limit

# Update rate
UPDATE_HZ = 50
DT = 1.0 / UPDATE_HZ

# ---------------- STATE ----------------

class ServoState:
    def __init__(self):
        self.current = 90.0
        self.target = 90.0
        self.velocity = 0.0

servos = [ServoState() for _ in range(SERVO_COUNT)]

# ---------------- CORE FUNCTIONS ----------------

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def set_target(servo_id, angle):
    if 0 <= servo_id < SERVO_COUNT:
        servos[servo_id].target = clamp(angle, ANGLE_MIN, ANGLE_MAX)

def update_servo(servo: ServoState):
    error = servo.target - servo.current

    # Desired velocity based on error
    desired_velocity = clamp(error * 2.0, -MAX_SPEED_DEG_PER_SEC, MAX_SPEED_DEG_PER_SEC)

    # Acceleration limiting
    accel = desired_velocity - servo.velocity
    accel = clamp(accel, -MAX_ACCEL_DEG_PER_SEC2 * DT, MAX_ACCEL_DEG_PER_SEC2 * DT)

    servo.velocity += accel

    # Apply velocity
    servo.current += servo.velocity * DT

    # Snap to target if close
    if abs(error) < 0.5:
        servo.current = servo.target
        servo.velocity = 0.0

# ---------------- GROUP MOTION ----------------

def set_pose(pose):
    """
    pose: list of angles for all servos
    """
    for i in range(min(len(pose), SERVO_COUNT)):
        set_target(i, pose[i])

# ---------------- MAIN LOOP ----------------

def run_motion_loop(send_callback):
    """
    send_callback(servo_id, angle)
    """
    while True:
        start = time.time()

        for i, servo in enumerate(servos):
            update_servo(servo)
            send_callback(i, servo.current)

        elapsed = time.time() - start
        sleep_time = max(0, DT - elapsed)
        time.sleep(sleep_time)

# ---------------- SAFETY ----------------

def emergency_stop():
    for servo in servos:
        servo.target = servo.current
        servo.velocity = 0.0

# ---------------- EXAMPLE CALLBACK ----------------

def debug_send(servo_id, angle):
    print(f"Servo {servo_id}: {angle:.2f}")

# ---------------- ENTRY (OPTIONAL TEST) ----------------

if __name__ == "__main__":
    # Example: move all servos to 120 degrees
    set_pose([120] * SERVO_COUNT)
    run_motion_loop(debug_send)
