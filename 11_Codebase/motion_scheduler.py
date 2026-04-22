# motion_scheduler.py — REV C (Octopod Wave Gait, 16 Servos)

import time

# ---------------- CONFIG ----------------

UPDATE_HZ = 50
DT = 1.0 / UPDATE_HZ

SERVO_COUNT = 16  # 8 legs × 2 DOF (hip, knee)

# Leg indexing (fixed mapping)
# Each leg: [hip, knee]
# Leg order:
# 0: Front Left 1
# 1: Front Left 2
# 2: Mid Left 1
# 3: Rear Left 1
# 4: Rear Left 2
# 5: Rear Left 3
# 6: Mid Right 1
# 7: Front Right 1

LEG_MAP = [
    (0, 1),    # L1
    (2, 3),    # L2
    (4, 5),    # L3
    (6, 7),    # L4
    (8, 9),    # R1
    (10, 11),  # R2
    (12, 13),  # R3
    (14, 15)   # R4
]

LEG_COUNT = 8

# Wave gait: one leg moves at a time (maximum stability)
STEP_DURATION = 0.25  # seconds per leg step
CYCLE_LENGTH = LEG_COUNT

# Motion offsets (real values tuned for 150KG servos)
HIP_FORWARD = 18.0     # degrees
HIP_BACK = -12.0
KNEE_LIFT = -22.0      # lift leg
KNEE_SUPPORT = 10.0    # slight compression for load

# ---------------- STATE ----------------

current_leg_index = 0
phase_time = 0.0

# ---------------- CORE ----------------

def apply_leg_offset(pose, leg_index, hip_offset, knee_offset):
    hip_id, knee_id = LEG_MAP[leg_index]
    pose[hip_id] += hip_offset
    pose[knee_id] += knee_offset

def generate_wave_gait(base_pose):
    """
    Wave gait:
    - One leg lifts and moves forward
    - All others support and push slightly backward
    """
    pose = base_pose.copy()

    for i in range(LEG_COUNT):
        if i == current_leg_index:
            # Swing leg
            apply_leg_offset(
                pose,
                i,
                HIP_FORWARD,
                KNEE_LIFT
            )
        else:
            # Support legs
            apply_leg_offset(
                pose,
                i,
                HIP_BACK / (LEG_COUNT - 1),
                KNEE_SUPPORT
            )

    return pose

# ---------------- SCHEDULER LOOP ----------------

def run_scheduler(get_base_pose, send_pose_callback):
    global current_leg_index, phase_time

    while True:
        start = time.time()

        base_pose = get_base_pose()

        pose = generate_wave_gait(base_pose)

        send_pose_callback(pose)

        # Timing
        phase_time += DT
        if phase_time >= STEP_DURATION:
            phase_time = 0.0
            current_leg_index = (current_leg_index + 1) % LEG_COUNT

        elapsed = time.time() - start
        time.sleep(max(0, DT - elapsed))

# ---------------- SAFETY ----------------

def reset_gait():
    global current_leg_index, phase_time
    current_leg_index = 0
    phase_time = 0.0

# ---------------- TEST ----------------

if __name__ == "__main__":
    def mock_base_pose():
        return [90.0] * SERVO_COUNT

    def debug_send(pose):
        print(["{:.1f}".format(p) for p in pose])

    run_scheduler(mock_base_pose, debug_send)
