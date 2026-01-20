import cv2
from ultralytics import YOLO
from config import HumanConfig

# Model weights are allowed as module-level state
model = YOLO("yolov8n.pt", verbose=False)


def detect_human(frame, cfg: HumanConfig):
    """
    Runs YOLO inference on a frame and draws boxes for detected humans.

    Returns:
        detected (bool)
    """
    results = model.predict(frame, verbose=False)
    detected = False

    for result in results:
        for box in result.boxes:
            if int(box.cls.item()) == 0 and box.conf >= cfg.conf_threshold:
                detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return detected
