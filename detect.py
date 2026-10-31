from ultralytics import YOLO
import cv2
import time

from speech import say, is_idle
from logic import describe, IGNORE, PERSON

model = YOLO("yolov8n-oiv7.pt")
cam = cv2.VideoCapture(0)

last_spoken = {}
COOLDOWN = 3

while True:
    ok, frame = cam.read()
    if not ok:
        break

    result = model(frame, conf=0.3, verbose=False)[0]
    H, W = frame.shape[:2]

    best = None
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        name = model.names[int(box.cls[0])]
        conf = float(box.conf[0])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} {conf:.2f}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if name in IGNORE:
            continue
        if name in PERSON:
            name = "person"

        side, near = describe(x1, y1, x2, y2, W, H)
        size = (y2 - y1) / H
        if best is None or size > best[0]:
            best = (size, name, side, near)

    if best:
        _, name, side, near = best
        key = (name, side)
        now = time.time()
        if now - last_spoken.get(key, 0) > COOLDOWN and is_idle():
            last_spoken[key] = now
            say(f"{name}, {side}, {near}")

    cv2.imshow("detect", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
