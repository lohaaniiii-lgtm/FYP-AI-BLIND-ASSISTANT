# Step 1: grab one frame from the webcam and see what the model finds.
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)

# The very first frame is often dark (exposure not ready), so skip 10 frames.
for i in range(10):
    ok, frame = cam.read()

cv2.imwrite("test.jpg", frame)
result = model(frame)[0]
print(result.boxes)
cam.release()
