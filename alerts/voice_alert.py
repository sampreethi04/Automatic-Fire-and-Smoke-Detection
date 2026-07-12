"""
voice_alert.py
Voice Alert Module for Automatic Fire and Smoke Detection System
"""

import threading
import pyttsx3


class VoiceAlert:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 170)

        self.engine.setProperty("volume", 1.0)

        self.last_message = ""

        self.speaking = False

    def speak(self, message):

        """
        Speak a message.
        """

        if self.speaking:
            return

        if message == self.last_message:
            return

        self.last_message = message

        thread = threading.Thread(
            target=self._voice_thread,
            args=(message,),
            daemon=True
        )

        thread.start()

    def _voice_thread(self, message):

        self.speaking = True

        try:

            self.engine.say(message)

            self.engine.runAndWait()

        except Exception as e:

            print("Voice Alert Error :", e)

        self.speaking = False

    def fire_alert(self):

        self.speak(
            "Warning. Fire has been detected."
        )

    def smoke_alert(self):

        self.speak(
            "Warning. Smoke has been detected."
        )

    def low_alert(self):

        self.speak(
            "Low Risk. Please monitor the area."
        )

    def medium_alert(self):

        self.speak(
            "Medium Risk. Please be careful."
        )

    def high_alert(self):

        self.speak(
            "High Risk. Immediate attention required."
        )

    def emergency_alert(self):

        self.speak(
            "Emergency. Fire detected. Please evacuate immediately."
        )

    def custom_alert(self, text):

        self.speak(text)

    def stop(self):

        try:

            self.engine.stop()

        except:

            pass

    def shutdown(self):

        self.stop()

        self.last_message = ""

        self.speaking = False
