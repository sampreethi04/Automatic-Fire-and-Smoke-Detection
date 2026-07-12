"""
sound_alert.py
Alarm Sound Module for Automatic Fire and Smoke Detection System
"""

import pygame
import os

from config import (
    LOW_SOUND,
    MEDIUM_SOUND,
    HIGH_SOUND,
    EMERGENCY_SOUND
)


class SoundAlert:

    def __init__(self):

        pygame.mixer.init()

        self.current_sound = None

    def play(self, sound_file):

        """
        Play a sound if it exists.
        """

        try:

            if not os.path.exists(sound_file):

                print(f"Sound file not found : {sound_file}")

                return

            if self.current_sound == sound_file:

                if pygame.mixer.music.get_busy():
                    return

            pygame.mixer.music.stop()

            pygame.mixer.music.load(sound_file)

            pygame.mixer.music.play()

            self.current_sound = sound_file

        except Exception as e:

            print("Sound Error :", e)

    def stop(self):

        try:

            pygame.mixer.music.stop()

            self.current_sound = None

        except:

            pass

    def low(self):

        self.play(LOW_SOUND)

    def medium(self):

        self.play(MEDIUM_SOUND)

    def high(self):

        self.play(HIGH_SOUND)

    def emergency(self):

        self.play(EMERGENCY_SOUND)

    def play_risk(self, risk_level):

        """
        Play sound based on calculated risk.
        """

        risk_level = risk_level.upper()

        if risk_level == "LOW":

            self.low()

        elif risk_level == "MEDIUM":

            self.medium()

        elif risk_level == "HIGH":

            self.high()

        elif risk_level == "EMERGENCY":

            self.emergency()

        else:

            self.stop()

    def shutdown(self):

        self.stop()

        pygame.mixer.quit()
