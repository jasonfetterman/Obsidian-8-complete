"""
swarm_comms.py
OBSIDIAN-8 V3 — REV D
Swarm communication module for sharing object positions, maps, and tasks
"""

import socket
import threading
import json
import time

class SwarmComms:
    def __init__(self, robot_id, port=5000):
        self.robot_id = robot_id
        self.port = port
        self.peers = {}  # {peer_id: (ip, port)}
        self.received_data = {}
        self.lock = threading.Lock()
        self.running = False

        # UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.port))
        self.sock.settimeout(0.5)

    def add_peer(self, peer_id, ip, port=5000):
        self.peers[peer_id] = (ip, port)

    def broadcast(self, data):
        """
        Send JSON data to all peers
        """
        msg = json.dumps({"robot_id": self.robot_id, "data": data}).encode('utf-8')
        for ip, port in self.peers.values():
            self.sock.sendto(msg, (ip, port))

    def receive_loop(self):
        while self.running:
            try:
                msg, addr = self.sock.recvfrom(4096)
                payload = json.loads(msg.decode('utf-8'))
                peer_id = payload["robot_id"]
                data = payload["data"]
                with self.lock:
                    self.received_data[peer_id] = data
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[SwarmComms] Error: {e}")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.receive_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.sock.close()

    def get_peer_data(self, peer_id):
        with self.lock:
            return self.received_data.get(peer_id, None)

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    swarm = SwarmComms(robot_id="OBS8-01", port=5000)
    swarm.add_peer("OBS8-02", "192.168.1.102")
    swarm.add_peer("OBS8-03", "192.168.1.103")
    swarm.start()

    try:
        counter = 0
        while True:
            # Example: broadcast own robot state
            data = {
                "position": [1.0 + counter*0.01, 2.0, 0.0],
                "objects": [{"id": 5, "pos": [3.0, 4.0, 0.0]}]
            }
            swarm.broadcast(data)
            counter += 1

            # Print received data from peers
            for peer_id in swarm.peers.keys():
                peer_data = swarm.get_peer_data(peer_id)
                if peer_data:
                    print(f"[Swarm] Data from {peer_id}: {peer_data}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        swarm.stop()
