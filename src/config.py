"""Configuration values for the hand gesture recognition application."""

from __future__ import annotations

from pathlib import Path
import logging

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "dataset"
MODELS_DIR = ROOT_DIR / "models"
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
DOCS_DIR = ROOT_DIR / "docs"
SRC_DIR = ROOT_DIR / "src"

CAMERA_INDEX = 0
WINDOW_NAME = "AI Hand Gesture Recognition"
TARGET_FPS = 25
MAX_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.5
SMOOTHING_ALPHA = 0.15
DRAW_LANDMARKS = True
DRAW_BOUNDING_BOX = True

DEFAULT_LOG_LEVEL = logging.INFO

# Gesture thresholds
PINCH_DISTANCE_THRESHOLD = 0.08
OK_DISTANCE_THRESHOLD = 0.08
OPEN_PALM_THRESHOLD = 0.25

# GUI settings
GUI_TITLE = "AI Hand Gesture Recognition and Virtual Control System"
GUI_WIDTH = 1100
GUI_HEIGHT = 750
