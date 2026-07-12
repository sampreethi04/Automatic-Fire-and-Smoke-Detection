"""
helpers.py
Helper functions for Automatic Fire and Smoke Detection System
"""

import cv2
import datetime
import os

from utils.colors import *


def draw_text(frame, text, position,
              color=WHITE,
              scale=0.7,
              thickness=2):

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA
    )


def draw_box(frame,
             x1,
             y1,
             x2,
             y2,
             label,
             confidence,
             color):

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        2
    )

    text = f"{label} {confidence:.2f}"

    (w, h), _ = cv2.getTextSize(
        text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        2
    )

    cv2.rectangle(
        frame,
        (x1, y1 - 25),
        (x1 + w + 10, y1),
        color,
        -1
    )

    cv2.putText(
        frame,
        text,
        (x1 + 5, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        WHITE,
        2
    )


def draw_risk_level(frame,
                    risk_level,
                    score):

    color = RISK_COLORS.get(risk_level, GREEN)

    text = f"Risk : {risk_level}"

    cv2.rectangle(
        frame,
        (10, 10),
        (320, 60),
        color,
        -1
    )

    cv2.putText(
        frame,
        text,
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        WHITE,
        2
    )

    cv2.putText(
        frame,
        f"Score : {score:.2f}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


def draw_fps(frame, fps):

    cv2.putText(
        frame,
        f"FPS : {fps}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        CYAN,
        2
    )


def current_timestamp():

    return datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


def ensure_directory(path):

    if not os.path.exists(path):
        os.makedirs(path)


def save_image(frame, folder):

    ensure_directory(folder)

    filename = os.path.join(
        folder,
        current_timestamp() + ".jpg"
    )

    cv2.imwrite(filename, frame)

    return filename


def resize_frame(frame,
                 width=1280,
                 height=720):

    return cv2.resize(
        frame,
        (width, height)
    )


def put_system_status(frame,
                      status="RUNNING"):

    color = GREEN if status == "RUNNING" else RED

    cv2.putText(
        frame,
        f"System : {status}",
        (20, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )
