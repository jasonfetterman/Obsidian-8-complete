"""
object_detection.py
OBSIDIAN-8 V3 — REV D
Detects objects in camera frames using YOLOv8 and outputs bounding boxes for tracking
"""

import torch
import numpy as np

class ObjectDetection:
    def __init__(self, model_path="yolov8n.pt", device="cuda"):
        """
        model_path: path to YOLOv8 model weights
        device: 'cuda' or 'cpu'
        """
        self.device = device
        self.model = torch.hub.load('ultralytics/yolov8', 'custom', path=model_path, force_reload=False)
        self.model.to(device)
        self.model.eval()

    def detect(self, frame):
        """
        frame: preprocessed image (numpy array, HxWxC, RGB)
        Returns: list of dicts with keys ['id', 'bbox', 'confidence', 'class_name']
        """
        results = self.model(frame)
        detections = []

        for i, det in enumerate(results.xyxy[0]):  # xyxy: x1, y1, x2, y2, conf, class
            x1, y1, x2, y2, conf, cls = det.cpu().numpy()
            detections.append({
                "id": i,
                "bbox": [x1, y1, x2, y2],
                "confidence": float(conf),
                "class_id": int(cls),
                "class_name": self.model.names[int(cls)]
            })
        return detections

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    import cv2
    from image_preprocessing import ImagePreprocessor

    cap = cv2.VideoCapture(0)
    preprocessor = ImagePreprocessor(target_size=(640,480))
    detector = ObjectDetection(model_path="yolov8n.pt", device="cuda")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed = preprocessor.preprocess(frame)
            detections = detector.detect(processed)

            for det in detections:
                x1, y1, x2, y2 = map(int, det["bbox"])
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, f"{det['class_name']}:{det['confidence']:.2f}",
                            (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            cv2.imshow("Detections", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[ObjectDetection] Stopped")
