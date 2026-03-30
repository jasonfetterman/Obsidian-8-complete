# stereo_depth.py
# OBSIDIAN-8 V3 — REV D
# Computes depth from stereo camera pair for navigation and obstacle detection

import cv2
import numpy as np
from depthai_sdk import OakCamera  # Luxonis OAK-D Pro
import pyrealsense2 as rs          # Intel RealSense D455

class StereoDepth:
    def __init__(self, use_oak=True):
        self.use_oak = use_oak
        if self.use_oak:
            self.pipeline = OakCamera()
            self.pipeline.start()
        else:
            # RealSense setup
            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            self.pipeline.start(config)

    def get_depth_frame(self):
        """
        Returns depth frame as a numpy array (meters)
        """
        if self.use_oak:
            frames, _ = self.pipeline.get_frames()
            depth_frame = frames.depth
            depth_np = np.asanyarray(depth_frame)
            return depth_np.astype(np.float32) / 1000.0  # mm -> meters
        else:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            depth_np = np.asanyarray(depth_frame.get_data())
            return depth_np.astype(np.float32) / 1000.0

    def get_point_cloud(self):
        """
        Converts depth map to 3D point cloud in camera coordinates
        """
        depth = self.get_depth_frame()
        h, w = depth.shape
        fx = fy = 0.5 * w / np.tan(np.deg2rad(60)/2)  # approximate focal length
        cx, cy = w/2, h/2

        indices = np.indices((h, w), dtype=np.float32)
        x = (indices[1] - cx) * depth / fx
        y = (indices[0] - cy) * depth / fy
        z = depth
        points = np.stack((x, y, z), axis=-1)
        return points

    def shutdown(self):
        if self.use_oak:
            self.pipeline.stop()
        else:
            self.pipeline.stop()
