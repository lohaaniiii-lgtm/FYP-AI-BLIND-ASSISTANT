# Step 4: decide which side an object is on and roughly how close it is.
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n-oiv7.pt")
cam = cv2.VideoCapture(0)


def describe(x1, y1, x2, y2, W, H):
    cx = (x1 + x2) / 2
    if cx < W / 3:
        side = "left"
    elif cx < 2 * W / 3:
        side = "center"
    else:
        side = "right"

    h_ratio = (y2 - y1) / H      # a bigger box means a closer object (an estimate)
    if h_ratio > 0.6:
        near = "very close"
    elif h_ratio > 0.35:
        near = "close"
    else:
        near = "far"
    return side, near


while True:
    ok, frame = cam.read()
    if not ok:
        break

    result = model(frame, conf=0.3, verbose=False)[0]
    H, W = frame.shape[:2]

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        name = model.names[int(box.cls[0])]
        side, near = describe(x1, y1, x2, y2, W, H)
        print(name, side, near)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("detect", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
