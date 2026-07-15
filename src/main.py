"""Main application entry point for the gesture recognition system."""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

try:
    from config import CAMERA_INDEX, GUI_HEIGHT, GUI_TITLE, GUI_WIDTH, TARGET_FPS, WINDOW_NAME
    from hand_tracker import HandTracker
    from gesture_classifier import GestureClassifier
    from actions import ActionController
    from utils import release_capture, save_frame, setup_logging
except ImportError:  # pragma: no cover - fallback for script execution
    from src.config import CAMERA_INDEX, GUI_HEIGHT, GUI_TITLE, GUI_WIDTH, TARGET_FPS, WINDOW_NAME
    from src.hand_tracker import HandTracker
    from src.gesture_classifier import GestureClassifier
    from src.actions import ActionController
    from src.utils import release_capture, save_frame, setup_logging


class GestureApp:
    """Tkinter GUI application for camera feed and gesture controls."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(GUI_TITLE)
        self.root.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}")
        self.root.minsize(1080, 720)
        self.root.configure(bg="#07111f")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.logger = setup_logging("gesture_app", logging.INFO)
        self.tracker = HandTracker()
        self.classifier = GestureClassifier()
        self.controller = ActionController()
        self.capture = cv2.VideoCapture(CAMERA_INDEX)
        self.running = False
        self.lock = threading.Lock()
        self.current_gesture = "Waiting"
        self.current_fps = 0.0
        self.last_action = "None"
        self.last_frame: Optional[np.ndarray] = None

        # Create Tkinter variables BEFORE building the UI
        self.status_text = tk.StringVar(value="Status: Idle")
        self.gesture_var = tk.StringVar(value="Waiting")
        self.fps_var = tk.StringVar(value="0.0")
        self.confidence_var = tk.StringVar(value="0.00")
        self.finger_var = tk.StringVar(value="-")
        self.action_var = tk.StringVar(value="None")
        self.placeholder_var = tk.StringVar(value="Camera inactive\nPress Start Camera")

        self._build_ui()

    def _build_ui(self) -> None:
        self._apply_theme()

        self.main_frame = ttk.Frame(self.root, padding=16)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(header, text="AI Hand Gesture Recognition", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(header, text="Real-time hand tracking, gesture recognition, and virtual control", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(2, 0))

        content = ttk.Frame(self.main_frame)
        content.pack(fill=tk.BOTH, expand=True)

        video_panel = ttk.LabelFrame(content, text="Camera Feed", padding=10, style="Card.TLabelframe")
        video_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        video_panel.configure(padding=10)

        self.video_label = ttk.Label(video_panel, textvariable=self.placeholder_var, anchor="center", padding=20, style="Video.TLabel")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        side_panel = ttk.Frame(content, padding=(0, 0, 0, 0))
        side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))

        status_panel = ttk.LabelFrame(side_panel, text="Live Status", padding=12, style="Card.TLabelframe")
        status_panel.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(status_panel, textvariable=self.status_text, style="Value.TLabel").pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(status_panel, text="Gesture", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(status_panel, textvariable=self.gesture_var, style="Value.TLabel").pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(status_panel, text="FPS", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(status_panel, textvariable=self.fps_var, style="Value.TLabel").pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(status_panel, text="Confidence", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(status_panel, textvariable=self.confidence_var, style="Value.TLabel").pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(status_panel, text="Fingers", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(status_panel, textvariable=self.finger_var, style="Value.TLabel").pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(status_panel, text="Action", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(status_panel, textvariable=self.action_var, style="Value.TLabel").pack(anchor=tk.W)

        controls = ttk.Frame(side_panel)
        controls.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(controls, text="Start Camera", command=self.start_camera, style="Primary.TButton").pack(fill=tk.X, pady=3)
        ttk.Button(controls, text="Stop Camera", command=self.stop_camera, style="Secondary.TButton").pack(fill=tk.X, pady=3)
        ttk.Button(controls, text="Save Screenshot", command=self.save_screenshot, style="Secondary.TButton").pack(fill=tk.X, pady=3)
        ttk.Button(controls, text="Exit", command=self.on_close, style="Danger.TButton").pack(fill=tk.X, pady=3)

        help_panel = ttk.LabelFrame(side_panel, text="Keyboard Shortcuts", padding=10, style="Card.TLabelframe")
        help_panel.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(help_panel, text="Q - Quit", style="Info.TLabel").pack(anchor=tk.W)
        ttk.Label(help_panel, text="S - Screenshot", style="Info.TLabel").pack(anchor=tk.W)
        ttk.Label(help_panel, text="R - Reset", style="Info.TLabel").pack(anchor=tk.W)

        self.root.bind("q", lambda event: self.on_close())
        self.root.bind("s", lambda event: self.save_screenshot())
        self.root.bind("r", lambda event: self.reset_state())

    def _apply_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#07111f")
        style.configure("Card.TLabelframe", background="#111827", bordercolor="#263449")
        style.configure("Card.TLabelframe.Label", background="#111827", foreground="#e2e8f0", font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", background="#07111f", foreground="#f8fafc", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#07111f", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#111827", foreground="#94a3b8", font=("Segoe UI", 9))
        style.configure("Value.TLabel", background="#111827", foreground="#f8fafc", font=("Segoe UI", 11, "bold"))
        style.configure("Info.TLabel", background="#111827", foreground="#cbd5e1", font=("Segoe UI", 9))
        style.configure("Video.TLabel", background="#020617", foreground="#f8fafc", font=("Segoe UI", 11, "bold"))
        style.configure("Primary.TButton", background="#2563eb", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Secondary.TButton", background="#1f2937", foreground="#f8fafc", font=("Segoe UI", 10), padding=8)
        style.configure("Danger.TButton", background="#dc2626", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Primary.TButton", background=[("active", "#3b82f6"), ("!disabled", "#2563eb")])
        style.map("Secondary.TButton", background=[("active", "#334155"), ("!disabled", "#1f2937")])
        style.map("Danger.TButton", background=[("active", "#ef4444"), ("!disabled", "#dc2626")])

    def start_camera(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop_camera(self) -> None:
        self.running = False

    def save_screenshot(self) -> None:
        if self.last_frame is not None:
            save_frame(self.last_frame, prefix="gui")
            self.status_text.set("Status: Screenshot saved")
            self.action_var.set("Screenshot")

    def reset_state(self) -> None:
        self.current_gesture = "Waiting"
        self.last_action = "None"
        self.gesture_var.set("Waiting")
        self.confidence_var.set("0.00")
        self.finger_var.set("-")
        self.action_var.set("None")
        self.status_text.set("Status: Reset")

    def _capture_loop(self) -> None:
        prev_time = time.time()
        while self.running:
            success, frame = self.capture.read()
            if not success or frame is None:
                self.logger.warning("Unable to read frame from camera")
                self.running = False
                break

            frame = cv2.flip(frame, 1)
            results = self.tracker.process_frame(frame)
            annotated = results["frame"]
            self.last_frame = annotated

            if results["hands"]:
                hand = results["hands"][0]
                gesture = self.classifier.classify(hand["landmarks"], hand["handedness"], hand["bbox"])
                self.current_gesture = gesture.name
                self.gesture_var.set(gesture.name)
                self.confidence_var.set(f"{gesture.confidence:.2f}")
                self.finger_var.set(str(gesture.finger_states))
                self.controller.handle(gesture.name, annotated, hand["bbox"])
                self.last_action = gesture.name
                self.action_var.set(gesture.name)
                self.status_text.set(f"Status: {gesture.name}")
                self._draw_text(annotated, f"Gesture: {gesture.name}", 10, 30)
                self._draw_text(annotated, f"Confidence: {gesture.confidence:.2f}", 10, 60)
                self._draw_text(annotated, f"Fingers: {gesture.finger_states}", 10, 90)
            else:
                self._draw_text(annotated, "Gesture: Waiting", 10, 30)
                self.action_var.set("None")
                self.status_text.set("Status: Waiting for hand")

            current_time = time.time()
            fps = 1 / max(current_time - prev_time, 1e-6)
            prev_time = current_time
            self.current_fps = fps
            self.fps_var.set(f"{fps:.1f}")
            self._draw_text(annotated, f"FPS: {fps:.1f}", 10, 120)

            cv2image = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            img = np.asarray(cv2image)
            img = cv2.resize(img, (900, 600))
            self._show_image(img)

            time.sleep(1 / TARGET_FPS)

        self.status_text.set("Status: Camera stopped")

    def _show_image(self, image: np.ndarray) -> None:
        photo = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
        img = cv2.resize(photo, (900, 560))
        img = np.array(img)
        img = img.reshape((img.shape[0], img.shape[1], 4))
        image_tk = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        self._update_image(image_tk)

    def _update_image(self, image: np.ndarray) -> None:
        if not hasattr(self, "photo"):
            self.photo = tk.PhotoImage(data="")
        import PIL.Image as Image
        import PIL.ImageTk as ImageTk
        pil_image = Image.fromarray(image)
        self.photo = ImageTk.PhotoImage(image=pil_image)
        self.video_label.configure(image=self.photo)
        self.video_label.image = self.photo

    def _draw_text(self, frame: np.ndarray, text: str, x: int, y: int) -> None:
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    def on_close(self) -> None:
        self.running = False
        if self.capture is not None:
            release_capture(self.capture)
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
