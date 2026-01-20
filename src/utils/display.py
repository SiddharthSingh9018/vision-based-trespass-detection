import cv2
import numpy as np


def add_text(frame, text):
    """
    Adds a label to the top-left corner of a frame.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        frame,
        text,
        (10, 30),
        font,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    return frame


def arrange_frames(frames, frame_size=(320, 240)):
    """
    Arranges multiple frames into a grid for display.
    """
    valid_frames = [
        frame if frame is not None else np.zeros(
            (frame_size[1], frame_size[0], 3), dtype=np.uint8
        )
        for frame in frames
    ]

    num_frames = len(valid_frames)
    cols = int(np.ceil(np.sqrt(num_frames)))
    rows = int(np.ceil(num_frames / cols))

    canvas = np.zeros(
        (rows * frame_size[1], cols * frame_size[0], 3),
        dtype=np.uint8,
    )

    for idx, frame in enumerate(valid_frames):
        resized = cv2.resize(frame, frame_size)
        row, col = divmod(idx, cols)

        y1 = row * frame_size[1]
        y2 = y1 + frame_size[1]
        x1 = col * frame_size[0]
        x2 = x1 + frame_size[0]

        canvas[y1:y2, x1:x2] = resized

    return canvas
