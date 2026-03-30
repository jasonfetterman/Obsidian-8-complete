# vision_interface.py
# OBSIDIAN-8 V3 — REV D
# Central interface for camera inputs, preprocessing, depth, and object tracking

import cv2
from stereo_depth import StereoDepth
from image_preprocessing import ImagePreprocessor
from object_tracking import ObjectTracker

class VisionInterface:
    def __init__(self, use_oak=True, undistort_params=None):
        self.stereo = StereoDepth(use_oak=use_oak)
        self.preprocessor = ImagePreprocessor(target_width=640, target_height=480,
                                              undistort_params=undistort_params)
        self.tracker = ObjectTracker(max_disappeared=10)

    def get_processed_frame(self):
        """
        Returns preprocessed frame ready for object detection/tracking
        """
        depth_frame = self.stereo.get_depth_frame()
        # Use RGB/color frame for preprocessing if OAK, else color from RealSense
        # For simplicity, using depth as placeholder; integrate color feed as needed
        frame = cv2.normalize(depth_frame, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
        processed = self.preprocessor.preprocess(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
        return processed

    def get_depth_points(self):
        """
        Returns point cloud in camera coordinates
        """
        return self.stereo.get_point_cloud()

    def update_tracking(self, detections):
        """
        detections: list of bounding boxes [(startX, startY, endX, endY)]
        Returns: dictionary {object_id: centroid}
        """
        return self.tracker.update(detections)

    def shutdown(self):
        self.stereo.shutdown()

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    vision = VisionInterface(use_oak=True)
    try:
        while True:
            frame = vision.get_processed_frame()
            # Simulated detections: for testing, create dummy bounding boxes
            detections = [(100,100,150,150), (300,200,350,250)]
            tracked_objects = vision.update_tracking(detections)
            print("Tracked Objects:", tracked_objects)
            cv2.imshow("Processed Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        vision.shutdown()
        cv2.destroyAllWindows()
