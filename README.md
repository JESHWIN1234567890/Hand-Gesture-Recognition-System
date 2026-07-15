# ✋ AI Hand Gesture Recognition and Virtual Control System

A real-time **Hand Gesture Recognition System** built using **Python**, **OpenCV**, **MediaPipe**, and **PyAutoGUI**. The application detects hand landmarks from a webcam, recognizes predefined gestures, and performs desktop automation tasks such as taking screenshots and controlling system functions.

---

## 🚀 Features

- Real-time hand detection using MediaPipe Hands
- 21-point hand landmark tracking
- Gesture recognition using finger positions
- Desktop automation with PyAutoGUI
- Screenshot capture using the Peace (✌️) gesture
- Graphical User Interface (GUI) for camera control
- Keyboard shortcuts for quick operations
- Modular and easy-to-extend project structure

---

## 🛠️ Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- Tkinter

---

## 📂 Project Structure

```text
Hand-Gesture-Recognition-System/
│
├── dataset/
├── docs/
├── models/
├── screenshots/
├── src/
│   ├── main.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│   ├── gesture_classifier.py
│   ├── actions.py
│   ├── config.py
│   └── utils.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/JESHWIN1234567890/Hand-Gesture-Recognition-System.git
```

### Navigate to the project

```bash
cd Hand-Gesture-Recognition-System
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python src/main.py
```

---

## ✋ Supported Gestures

| Gesture | Action |
|----------|--------|
| ✌️ Peace | Capture Screenshot |
| 🖐 Open Palm | Detect Hand |
| ✊ Fist | Customizable |
| 👍 Thumbs Up | Customizable |
| 👌 OK | Customizable |

> Additional gestures can be added by extending the gesture recognition logic.

---

## 📷 Screenshots 

Screenshots are saved under the screenshots folder after the save screenshot action.

---

## 🧠 How It Works

```text
Webcam
   │
   ▼
MediaPipe Hand Detection
   │
   ▼
21 Hand Landmarks
   │
   ▼
Gesture Recognition
   │
   ▼
Action Controller
   │
   ▼
Desktop Automation
```

---

## ⌨️ Keyboard Shortcuts

| Key | Function |
|-----|----------|
| **S** | Save Screenshot |
| **R** | Reset Gesture State |
| **Q** | Quit Application |

---

## 🎯 Applications

- Human-Computer Interaction (HCI)
- Touchless Computer Control
- Smart Home Interfaces
- Accessibility Systems
- Gesture-based Automation
- Computer Vision Learning

---

## 🚀 Future Improvements

- Machine Learning–based gesture classification
- Virtual mouse control
- Virtual keyboard
- Air drawing and whiteboard
- Sign language recognition
- Multi-hand gesture support
- Voice feedback
- Gesture customization through the GUI

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Jeshwin V S**

B.Tech Computer Science and Engineering (Artificial Intelligence & Machine Learning)

Rajadhani Institute of Engineering and Technology

---

⭐ **If you found this project useful, consider giving it a star on GitHub!**
