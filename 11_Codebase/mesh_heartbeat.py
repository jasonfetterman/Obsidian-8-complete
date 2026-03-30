"""
mesh_heartbeat.py
OBSIDIAN-8 V3 — REV D
Maintains live heartbeat and connectivity with swarm bots
"""

import threading
import time
from swarm_comms import SwarmComms

class MeshHeartbeat:
    def __init__(self, swarm: SwarmComms, heartbeat_interval=1.0):
        """
        swarm: instance of SwarmComms
        heartbeat_interval: seconds between heartbeats
        """
        self.swarm = swarm
        self.heartbeat_interval = heartbeat_interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.heartbeat_loop)
        self.thread.start()
        print("[MeshHeartbeat] Heartbeat started")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("[MeshHeartbeat] Heartbeat stopped")

    def heartbeat_loop(self):
        while self.running:
            all_states = self.swarm.get_all_states()
            for bot_id in all_states:
                # Send ping
                msg = {"bot_id": "OBSIDIAN_MASTER", "command": "heartbeat"}
                self.swarm.send_command(bot_id, msg)
            # Cleanup inactive bots
            self.swarm.cleanup_inactive(timeout=5.0)
            time.sleep(self.heartbeat_interval)

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    from swarm_comms import SwarmComms
    swarm = SwarmComms(swarm_size=50)
    swarm.start()
    heartbeat = MeshHeartbeat(swarm)
    heartbeat.start()

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        heartbeat.stop()
        swarm.stop()
