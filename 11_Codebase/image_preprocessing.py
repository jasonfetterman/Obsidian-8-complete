"""
image_preprocessing.py
OBSIDIAN-8 V3 — REV D
Preprocesses raw camera frames for object detection and tracking
"""

import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self, target_size=(640, 480), normalize=True):
        """
        target_size: (width, height)
        normalize: whether to scale pixel values to 0-1
        """
        self.target_size = target_size
        self.normalize = normalize

    def preprocess(self, frame):
        """
        frame: raw RGB/BGR frame from camera
        Returns: preprocessed frame ready for detection
        """
        # Convert to RGB if needed
        if frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize
        frame_resized = cv2.resize(frame, self.target_size, interpolation=cv2.INTER_AREA)

        # Normalize
        if self.normalize:
            frame_resized = frame_resized.astype(np.float32) / 255.0

        return frame_resized

    def augment(self, frame):
        """
        Optional augmentation (flip, brightness, noise)
        """
        frame_aug = frame.copy()

        # Horizontal flip 50% chance
        if np.random.rand() > 0.5:
            frame_aug = cv2.flip(frame_aug, 1)

        # Random brightness adjustment
        alpha = 1.0 + (np.random.rand() - 0.5) * 0.2  # ±10%
        frame_aug = np.clip(frame_aug * alpha, 0, 1)

        # Gaussian noise
        noise = np.random.normal(0, 0.01, frame_aug.shape).astype(np.float32)
        frame_aug = np.clip(frame_aug + noise, 0, 1)

        return frame_aug

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    import cv2

    cap = cv2.VideoCapture(0)
    preprocessor = ImagePreprocessor(target_size=(640,480), normalize=True)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed = preprocessor.preprocess(frame)
            augmented = preprocessor.augment(processed)

            # Convert back to 0-255 for visualization
            vis = (augmented * 255).astype(np.uint8)
            cv2.imshow("Augmented Frame", cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[ImagePreprocessing] Stopped")
