from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gesture_classifier import GestureClassifier


def test_classify_open_palm() -> None:
    classifier = GestureClassifier()
    landmarks = [(0.2, 0.2, 0.0)] * 21
    # Simulate an open hand by making finger tips above their base points.
    landmarks[4] = (0.25, 0.10, 0.0)
    landmarks[8] = (0.20, 0.10, 0.0)
    landmarks[12] = (0.20, 0.10, 0.0)
    landmarks[16] = (0.20, 0.10, 0.0)
    landmarks[20] = (0.20, 0.10, 0.0)
    landmarks[3] = (0.20, 0.20, 0.0)
    landmarks[6] = (0.20, 0.20, 0.0)
    landmarks[10] = (0.20, 0.20, 0.0)
    landmarks[14] = (0.20, 0.20, 0.0)
    landmarks[18] = (0.20, 0.20, 0.0)

    result = classifier.classify(landmarks, handedness="Right")

    assert result.name == "Open Palm"
