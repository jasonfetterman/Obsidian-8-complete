# image_preprocessing.py
# OBSIDIAN-8 V3 — REV D
# Preprocesses camera images for object detection and vision pipeline

import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self, target_width=640, target_height=480, undistort_params=None):
        """
        target_width, target_height: desired image resolution
        undistort_params: dict with 'K' and 'D' (camera matrix and distortion coefficients)
        """
        self.width = target_width
        self.height = target_height
        self.undistort_params = undistort_params

        if undistort_params:
            K = undistort_params['K']
            D = undistort_params['D']
            self.map1, self.map2 = cv2.initUndistortRectifyMap(K, D, None, K,
                                                               (self.width, self.height),
                                                               cv2.CV_32FC1)
        else:
            self.map1 = None
            self.map2 = None

    def preprocess(self, frame):
        """
        Preprocess input frame:
        1. Resize
        2. Undistort (if params provided)
        3. Convert to grayscale
        4. Apply Gaussian blur
        """
        frame_resized = cv2.resize(frame, (self.width, self.height))

        if self.map1 is not None and self.map2 is not None:
            frame_undistorted = cv2.remap(frame_resized, self.map1, self.map2, cv2.INTER_LINEAR)
        else:
            frame_undistorted = frame_resized

        frame_gray = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

        return frame_blur

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    preprocessor = ImagePreprocessor(target_width=640, target_height=480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed = preprocessor.preprocess(frame)
        cv2.imshow("Processed", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
