# Project Report

## Overview
The AI Hand Gesture Recognition and Virtual Control System is a Python-based real-time vision application that uses MediaPipe Hands to track a user's hand, recognize gesture states, and trigger desktop automation actions.

## Components
- HandTracker: wraps MediaPipe Hand solutions and returns landmarks and bounding boxes.
- GestureClassifier: uses rule-based geometry to classify gestures.
- ActionController: maps recognized gestures to OS actions such as media control, cursor movement, screenshots, and launching apps.
- GestureApp: provides a Tkinter-based GUI for live camera feedback and user controls.

## Performance
The system is designed for a target frame rate of 25 FPS and uses simple geometry rules to keep processing lightweight.

## Limitations
- The current classifier is rule-based and may require calibration for different lighting conditions and camera angles.
- OS automation actions vary by platform and may need permission on some systems.

## Future Work
- Add a TensorFlow-based custom classifier trained on a local dataset.
- Improve gesture transitions with temporal filtering.
- Add a virtual drawing and presentation controller mode.
