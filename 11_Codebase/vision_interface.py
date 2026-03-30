"""
vision_interface.py
OBSIDIAN-8 V3 — REV D
Handles camera streams, preprocessing, and feeds to detection/tracking modules
"""

import cv2
import threading
import time
from image_preprocessing import ImagePreprocessor

class VisionInterface:
    def __init__(self, camera_sources=None, target_size=(640, 480)):
        """
        camera_sources: list of int (device indices) or str (video paths)
        """
        if camera_sources is None:
            camera_sources = [0]  # Default to first webcam

        self.cameras = [cv2.VideoCapture(src) for src in camera_sources]
        self.frames = [None] * len(self.cameras)
        self.lock = threading.Lock()
        self.running = False
        self.preprocessor = ImagePreprocessor(target_size=target_size)

    def capture_loop(self, cam_index):
        cap = self.cameras[cam_index]
        while self.running:
            ret, frame = cap.read()
            if ret:
                processed = self.preprocessor.preprocess(frame)
                with self.lock:
                    self.frames[cam_index] = processed
            time.sleep(0.01)  # ~100 Hz capture loop

    def start(self):
        self.running = True
        self.threads = []
        for i in range(len(self.cameras)):
            t = threading.Thread(target=self.capture_loop, args=(i,))
            t.start()
            self.threads.append(t)

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()
        for cap in self.cameras:
            cap.release()

    def get_frame(self, cam_index=0):
        with self.lock:
            return self.frames[cam_index]

    def get_all_frames(self):
        with self.lock:
            return list(self.frames)

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    vi = VisionInterface(camera_sources=[0,1], target_size=(640,480))
    vi.start()

    try:
        while True:
            frames = vi.get_all_frames()
            for idx, frame in enumerate(frames):
                if frame is not None:
                    cv2.imshow(f"Camera {idx}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        vi.stop()
        cv2.destroyAllWindows()
        print("[VisionInterface] Stopped")
