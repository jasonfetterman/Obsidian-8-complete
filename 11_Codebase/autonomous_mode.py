# autonomous_mode.py
# OBSIDIAN-8 V3 — REV D
# Full autonomous control integrating vision, sensors, swarm, and persistent mapping

import time
from vision_interface import VisionInterface
from object_detection import ObjectDetection
from swarm_comms import SwarmComms
from map_manager import MapManager
import ctypes
import threading

# Load foot_sensor shared library compiled from foot_sensor.cpp
foot_lib = ctypes.CDLL('./foot_sensor.so')
foot_lib.read.restype = ctypes.POINTER(ctypes.c_bool * 8)

class AutonomousMode:
    def __init__(self, node_id="OB8-Node1", map_manager=None):
        # Vision and object detection
        self.vision = VisionInterface(use_oak=True)
        self.detector = ObjectDetection(use_oak=True)
        self.tracker = self.vision.tracker

        # Swarm communications
        self.swarm = SwarmComms(node_id=node_id)

        # Foot sensor data
        self.foot_state = [False]*8

        # Map Manager for persistent environment memory
        self.map_manager = map_manager

        self.running = True

    def read_feet(self):
        """Reads foot contact sensors via compiled C++ shared library"""
        raw_ptr = foot_lib.read()
        self.foot_state = list(raw_ptr.contents)

    def process_vision(self):
        """Runs detection and updates tracker"""
        detections = self.detector.detect_objects()
        # Extract only bounding boxes for tracker
        rects = [(x1, y1, x2, y2) for (x1, y1, x2, y2, cls, conf) in detections]
        tracked_objects = self.tracker.update(rects)

        # Feed detected obstacles into the map_manager
        if self.map_manager:
            for obj_id, bbox in tracked_objects.items():
                # Convert bbox centroid to meters
                x_m = (bbox[0] + bbox[2]) / 2.0 * 0.001  # example conversion
                y_m = (bbox[1] + bbox[3]) / 2.0 * 0.001
                self.map_manager.update_cell(x_m, y_m, 1)  # mark occupied

        return tracked_objects

    def swarm_heartbeat(self):
        """Periodically broadcast status to swarm"""
        while self.running:
            self.swarm.send({
                "type": "heartbeat",
                "node_id": self.swarm.node_id,
                "timestamp": time.time(),
                "foot_state": self.foot_state
            })
            time.sleep(1)

    def run(self):
        """Main autonomous loop"""
        # Start swarm heartbeat thread
        heartbeat_thread = threading.Thread(target=self.swarm_heartbeat)
        heartbeat_thread.start()

        try:
            while self.running:
                # 1. Read foot sensors
                self.read_feet()

                # 2. Vision processing
                tracked_objects = self.process_vision()
                print("Tracked objects:", tracked_objects)
                print("Foot states:", self.foot_state)

                # 3. Swarm messages
                messages = self.swarm.get_messages()
                for msg in messages:
                    print("Received swarm msg:", msg)

                # 4. TODO: Motion planner integration
                # Use tracked_objects + foot_state + map_manager for gait commands

                time.sleep(0.05)  # 20 Hz loop
        finally:
            self.shutdown()
            heartbeat_thread.join()

    def shutdown(self):
        self.running = False
        self.vision.shutdown()
        self.detector.shutdown()
        self.swarm.shutdown()
        if self.map_manager:
            self.map_manager.shutdown()
        print("[AutonomousMode] Shutdown complete.")


# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    map_mgr = MapManager()
    autonomous = AutonomousMode(node_id="OB8-Node1", map_manager=map_mgr)
    autonomous.run()
