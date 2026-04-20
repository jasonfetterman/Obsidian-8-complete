import socket
import json
import threading
import time


class SwarmComms:
    def __init__(self, listen_port=5005, broadcast_port=5006):
        self.listen_port = listen_port
        self.broadcast_port = broadcast_port

        self.running = True

        # Latest command
        self.latest_command = {"vx": 0, "vy": 0, "w": 0}

        # Node ID (simple for now)
        self.node_id = f"node_{int(time.time())}"

        # Socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.listen_port))
        self.sock.setblocking(False)

        # Start listener thread
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    # =========================
    # LISTEN LOOP
    # =========================
    def _listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                message = json.loads(data.decode())

                if self._validate(message):
                    self._handle_message(message)

            except BlockingIOError:
                time.sleep(0.01)
            except Exception as e:
                print(f"[COMMS ERROR] {e}")

    # =========================
    # MESSAGE HANDLING
    # =========================
    def _handle_message(self, msg):
        msg_type = msg.get("type")

        if msg_type == "COMMAND":
            self.latest_command = msg.get("data", self.latest_command)

        elif msg_type == "HEARTBEAT":
            pass  # future use

        elif msg_type == "TELEMETRY":
            pass  # future swarm sharing

    def _validate(self, msg):
        return isinstance(msg, dict) and "type" in msg

    # =========================
    # PUBLIC INTERFACE
    # =========================
    def get_teleop_commands(self):
        return self.latest_command

    def send_telemetry(self, state):
        msg = {
            "type": "TELEMETRY",
            "node": self.node_id,
            "data": state
        }
        self._broadcast(msg)

    def send_heartbeat(self):
        msg = {
            "type": "HEARTBEAT",
            "node": self.node_id,
            "timestamp": time.time()
        }
        self._broadcast(msg)

    # =========================
    # NETWORK
    # =========================
    def _broadcast(self, message):
        try:
            data = json.dumps(message).encode()
            self.sock.sendto(data, ("<broadcast>", self.broadcast_port))
        except Exception as e:
            print(f"[SEND ERROR] {e}")

    def shutdown(self):
        self.running = False
        self.sock.close()
