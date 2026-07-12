"""
main.py
Automatic Fire and Smoke Detection System
"""

import cv2
import time

from config import *

from detection.detector import FireSmokeDetector
from detection.preprocess import FramePreprocessor
from detection.risk_assessment import RiskAssessment

from alerts.telegram_alert import TelegramAlert
from alerts.voice_alert import VoiceAlert
from alerts.sound_alert import SoundAlert

from evidence.logger import EvidenceLogger

from utils.fps import FPSCounter
from utils.helpers import (
    draw_fps,
    draw_risk_level,
    put_system_status
)


class FireSmokeDetectionSystem:

    def __init__(self):

        print("=" * 60)
        print("Automatic Fire and Smoke Detection System")
        print("=" * 60)

        # -------------------------
        # Load Modules
        # -------------------------

        self.detector = FireSmokeDetector()

        self.preprocessor = FramePreprocessor()

        self.risk = RiskAssessment()

        self.telegram = TelegramAlert()

        self.voice = VoiceAlert()

        self.sound = SoundAlert()

        self.logger = EvidenceLogger()

        self.fps_counter = FPSCounter()

        # -------------------------
        # Webcam
        # -------------------------

        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            FRAME_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            FRAME_HEIGHT
        )

        self.cap.set(
            cv2.CAP_PROP_FPS,
            TARGET_FPS
        )

        if not self.cap.isOpened():

            raise Exception("Unable to open webcam.")

        print("Webcam Started.")

        self.running = True

    # ----------------------------------------------------

    def process_frame(self, frame):

        detections = self.detector.detect(frame)

        frame = self.detector.draw_detections(
            frame,
            detections
        )

        frame = self.detector.annotate_statistics(
            frame,
            detections
        )

        risk_level, score = self.risk.calculate(
            detections
        )

        draw_risk_level(
            frame,
            risk_level,
            score
        )

        return frame, detections, risk_level, score

    # ----------------------------------------------------

    def alert_manager(
            self,
            frame,
            detections,
            risk_level,
            score):

        fire_count = self.detector.count_fire(
            detections
        )

        smoke_count = self.detector.count_smoke(
            detections
        )

        if len(detections) == 0:

            self.sound.stop()

            return

        image_path = self.logger.save_image(
            frame,
            risk_level
        )

        self.logger.log_detection(
            risk_level,
            fire_count,
            smoke_count,
            score
        )

        # Telegram

        self.telegram.send_alert(
            risk_level,
            fire_count,
            smoke_count,
            score,
            image_path
        )

        # Voice

        if risk_level == "LOW":

            self.voice.low_alert()

        elif risk_level == "MEDIUM":

            self.voice.medium_alert()

        elif risk_level == "HIGH":

            self.voice.high_alert()

        elif risk_level == "EMERGENCY":

            self.voice.emergency_alert()

        # Alarm Sound

        self.sound.play_risk(
            risk_level
        )
            # ----------------------------------------------------

    def run(self):

        print("System Running...")
        print("Press 'Q' to Exit")

        while self.running:

            ret, frame = self.cap.read()

            if not ret:

                print("Failed to capture frame.")

                break

            frame = cv2.resize(
                frame,
                (FRAME_WIDTH, FRAME_HEIGHT)
            )

            frame, detections, risk_level, score = \
                self.process_frame(frame)

            # -----------------------------
            # Alerts
            # -----------------------------

            self.alert_manager(
                frame,
                detections,
                risk_level,
                score
            )

            # -----------------------------
            # Video Recording
            # -----------------------------

            if risk_level in [

                "HIGH",

                "EMERGENCY"

            ]:

                if not self.logger.recording:

                    self.logger.start_recording(
                        risk_level
                    )

                self.logger.write_frame(
                    frame
                )

            else:

                if self.logger.recording:

                    self.logger.stop_recording()

            # -----------------------------
            # FPS
            # -----------------------------

            fps = self.fps_counter.update()

            draw_fps(
                frame,
                fps
            )

            put_system_status(
                frame,
                "RUNNING"
            )

            cv2.imshow(

                WINDOW_NAME,

                frame

            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                self.running = False

            elif key == ord("s"):

                image = self.logger.save_image(

                    frame,

                    "MANUAL"

                )

                print(

                    "Image Saved:",

                    image

                )

            elif key == ord("r"):

                if self.logger.recording:

                    self.logger.stop_recording()

                else:

                    self.logger.start_recording(

                        "MANUAL"

                    )

            elif key == ord("c"):

                self.risk.reset()

                print(

                    "Risk Reset."

                )

        self.cleanup()
          # ----------------------------------------------------

    def cleanup(self):

        print("Closing System...")

        try:

            self.cap.release()

        except:

            pass

        try:

            self.logger.cleanup()

        except:

            pass

        try:

            self.sound.shutdown()

        except:

            pass

        try:

            self.voice.shutdown()

        except:

            pass

        cv2.destroyAllWindows()

        print("System Closed Successfully.")


# ======================================================

if __name__ == "__main__":

    try:

        system = FireSmokeDetectionSystem()

        system.run()

    except KeyboardInterrupt:

        print("Interrupted by User.")

    except Exception as e:

        print("Error :", e)
