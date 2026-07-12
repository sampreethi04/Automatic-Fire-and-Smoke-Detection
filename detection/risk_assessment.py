"""
risk_assessment.py
Risk Assessment Module for Automatic Fire and Smoke Detection System
"""

from config import (
    LOW_THRESHOLD,
    MEDIUM_THRESHOLD,
    HIGH_THRESHOLD,
    EMERGENCY_THRESHOLD
)


class RiskAssessment:

    def __init__(self):

        self.risk_level = "NO RISK"
        self.risk_score = 0.0

    def calculate(self, detections):

        """
        detections = [
            {
                "class":"fire",
                "confidence":0.91,
                "box":[x1,y1,x2,y2]
            }
        ]
        """

        if len(detections) == 0:

            self.risk_level = "NO RISK"
            self.risk_score = 0

            return self.risk_level, self.risk_score

        fire_count = 0
        smoke_count = 0

        fire_conf = 0
        smoke_conf = 0

        for detection in detections:

            label = detection["class"]

            confidence = detection["confidence"]

            if label.lower() == "fire":

                fire_count += 1
                fire_conf += confidence

            elif label.lower() == "smoke":

                smoke_count += 1
                smoke_conf += confidence

        total_confidence = fire_conf + smoke_conf

        score = (
            fire_count * 0.6 +
            smoke_count * 0.3 +
            total_confidence
        )

        self.risk_score = round(score, 2)

        if score >= EMERGENCY_THRESHOLD:

            self.risk_level = "EMERGENCY"

        elif score >= HIGH_THRESHOLD:

            self.risk_level = "HIGH"

        elif score >= MEDIUM_THRESHOLD:

            self.risk_level = "MEDIUM"

        elif score >= LOW_THRESHOLD:

            self.risk_level = "LOW"

        else:

            self.risk_level = "NO RISK"

        return self.risk_level, self.risk_score

    def get_color(self):

        colors = {

            "NO RISK": (0,255,0),

            "LOW": (0,255,255),

            "MEDIUM": (0,165,255),

            "HIGH": (0,0,255),

            "EMERGENCY": (0,0,180)

        }

        return colors[self.risk_level]

    def reset(self):

        self.risk_level = "NO RISK"
        self.risk_score = 0

    def summary(self):

        return {

            "Risk Level": self.risk_level,

            "Risk Score": self.risk_score

        }
