import cv2
import time
from json import load
from datetime import datetime

from detectors.motion import detect_motion
from detectors.human import detect_human
from alerts.email import send_email_alert
from utils.display import add_text, arrange_frames


with open("data/raw/data.json") as f:
    cams = load(f)

caps = [cv2.VideoCapture(cam["link"]) for cam in cams]

has_motion = [False] * len(caps)
last_motion_at = [0] * len(caps)
last_alert = [0] * len(caps)

CHECK_PERIOD = 5
ALERT_COOLDOWN = 300

frames = [None] * len(caps)

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            continue

        if has_motion[i]:
            detected = detect_human(frame)
            if detected and time.time() - last_alert[i] > ALERT_COOLDOWN:
                last_alert[i] = time.time()
                send_email_alert(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    cams[i],
                )
        else:
            has_motion[i], last_motion_at[i] = detect_motion(
                frame, last_motion_at[i], CHECK_PERIOD
            )

        frames[i] = add_text(frame, cams[i]["name"])

    cv2.imshow("Trespass Monitor", arrange_frames(frames))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()
