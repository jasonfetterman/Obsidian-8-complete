# object_detection.py
# OBSIDIAN-8 V3 — REV D
# Object detection module using vision interface and AI models (YOLOv8 example)

import cv2
from vision_interface import VisionInterface
from ultralytics import YOLO  # YOLOv8

class ObjectDetection:
    def __init__(self, model_path="yolov8n.pt", use_oak=True, undistort_params=None):
        self.vision = VisionInterface(use_oak=use_oak, undistort_params=undistort_params)
        self.model = YOLO(model_path)  # load pre-trained YOLOv8 model

    def detect_objects(self):
        """
        Returns list of detections in format: [(startX, startY, endX, endY, class_id, confidence)]
        """
        frame = self.vision.get_processed_frame()
        results = self.model.predict(frame)
        detections = []

        for result in results:
            boxes = result.boxes.xyxy  # bounding boxes: x1,y1,x2,y2
            classes = result.boxes.cls  # class IDs
            confidences = result.boxes.conf  # confidence scores
            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = map(int, box)
                detections.append((x1, y1, x2, y2, int(cls), float(conf)))

        return detections

    def shutdown(self):
        self.vision.shutdown()

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    detector = ObjectDetection(model_path="yolov8n.pt", use_oak=True)
    try:
        while True:
            detections = detector.detect_objects()
            print("Detections:", detections)
    finally:
        detector.shutdown()
