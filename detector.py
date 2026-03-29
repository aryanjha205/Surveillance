from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_people(frame):
    results = model(frame)
    count = 0
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if model.names[cls] == 'person':
                count += 1
                frame = cv2.rectangle(
                    frame,
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                    (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                    (0, 255, 0), 2
                )
    return frame, count
