"""Utility helpers for logging, image handling, and math operations."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Iterable, Sequence, Tuple

import cv2
import numpy as np

try:
    from config import SCREENSHOTS_DIR
except ImportError:  # pragma: no cover - fallback for script execution
    from src.config import SCREENSHOTS_DIR


def setup_logging(name: str = "gesture_app", level: int = logging.INFO) -> logging.Logger:
    """Create and return a configured logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def ensure_directories() -> None:
    """Create the directories used by the application if they do not exist."""
    for directory in (SCREENSHOTS_DIR,):
        directory.mkdir(parents=True, exist_ok=True)


def euclidean_distance(point_a: Sequence[float], point_b: Sequence[float]) -> float:
    """Compute the Euclidean distance between two points."""
    return float(np.linalg.norm(np.array(point_a) - np.array(point_b)))


def normalize_landmarks(landmarks: Iterable[Sequence[float]]) -> list[tuple[float, float, float]]:
    """Convert landmark objects into plain tuples."""
    return [(float(lm[0]), float(lm[1]), float(lm[2])) for lm in landmarks]


def save_frame(frame: np.ndarray, prefix: str = "screenshot") -> Path:
    """Save a BGR image to the screenshots directory."""
    ensure_directories()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOTS_DIR / f"{prefix}_{timestamp}.png"
    cv2.imwrite(str(path), frame)
    return path


def release_capture(capture: cv2.VideoCapture) -> None:
    """Release OpenCV capture safely."""
    if capture is not None:
        capture.release()
