"""
detector.py
Fire and Smoke Detection using YOLOv8
"""

import cv2
from ultralytics import YOLO

from config import (
    MODEL_PATH,
    FIRE_CONFIDENCE,
    SMOKE_CONFIDENCE
)

from utils.colors import CLASS_COLORS


class FireSmokeDetector:

    def __init__(self):

        print("Loading YOLO Model...")

        self.model = YOLO(MODEL_PATH)

        print("Model Loaded Successfully!")

        self.class_names = self.model.names

    def detect(self, frame):

        """
        Perform detection on frame

        Returns:
            detections (list)
        """

        detections = []

        results = self.model.predict(
            source=frame,
            conf=min(FIRE_CONFIDENCE, SMOKE_CONFIDENCE),
            verbose=False
        )

        for result in results:

            boxes = result.boxes

            if boxes is None:
                continue

            for box in boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                label = self.class_names[class_id].lower()

                # Apply confidence thresholds

                if label == "fire":

                    if confidence < FIRE_CONFIDENCE:
                        continue

                elif label == "smoke":

                    if confidence < SMOKE_CONFIDENCE:
                        continue

                else:
                    continue

                detections.append({

                    "class": label,

                    "confidence": confidence,

                    "box": [x1, y1, x2, y2]

                })

        return detections

    def draw_detections(self,
                        frame,
                        detections):

        """
        Draw bounding boxes
        """

        for detection in detections:

            x1, y1, x2, y2 = detection["box"]

            label = detection["class"]

            confidence = detection["confidence"]

            color = CLASS_COLORS.get(
                label,
                (0,255,0)
            )

            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                color,
                2
            )

            text = f"{label.upper()} {confidence:.2f}"

            (w,h),_ = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            cv2.rectangle(
                frame,
                (x1,y1-30),
                (x1+w+10,y1),
                color,
                -1
            )

            cv2.putText(
                frame,
                text,
                (x1+5,y1-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2
            )

        return frame

    def count_fire(self, detections):
        """
        Count fire detections.
        """
        return sum(
            1 for d in detections
            if d["class"] == "fire"
        )

    def count_smoke(self, detections):
        """
        Count smoke detections.
        """
        return sum(
            1 for d in detections
            if d["class"] == "smoke"
        )

    def largest_detection(self, detections):
        """
        Return the largest detected object based on
        bounding box area.
        """

        if len(detections) == 0:
            return None

        largest = None
        max_area = 0

        for detection in detections:

            x1, y1, x2, y2 = detection["box"]

            area = (x2 - x1) * (y2 - y1)

            if area > max_area:

                max_area = area
                largest = detection

        return largest

    def average_confidence(self, detections):
        """
        Average confidence of all detections.
        """

        if len(detections) == 0:
            return 0.0

        total = sum(
            d["confidence"]
            for d in detections
        )

        return round(
            total / len(detections),
            2
        )

    def annotate_statistics(
            self,
            frame,
            detections):

        """
        Display detection statistics.
        """

        fire_count = self.count_fire(detections)

        smoke_count = self.count_smoke(detections)

        avg_conf = self.average_confidence(detections)

        cv2.putText(
            frame,
            f"Fire : {fire_count}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Smoke : {smoke_count}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Average Confidence : {avg_conf:.2f}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return frame

    def process(self, frame):
        """
        Complete detection pipeline.
        """

        detections = self.detect(frame)

        frame = self.draw_detections(
            frame,
            detections
        )

        frame = self.annotate_statistics(
            frame,
            detections
        )

        return frame, detections

    def get_model_info(self):
        """
        Return model information.
        """

        return {
            "Model Path": MODEL_PATH,
            "Fire Threshold": FIRE_CONFIDENCE,
            "Smoke Threshold": SMOKE_CONFIDENCE,
            "Classes": self.class_names
        }
