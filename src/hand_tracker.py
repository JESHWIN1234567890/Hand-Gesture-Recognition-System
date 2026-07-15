"""MediaPipe-based hand tracking and frame annotation."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np
import mediapipe as mp

try:
    from config import (
        DRAW_BOUNDING_BOX,
        DRAW_LANDMARKS,
        MAX_HANDS,
        MIN_DETECTION_CONFIDENCE,
        MIN_TRACKING_CONFIDENCE,
    )
except ImportError:
    from src.config import (
        DRAW_BOUNDING_BOX,
        DRAW_LANDMARKS,
        MAX_HANDS,
        MIN_DETECTION_CONFIDENCE,
        MIN_TRACKING_CONFIDENCE,
    )


class HandTracker:
    """MediaPipe Hands wrapper."""

    def __init__(self) -> None:
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_style = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

    def process_frame(self, frame: np.ndarray) -> dict[str, Any]:
        """Detect hands and return annotated frame."""
        height, width, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        annotated = frame.copy()
        hand_results = []

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                landmarks = []

                xs = []
                ys = []

                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x, lm.y, lm.z))
                    xs.append(lm.x)
                    ys.append(lm.y)

                bbox = {
                    "x_min": int(min(xs) * width),
                    "y_min": int(min(ys) * height),
                    "x_max": int(max(xs) * width),
                    "y_max": int(max(ys) * height),
                    "width": int((max(xs) - min(xs)) * width),
                    "height": int((max(ys) - min(ys)) * height),
                }

                handedness = "Unknown"

                if results.multi_handedness:
                    handedness = (
                        results.multi_handedness[idx]
                        .classification[0]
                        .label
                    )

                if DRAW_LANDMARKS:
                    self.mp_draw.draw_landmarks(
                        annotated,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_style.get_default_hand_landmarks_style(),
                        self.mp_style.get_default_hand_connections_style(),
                    )

                if DRAW_BOUNDING_BOX:
                    cv2.rectangle(
                        annotated,
                        (bbox["x_min"], bbox["y_min"]),
                        (bbox["x_max"], bbox["y_max"]),
                        (0, 255, 0),
                        2,
                    )

                hand_results.append(
                    {
                        "landmarks": landmarks,
                        "bbox": bbox,
                        "handedness": handedness,
                    }
                )

        return {
            "frame": annotated,
            "hands": hand_results,
            "hand_count": len(hand_results),
        }

    def close(self):
        self.hands.close()