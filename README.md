# AI Blind Assistant: detection and voice core, built step by step

I built the detection-and-voice core of our final year project (AI Blind Assistant) on my laptop, 
## What it does

webcam frame -> YOLOv8n (Open Images V7 weights) -> which side (left, center, right) and how close (very close, close, far) -> one short spoken alert for the closest object, for example "person, center, very close".

## Run it (Windows)

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python detect.py
```

Press `q` in the video window to quit. Speech uses the offline Windows SAPI voice, so no internet is needed after the model has downloaded once.

## Files

| File | Job |
|---|---|
| `detect.py` | Opens the camera, runs the model, draws boxes |
| `logic.py` | Side, closeness, and what to ignore (face, clothing) or merge (Man, Woman -> person) |
| `speech.py` | Queue plus Windows voice running in its own thread, so video never freezes |
| `steps/` | The small scripts I wrote on the way, in order (step 1 to step 5) |

## What I measured (my laptop CPU only)

Average over 20 frames of the same image:

| Model | Classes | Time per frame |
|---|---|---|
| yolov8n.pt (COCO) | 80 | 108 ms |
| yolov8n-oiv7.pt (Open Images V7) | 601 | 155 ms |
| YOLO-World | any text prompt | 1020 ms |

I chose `yolov8n-oiv7.pt`: about 1.4 times slower than COCO, but it knows pen, footwear, spoon, handbag and stairs, and roughly 6.5 frames per second was enough for this. These timings are from a laptop, not a phone or a Raspberry Pi.

## Decisions along the way

- First camera frame was empty, so the code skips 10 frames before using one.
- A confidence threshold of 0.3 removes weak guesses (an early false "baseball bat" at 29%).
- Closeness is an estimate from box height, not a measured distance.
- `pyttsx3` went silent after one use, so speech runs through Windows SAPI in a separate thread with a queue and a 3 second cooldown.
- One person was announced three times (Man, Human face, Clothing), so only the biggest box is spoken and person parts are ignored.

## Limits

- This is an assistive aid. It does not replace a white cane, a guide dog or trained help.
- Stairs are found only when clearly visible. Drop-offs are not detected; that needs a distance sensor.
- Small objects such as a cigarette or pen are often missed and need fine-tuning on my own photos (next step).
- Wrong labels still happen at this confidence level.
