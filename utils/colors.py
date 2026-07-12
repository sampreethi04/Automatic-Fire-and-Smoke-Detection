"""
colors.py
Color definitions for Automatic Fire and Smoke Detection System
OpenCV uses BGR color format.
"""

# Basic Colors (BGR)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)

CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)

GRAY = (128, 128, 128)

# --------------------------------------
# Bounding Box Colors
# --------------------------------------

FIRE_BOX = RED
SMOKE_BOX = BLUE

# --------------------------------------
# Risk Level Colors
# --------------------------------------

RISK_COLORS = {

    "NO RISK": GREEN,

    "LOW": YELLOW,

    "MEDIUM": ORANGE,

    "HIGH": RED,

    "EMERGENCY": (0, 0, 180)

}

# --------------------------------------
# Text Colors
# --------------------------------------

TEXT_COLOR = WHITE
BACKGROUND_COLOR = BLACK

# --------------------------------------
# UI Colors
# --------------------------------------

FPS_COLOR = CYAN
CONFIDENCE_COLOR = WHITE
WARNING_COLOR = RED

# --------------------------------------
# Alert Colors
# --------------------------------------

ALERT_GREEN = (0, 255, 0)
ALERT_YELLOW = (0, 255, 255)
ALERT_ORANGE = (0, 165, 255)
ALERT_RED = (0, 0, 255)

# --------------------------------------
# Detection Colors
# --------------------------------------

CLASS_COLORS = {

    "fire": FIRE_BOX,

    "smoke": SMOKE_BOX

}
