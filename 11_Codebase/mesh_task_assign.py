# mesh_task_assign.py
# OBSIDIAN-8 V3 — REV D
# Dynamically assigns tasks to swarm nodes based on load and availability

import random
import socket
import time

# -------------------- CONFIG --------------------
SWARM_NODES = [
    "192.168.50.101",
    "192.168.50.102",
    "192.168.50.103",
]

MESH_PORT = 5000
TASKS = [
    "survey_area",
    "sample_collection",
    "inspection",
    "battery_check",
]

# -------------------- FUNCTIONS --------------------
def assign_task(node_ip: str, task: str):
    """Send task assignment via UDP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        message = f"TASK:{task}".encode("utf-8")
        sock.sendto(message, (node_ip, MESH_PORT))
        sock.close()
        print(f"[Task Assign] Assigned '{task}' to {node_ip}")
    except Exception as e:
        print(f"[Task Assign] Failed to assign '{task}' to {node_ip}: {e}")

def distribute_tasks():
    """Assign tasks randomly for demo; can implement load-balancing logic"""
    for node in SWARM_NODES:
        task = random.choice(TASKS)
        assign_task(node, task)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    while True:
        distribute_tasks()
        time.sleep(10)  # Assign every 10 seconds
