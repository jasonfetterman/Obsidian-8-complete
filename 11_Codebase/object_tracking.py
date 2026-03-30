"""
object_tracking.py
OBSIDIAN-8 V3 — REV D
Tracks detected objects across frames, maintains unique IDs and history
"""

import numpy as np
from collections import deque
from scipy.spatial.distance import cdist

class TrackedObject:
    def __init__(self, obj_id, bbox, max_history=20):
        self.id = obj_id
        self.bbox = bbox
        self.history = deque(maxlen=max_history)

    def update(self, bbox):
        self.bbox = bbox
        center = [(bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2]
        self.history.append(center)

class ObjectTracker:
    def __init__(self, max_distance=50.0):
        self.tracked_objects = []
        self.next_id = 0
        self.max_distance = max_distance

    def update(self, detections):
        """
        detections: list of dicts from ObjectDetection
        Returns: list of TrackedObject
        """
        if not self.tracked_objects:
            for det in detections:
                obj = TrackedObject(self.next_id, det["bbox"])
                obj.update(det["bbox"])
                self.tracked_objects.append(obj)
                self.next_id += 1
            return self.tracked_objects

        # Compute current tracked centers
        tracked_centers = np.array([[(t.bbox[0]+t.bbox[2])/2, (t.bbox[1]+t.bbox[3])/2] for t in self.tracked_objects])
        detected_centers = np.array([[(d["bbox"][0]+d["bbox"][2])/2, (d["bbox"][1]+d["bbox"][3])/2] for d in detections])

        # Compute distance matrix
        if len(tracked_centers) > 0 and len(detected_centers) > 0:
            dist_matrix = cdist(tracked_centers, detected_centers)
            assigned = set()
            for t_idx, obj in enumerate(self.tracked_objects):
                d_idx = np.argmin(dist_matrix[t_idx])
                if dist_matrix[t_idx, d_idx] < self.max_distance and d_idx not in assigned:
                    obj.update(detections[d_idx]["bbox"])
                    assigned.add(d_idx)

            # Add new detections
            for i, det in enumerate(detections):
                if i not in assigned:
                    obj = TrackedObject(self.next_id, det["bbox"])
                    obj.update(det["bbox"])
                    self.tracked_objects.append(obj)
                    self.next_id += 1
        else:
            # No tracked objects: add all detections
            for det in detections:
                obj = TrackedObject(self.next_id, det["bbox"])
                obj.update(det["bbox"])
                self.tracked_objects.append(obj)
                self.next_id += 1

        return self.tracked_objects

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    from object_detection import ObjectDetection
    import cv2
    from image_preprocessing import ImagePreprocessor

    cap = cv2.VideoCapture(0)
    preprocessor = ImagePreprocessor()
    detector = ObjectDetection(model_path="yolov8n.pt", device="cuda")
    tracker = ObjectTracker(max_distance=50.0)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed = preprocessor.preprocess(frame)
            detections = detector.detect(processed)
            tracked_objects = tracker.update(detections)

            # Draw tracked objects
            for obj in tracked_objects:
                x1, y1, x2, y2 = map(int, obj.bbox)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
                cv2.putText(frame, f"ID:{obj.id}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

            cv2.imshow("Tracked Objects", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[ObjectTracking] Stopped")
