"""
mesh_task_assign.py
OBSIDIAN-8 V3 — REV D
Assigns tasks to swarm bots dynamically based on state and priorities
"""

import threading
import time
from swarm_comms import SwarmComms

class MeshTaskAssign:
    def __init__(self, swarm: SwarmComms, assign_interval=0.5):
        """
        swarm: instance of SwarmComms
        assign_interval: seconds between task assignment cycles
        """
        self.swarm = swarm
        self.assign_interval = assign_interval
        self.running = False
        self.thread = None
        self.task_queue = []  # list of tasks

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.task_loop)
        self.thread.start()
        print("[MeshTaskAssign] Task assignment started")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("[MeshTaskAssign] Task assignment stopped")

    def add_task(self, task):
        """Add a new task to the queue"""
        self.task_queue.append(task)

    def task_loop(self):
        while self.running:
            all_states = self.swarm.get_all_states()
            if not all_states or not self.task_queue:
                time.sleep(self.assign_interval)
                continue

            # Simple round-robin task assignment
            bots = list(all_states.keys())
            for i, task in enumerate(self.task_queue):
                bot_id = bots[i % len(bots)]
                command = {"bot_id": "OBSIDIAN_MASTER", "task": task}
                self.swarm.send_command(bot_id, command)

            # Clear tasks once assigned
            self.task_queue.clear()
            time.sleep(self.assign_interval)

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    from swarm_comms import SwarmComms
    swarm = SwarmComms(swarm_size=50)
    swarm.start()
    task_assigner = MeshTaskAssign(swarm)
    task_assigner.start()

    # Example tasks
    task_assigner.add_task({"action": "explore", "area": [0,0,10,10]})
    task_assigner.add_task({"action": "map_object", "object_id": 1})

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        task_assigner.stop()
        swarm.stop()
