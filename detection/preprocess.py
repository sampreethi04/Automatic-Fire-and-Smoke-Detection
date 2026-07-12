"""
preprocess.py
Frame preprocessing module for Automatic Fire and Smoke Detection System
"""

import cv2
import numpy as np


class FramePreprocessor:

    def __init__(self,
                 input_size=(640, 640),
                 normalize=True):

        self.input_size = input_size
        self.normalize = normalize

    def resize(self, frame):
        """
        Resize frame for YOLO model.
        """
        return cv2.resize(frame, self.input_size)

    def normalize_frame(self, frame):
        """
        Normalize pixel values to range [0,1].
        """
        frame = frame.astype(np.float32)
        frame = frame / 255.0
        return frame

    def denormalize(self, frame):
        """
        Convert normalized image back to uint8.
        """
        frame = (frame * 255).astype(np.uint8)
        return frame

    def gaussian_blur(self, frame):
        """
        Reduce image noise.
        """
        return cv2.GaussianBlur(frame, (5, 5), 0)

    def sharpen(self, frame):
        """
        Sharpen image.
        """
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        return cv2.filter2D(frame, -1, kernel)

    def adjust_brightness(self, frame, alpha=1.1, beta=10):
        """
        Increase brightness.
        """
        return cv2.convertScaleAbs(frame,
                                   alpha=alpha,
                                   beta=beta)

    def enhance_contrast(self, frame):
        """
        Improve image contrast using CLAHE.
        """
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))

        return cv2.cvtColor(
            lab,
            cv2.COLOR_LAB2BGR
        )

    def preprocess(self, frame):
        """
        Complete preprocessing pipeline.
        """

        frame = self.resize(frame)

        frame = self.gaussian_blur(frame)

        frame = self.enhance_contrast(frame)

        frame = self.adjust_brightness(frame)

        frame = self.sharpen(frame)

        if self.normalize:
            frame = self.normalize_frame(frame)

        return frame

    def prepare_for_display(self, frame):
        """
        Convert normalized frame back for OpenCV display.
        """

        if frame.dtype != np.uint8:
            frame = self.denormalize(frame)

        return frame
