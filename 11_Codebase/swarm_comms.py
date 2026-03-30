"""
swarm_comms.py
OBSIDIAN-8 V3 — REV D
Manages communication with up to 50 swarm robots
Handles command distribution, state collection, and shared perception
"""

import socket
import threading
import json
import time

class SwarmComms:
    def __init__(self, swarm_size=50, listen_ip="0.0.0.0", listen_port=9000):
        self.swarm_size = swarm_size
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.bots = {}  # bot_id -> last state
        self.lock = threading.Lock()
        self.running = False

        # UDP socket for lightweight state updates and commands
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.listen_ip, self.listen_port))
        self.sock.settimeout(0.1)  # Non-blocking

        print(f"[SwarmComms] Listening on {self.listen_ip}:{self.listen_port}")

    def start(self):
        self.running = True
        self.recv_thread = threading.Thread(target=self.receive_loop)
        self.recv_thread.start()

    def stop(self):
        self.running = False
        self.recv_thread.join()
        self.sock.close()
        print("[SwarmComms] Stopped")

    # ---------------- Receiving ----------------
    def receive_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                message = json.loads(data.decode("utf-8"))
                bot_id = message.get("bot_id")
                state = message.get("state")
                with self.lock:
                    if bot_id is not None:
                        self.bots[bot_id] = {"state": state, "last_seen": time.time(), "addr": addr}
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[SwarmComms] Receive error: {e}")

    # ---------------- Sending ----------------
    def send_command(self, bot_id, command_dict):
        """
        command_dict: arbitrary dict with commands (e.g., motion, tasks)
        """
        with self.lock:
            bot_info = self.bots.get(bot_id)
            if bot_info:
                addr = bot_info["addr"]
                msg = json.dumps(command_dict).encode("utf-8")
                self.sock.sendto(msg, addr)

    def broadcast_command(self, command_dict):
        """Send same command to all known swarm bots"""
        with self.lock:
            for bot_id, bot_info in self.bots.items():
                msg = json.dumps(command_dict).encode("utf-8")
                self.sock.sendto(msg, bot_info["addr"])

    # ---------------- Utilities ----------------
    def get_bot_state(self, bot_id):
        with self.lock:
            return self.bots.get(bot_id)

    def get_all_states(self):
        with self.lock:
            return self.bots.copy()

    def cleanup_inactive(self, timeout=5.0):
        """Remove bots not seen for a certain period"""
        with self.lock:
            now = time.time()
            inactive = [bot_id for bot_id, info in self.bots.items() if now - info["last_seen"] > timeout]
            for bot_id in inactive:
                print(f"[SwarmComms] Removing inactive bot: {bot_id}")
                del self.bots[bot_id]

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    swarm = SwarmComms(swarm_size=50, listen_port=9000)
    swarm.start()
    print("[SwarmComms] Running. Ctrl+C to stop.")

    try:
        while True:
            all_states = swarm.get_all_states()
            if all_states:
                print(f"[SwarmComms] Active bots: {list(all_states.keys())}")
            time.sleep(1.0)
            swarm.cleanup_inactive(timeout=10.0)
    except KeyboardInterrupt:
        swarm.stop()
