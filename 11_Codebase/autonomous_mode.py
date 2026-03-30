"""
autonomous_mode.py
OBSIDIAN-8 V3 — REV D
Integrates sensor data, object tracking, depth maps, and swarm comms
for fully autonomous navigation and task execution
"""

import time
import numpy as np
from imu_reader import IMUReader
from foot_sensor import FootSensor
from stereo_depth import StereoDepth
from image_preprocessing import ImagePreprocessor
from object_detection import ObjectDetector
from object_tracking import ObjectTracker
from swarm_comms import SwarmComms

class AutonomousMode:
    def __init__(self, robot_id="OBS8-01"):
        # Sensors
        self.imu = IMUReader()
        self.foot_sensors = FootSensor()
        self.stereo = StereoDepth()
        self.preprocessor = ImagePreprocessor(target_size=(640,480))
        self.detector = ObjectDetector(model_path="yolov8n.pt", device="cuda")
        self.tracker = ObjectTracker()
        
        # Swarm communication
        self.swarm = SwarmComms(robot_id=robot_id, port=5000)
        self.swarm.start()
        
        self.running = False

    def get_robot_state(self):
        imu_data = {
            "quaternion": self.imu.getQuaternion(),
            "accel": self.imu.getAccel(),
            "gyro": self.imu.getGyro()
        }
        foot_state = self.foot_sensors.read()
        return {"imu": imu_data, "foot": foot_state}

    def perceive_environment(self):
        oak_depth = self.stereo.get_oakd_depth()
        rs_depth = self.stereo.get_realsense_depth()

        # Choose best available depth
        depth = oak_depth if oak_depth is not None else rs_depth

        ret, frame = True, np.zeros((480,640,3), dtype=np.uint8)
        if ret:
            processed = self.preprocessor.preprocess(frame)
            detections = self.detector.detect(processed)
            tracked = self.tracker.update(detections)
            return depth, tracked
        return depth, []

    def broadcast_state(self):
        state = {
            "robot_state": self.get_robot_state(),
            "timestamp": time.time()
        }
        self.swarm.broadcast(state)

    def autonomous_loop(self):
        self.foot_sensors.start()
        self.running = True
        try:
            while self.running:
                # Update sensors
                self.imu.update()
                
                # Perceive environment
                depth_map, tracked_objects = self.perceive_environment()
                
                # Broadcast to swarm
                self.broadcast_state()
                
                # Here, path planning / motion commands would be issued
                # Example: plan next footstep or trajectory
                # This can be integrated with motion_planner.py and path_planner.py

                time.sleep(0.05)  # 20 Hz main loop
        finally:
            self.foot_sensors.stop()
            self.swarm.stop()
            self.stereo.shutdown()

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    auto_mode = AutonomousMode(robot_id="OBS8-01")
    try:
        auto_mode.autonomous_loop()
    except KeyboardInterrupt:
        print("[AutonomousMode] Stopped by user")
