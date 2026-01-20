import cv2
import time
from config import MotionConfig

# Background subtractor and kernel are allowed module-level state
backSub = cv2.createBackgroundSubtractorMOG2(
    history=100,
    varThreshold=16,
    detectShadows=False
)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


def detect_motion(frame, last_motion_at, cfg: MotionConfig):
    """
    Detects motion in a frame using background subtraction.

    Returns:
        has_motion (bool)
        updated_last_motion_at (float)
    """
    fgMask = backSub.apply(frame)
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(
        fgMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) > cfg.min_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / float(w)

            if aspect_ratio > cfg.aspect_ratio_thresh:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )
                return True, time.time()

    # decay motion flag if no motion persists
    if time.time() - last_motion_at > cfg.check_period:
        return False, last_motion_at

    return True, last_motion_at
