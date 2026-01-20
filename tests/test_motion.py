import numpy as np
from detectors.motion import detect_motion
from config import MotionConfig


def test_no_motion_black_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    has_motion, _ = detect_motion(frame, 0, MotionConfig())
    assert has_motion is False
