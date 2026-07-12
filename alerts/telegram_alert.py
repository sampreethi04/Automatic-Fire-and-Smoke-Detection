"""
telegram_alert.py
Telegram Alert Module for Automatic Fire and Smoke Detection System
"""

import os
import time
import requests

from config import (
    BOT_TOKEN,
    CHAT_ID,
    ALERT_COOLDOWN
)


class TelegramAlert:

    def __init__(self):

        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID

        self.last_alert_time = 0

        self.base_url = (
            f"https://api.telegram.org/bot{self.bot_token}"
        )

    def cooldown_over(self):

        current = time.time()

        if current - self.last_alert_time >= ALERT_COOLDOWN:

            self.last_alert_time = current
            return True

        return False

    def send_message(self,
                     risk_level,
                     fire_count,
                     smoke_count,
                     score):

        if not self.cooldown_over():
            return False

        message = f"""
🚨 FIRE & SMOKE DETECTION ALERT 🚨

Risk Level : {risk_level}

Fire Detected : {fire_count}

Smoke Detected : {smoke_count}

Risk Score : {score}

Time : {time.strftime("%Y-%m-%d %H:%M:%S")}

Automatic Fire and Smoke Detection System
"""

        url = f"{self.base_url}/sendMessage"

        data = {

            "chat_id": self.chat_id,

            "text": message

        }

        try:

            response = requests.post(
                url,
                data=data,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:

            print("Telegram Error:", e)

            return False

    def send_photo(self,
                   image_path,
                   caption="Fire Detected"):

        if not os.path.exists(image_path):
            return False

        url = f"{self.base_url}/sendPhoto"

        try:

            with open(image_path, "rb") as photo:

                files = {

                    "photo": photo

                }

                data = {

                    "chat_id": self.chat_id,

                    "caption": caption

                }

                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    timeout=20
                )

            return response.status_code == 200

        except Exception as e:

            print("Telegram Image Error:", e)

            return False

    def send_alert(self,
                   risk_level,
                   fire_count,
                   smoke_count,
                   score,
                   image_path=None):

        success = self.send_message(
            risk_level,
            fire_count,
            smoke_count,
            score
        )

        if image_path is not None:

            self.send_photo(
                image_path,
                caption=f"{risk_level} Alert"
            )

        return success

    def test_connection(self):

        url = f"{self.base_url}/getMe"

        try:

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code == 200:

                print("Telegram Bot Connected")

                return True

            print("Telegram Connection Failed")

            return False

        except Exception as e:

            print(e)

            return False
