"""Rule-based gesture classification using hand landmarks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

try:
    from utils import euclidean_distance
except ImportError:  # pragma: no cover - fallback for script execution
    from src.utils import euclidean_distance


@dataclass
class GestureResult:
    """Structured result for a recognized gesture."""

    name: str
    confidence: float
    finger_states: dict[str, str]
    bbox: dict[str, Any] | None = None


class GestureClassifier:
    """Recognize gestures using landmark geometry and finger state rules."""

    def __init__(self) -> None:
        self._finger_indices = {
            "thumb": [4, 3, 2],
            "index": [8, 6, 5],
            "middle": [12, 10, 9],
            "ring": [16, 14, 13],
            "pinky": [20, 18, 17],
        }

    def classify(self, landmarks: list[tuple[float, float, float]], handedness: str = "Right", bbox: dict[str, Any] | None = None) -> GestureResult:
        """Classify the hand into a known gesture or return 'Unknown'."""
        if len(landmarks) < 21:
            return GestureResult("Unknown", 0.0, {name: "unknown" for name in self._finger_indices})

        finger_states = self._compute_finger_states(landmarks, handedness)
        thumb_extended = finger_states["thumb"] == "open"
        index_open = finger_states["index"] == "open"
        middle_open = finger_states["middle"] == "open"
        ring_open = finger_states["ring"] == "open"
        pinky_open = finger_states["pinky"] == "open"

        thumb_tip = np.array(landmarks[4])
        index_tip = np.array(landmarks[8])
        thumb_index_distance = euclidean_distance(thumb_tip, index_tip)

        all_closed = not any([thumb_extended, index_open, middle_open, ring_open, pinky_open])
        all_open = thumb_extended and index_open and middle_open and ring_open and pinky_open

        if all_closed:
            if thumb_index_distance < 0.08:
                return GestureResult("OK Sign", 0.92, finger_states, bbox)
            return GestureResult("Closed Fist", 0.93, finger_states, bbox)

        if all_open:
            return GestureResult("Open Palm", 0.95, finger_states, bbox)

        if thumb_extended and not index_open and not middle_open and not ring_open and not pinky_open:
            if landmarks[4][1] < landmarks[2][1] - 0.03:
                return GestureResult("Thumbs Up", 0.91, finger_states, bbox)
            if landmarks[4][1] > landmarks[2][1] + 0.03:
                return GestureResult("Thumbs Down", 0.91, finger_states, bbox)

        if index_open and middle_open and not ring_open and not pinky_open:
            return GestureResult("Peace Sign", 0.93, finger_states, bbox)

        if index_open and not middle_open and not ring_open and not pinky_open:
            return GestureResult("Pointing Finger", 0.92, finger_states, bbox)

        if thumb_index_distance < 0.08 and not middle_open and not ring_open and not pinky_open:
            return GestureResult("Pinch", 0.89, finger_states, bbox)

        if index_open and pinky_open and not middle_open and not ring_open:
            return GestureResult("Rock Sign", 0.88, finger_states, bbox)

        if thumb_extended and index_open and pinky_open and not middle_open and not ring_open:
            return GestureResult("Call Me Sign", 0.86, finger_states, bbox)

        return GestureResult("Unknown", 0.55, finger_states, bbox)

    def _compute_finger_states(self, landmarks: list[tuple[float, float, float]], handedness: str) -> dict[str, str]:
        """Return open/closed state for each finger."""
        states: dict[str, str] = {}
        for name, indices in self._finger_indices.items():
            if name == "thumb":
                states[name] = self._thumb_state(landmarks, handedness)
            else:
                states[name] = self._finger_state(landmarks, indices[0], indices[1])
        return states

    def _thumb_state(self, landmarks: list[tuple[float, float, float]], handedness: str) -> str:
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        horizontal_delta = abs(thumb_tip[0] - thumb_ip[0])
        vertical_delta = abs(thumb_tip[1] - thumb_ip[1])
        if handedness.lower() == "right":
            return "open" if horizontal_delta > 0.03 or vertical_delta > 0.03 else "closed"
        return "open" if horizontal_delta > 0.03 or vertical_delta > 0.03 else "closed"

    def _finger_state(self, landmarks: list[tuple[float, float, float]], tip_idx: int, pip_idx: int) -> str:
        tip = np.array(landmarks[tip_idx])
        pip = np.array(landmarks[pip_idx])
        return "open" if tip[1] < pip[1] - 0.03 else "closed"
