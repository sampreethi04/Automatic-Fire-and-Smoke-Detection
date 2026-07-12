"""
logger.py
Evidence Logging Module for Automatic Fire and Smoke Detection System
"""

import cv2
import os
import datetime

from config import (
    IMAGE_FOLDER,
    VIDEO_FOLDER,
    LOG_FILE,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    VIDEO_CODEC,
    VIDEO_EXTENSION
)


class EvidenceLogger:

    def __init__(self):

        self.video_writer = None

        self.recording = False

        self.video_path = None

    def timestamp(self):

        return datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

    def save_image(self, frame, risk_level):

        filename = os.path.join(
            IMAGE_FOLDER,
            f"{risk_level}_{self.timestamp()}.jpg"
        )

        cv2.imwrite(filename, frame)

        self.write_log(
            f"Image Saved : {filename}"
        )

        return filename

    def start_recording(self, risk_level):

        if self.recording:
            return

        self.video_path = os.path.join(
            VIDEO_FOLDER,
            f"{risk_level}_{self.timestamp()}{VIDEO_EXTENSION}"
        )

        fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)

        self.video_writer = cv2.VideoWriter(
            self.video_path,
            fourcc,
            20,
            (FRAME_WIDTH, FRAME_HEIGHT)
        )

        self.recording = True

        self.write_log(
            f"Recording Started : {self.video_path}"
        )

    def write_frame(self, frame):

        if self.recording and self.video_writer is not None:

            self.video_writer.write(frame)

    def stop_recording(self):

        if self.video_writer is not None:

            self.video_writer.release()

        self.video_writer = None

        self.recording = False

        self.write_log(
            "Recording Stopped"
        )

    def write_log(self, message):

        time = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(LOG_FILE, "a") as file:

            file.write(
                f"[{time}] {message}\n"
            )

    def log_detection(
            self,
            risk_level,
            fire_count,
            smoke_count,
            score):

        message = (
            f"Risk={risk_level} | "
            f"Fire={fire_count} | "
            f"Smoke={smoke_count} | "
            f"Score={score:.2f}"
        )

        self.write_log(message)

    def cleanup(self):

        self.stop_recording()
