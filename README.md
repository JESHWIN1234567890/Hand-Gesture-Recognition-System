# AI Hand Gesture Recognition and Virtual Control System

This project implements a production-ready hand gesture recognition system using Python, OpenCV, MediaPipe Hands, and PyAutoGUI. It detects hands from a webcam, recognizes common gestures, and triggers desktop actions such as media control, cursor movement, screenshots, browser launching, and system volume control.

## Features

- Real-time hand detection with MediaPipe Hands
- 21-landmark tracking and skeleton drawing
- Gesture recognition for open palm, closed fist, thumbs up/down, peace sign, OK sign, pointing finger, pinch, rock sign, and call me sign
- GUI with start/stop camera controls and status display
- Keyboard shortcuts for screenshot, reset, and quit
- Optional action mapping to desktop automation

## Project Structure

```text
HandGestureRecognition/
├── dataset/
├── models/
├── screenshots/
├── docs/
├── src/
│   ├── main.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│   ├── gesture_classifier.py
│   ├── actions.py
│   ├── utils.py
│   └── config.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/main.py
   ```

## Usage

- Press Start Camera to begin webcam processing.
- Use the on-screen controls to save screenshots and stop the feed.
- Keyboard shortcuts:
  - Q: quit
  - S: save screenshot
  - R: reset gesture state

## Screenshots

Screenshots are saved under the screenshots folder after the Save Screenshot action.

## Future Improvements

- Add a TensorFlow/Keras custom gesture classifier
- Add virtual drawing and air-writing modes
- Improve gesture robustness with temporal smoothing
- Add voice feedback and dark mode themes

## Architecture Overview

```text
Webcam -> HandTracker -> GestureClassifier -> ActionController -> GUI
```

## License

MIT License
