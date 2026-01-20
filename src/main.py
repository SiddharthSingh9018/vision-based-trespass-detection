import cv2
import smtplib
from email.mime.text import MIMEText
import time
import os
from ultralytics import YOLO
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
from json import load

model = YOLO("yolov8n.pt", verbose=False)

caps = []
cams = []
with open('data.json', 'r') as file:
    data = load(file)
    for item in data:
        cap = cv2.VideoCapture(item.get('link', None))
        if cap.isOpened():
            width = item.get('width', None)  
            height = item.get('height', None)
            if width and height:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
            caps.append(cap)
            cams.append(item)
        else:
            print(f"Unable to open camera {item['link']}")

load_dotenv()
sender_email = os.getenv('SENDER_EMAIL')
receiver_email = os.getenv('RECEIVER_EMAIL')
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_password = os.getenv("SENDER_PASS")
notification_cooldown_period = 300
last_trespass_alert_times = [0] * len(caps)

has_motions = [False] * len(caps)
last_motion_ats = [0] * len(caps)
check_period = 5

backSub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=16, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

fps = 5
i = 1


def add_text(frame, text):
    """Adds text to the top-left corner of a frame."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame

def arrange_frames(frames, frame_size=(320, 240)):
    """Arrange frames in a grid layout."""
    num_frames = len(frames)
    cols = int(np.ceil(np.sqrt(num_frames)))
    rows = int(np.ceil(num_frames / cols))
    
    blank_image = np.zeros((rows * frame_size[1], cols * frame_size[0], 3), dtype=np.uint8)

    for idx, frame in enumerate(frames):
        if frame is None:
            frame = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)
        resized_frame = cv2.resize(frame, frame_size)
        labeled_frame = add_text(resized_frame, f"Frame {idx}")

        row, col = divmod(idx, cols)
        y_start, y_end = row * frame_size[1], (row + 1) * frame_size[1]
        x_start, x_end = col * frame_size[0], (col + 1) * frame_size[0]
        blank_image[y_start:y_end, x_start:x_end] = labeled_frame

    return blank_image

def send_email_alert(timestamp, idx):
    subject = "Trespassing Alert"
    cam = cams[idx]
    body = f"A human trespassing event was detected at {timestamp}. Camera Info: Name: {cam.get('name', 'Cam Undefined')}, Description: {cam.get('desc', 'No description')}, Link: {cam.get('link', 'no link')}."
    print(subject, body)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print(f"Alert email sent at {timestamp}.")
    except Exception as e:
        print("Failed to send email:", e)



isEnd = False
frames = [0] * len(caps)

while not isEnd:
    for idx, cap in enumerate(caps):
        ret, frames[idx] = cap.read()
        if not ret:
            break

        if has_motions[idx]:
            if i % fps != 0:
                i += 1
                continue
            i = 1

            results = model.predict(frames[idx], verbose=False)
            human_detected = False

            for result in results:
                for box in result.boxes:
                    if int(box.cls.item()) == 0 and box.conf >= 0.5:  
                        human_detected = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frames[idx], (x1, y1), (x2, y2), (0, 0, 255), 2)
                        
            if human_detected and time.time() - last_trespass_alert_times[idx] >= notification_cooldown_period:
                last_trespass_alert_times[idx] = time.time()
                detection_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                send_email_alert(detection_time_str, idx)  

            if time.time() - last_motion_ats[idx] > check_period:
                has_motions[idx] = False
                last_motion_ats[idx] = time.time()
        else:
            human_detected = False
            fgMask = backSub.apply(frames[idx])
            fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = h / float(w)
                    if aspect_ratio > 1.2:
                        cv2.rectangle(frames[idx], (x, y), (x+w, y+h), (0, 255, 0), 2)
                        has_motions[idx] = True
                        last_motion_ats[idx] = time.time()
                        break
        if cv2.waitKey(1) == ord("q"):
            isEnd = True
        frames[idx] = add_text(frames[idx], cams[idx]['name'])
    cv2.imshow("Frame", arrange_frames(frames))
    if cv2.waitKey(1) == ord("q"):
        isEnd = True

for cap in caps:
    cap.release()
    
cv2.destroyAllWindows()