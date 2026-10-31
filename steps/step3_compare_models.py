# Step 3: measure how long each model takes on the same frame.
from ultralytics import YOLO
import cv2
import time

cam = cv2.VideoCapture(0)
for i in range(10):
    ok, frame = cam.read()
cam.release()

for path in ["yolov8n.pt", "yolov8n-oiv7.pt"]:
    model = YOLO(path)
    model(frame, verbose=False)          # warm-up, not counted
    start = time.time()
    for i in range(20):
        model(frame, conf=0.3, verbose=False)
    ms = (time.time() - start) / 20 * 1000
    print(path, round(ms), "ms per frame")

# Check which of my objects exist in the Open Images V7 class list.
names = YOLO("yolov8n-oiv7.pt").names
for word in ["footwear", "pen", "spoon", "handbag", "cigarette", "stairs"]:
    print(word, "->", [n for n in names.values() if word in n.lower()])
