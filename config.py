"""
config.py
Configuration file for Automatic Fire and Smoke Detection System
"""

import os

# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

# Path to trained YOLO model
MODEL_PATH = "models/best.pt"

# Detection confidence thresholds
FIRE_CONFIDENCE = 0.30
SMOKE_CONFIDENCE = 0.15

# ==========================================================
# CAMERA SETTINGS
# ==========================================================

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

TARGET_FPS = 30

# ==========================================================
# TELEGRAM SETTINGS
# ==========================================================

BOT_TOKEN = "YOUR_BOT_TOKEN"

CHAT_ID = "YOUR_CHAT_ID"

# ==========================================================
# ALERT SETTINGS
# ==========================================================

ALERT_COOLDOWN = 30

VOICE_COOLDOWN = 10

ENABLE_TELEGRAM = True
ENABLE_SOUND = True
ENABLE_VOICE = True

# ==========================================================
# EVIDENCE SETTINGS
# ==========================================================

IMAGE_FOLDER = "evidence/images"
VIDEO_FOLDER = "evidence/videos"
LOG_FOLDER = "evidence/logs"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# ==========================================================
# AUDIO FILES
# ==========================================================

LOW_SOUND = "assets/low.wav"
MEDIUM_SOUND = "assets/medium.wav"
HIGH_SOUND = "assets/high.wav"
EMERGENCY_SOUND = "assets/emergency.wav"

# ==========================================================
# COLORS (BGR FORMAT)
# ==========================================================

GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RISK_COLORS = {
    "NO RISK": GREEN,
    "LOW": YELLOW,
    "MEDIUM": ORANGE,
    "HIGH": RED,
    "EMERGENCY": RED
}

# ==========================================================
# FONT SETTINGS
# ==========================================================

FONT_SCALE = 0.7
FONT_THICKNESS = 2

# ==========================================================
# WINDOW SETTINGS
# ==========================================================

WINDOW_NAME = "Automatic Fire and Smoke Detection"

# ==========================================================
# VIDEO RECORDING
# ==========================================================

VIDEO_CODEC = "XVID"

VIDEO_EXTENSION = ".avi"

SAVE_DETECTION_IMAGES = True
SAVE_DETECTION_VIDEO = True

# ==========================================================
# LOGGING
# ==========================================================

LOG_FILE = os.path.join(LOG_FOLDER, "detections.log")

# ==========================================================
# RISK SCORE SETTINGS
# ==========================================================

LOW_THRESHOLD = 0.5
MEDIUM_THRESHOLD = 1.0
HIGH_THRESHOLD = 1.5
EMERGENCY_THRESHOLD = 2.0

# ==========================================================
# DISPLAY OPTIONS
# ==========================================================

SHOW_FPS = True
SHOW_CONFIDENCE = True
SHOW_RISK_LEVEL = True
SHOW_BOUNDING_BOX = True

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

PROJECT_NAME = "Automatic Fire and Smoke Detection"

VERSION = "1.0"

AUTHOR = "Sampreethi Kookutla"
