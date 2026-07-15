"""Computer actions triggered by recognized gestures."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from typing import Any

import pyautogui

try:
    from utils import save_frame
except ImportError:  # pragma: no cover - fallback for script execution
    from src.utils import save_frame


class ActionController:
    """Map gestures to OS-level actions."""

    def __init__(self) -> None:
        pyautogui.FAILSAFE = True
        self.last_click_time = 0.0
        self.dragging = False
        self.last_cursor = (0, 0)

    def handle(self, gesture_name: str, frame: Any, bbox: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute an action for a gesture and return status information."""
        result = {"action": "none", "message": "No action"}
        if gesture_name == "Open Palm":
            result = {"action": "pause", "message": "Detection paused"}
        elif gesture_name == "Closed Fist":
            self._toggle_media()
            result = {"action": "media", "message": "Media toggled"}
        elif gesture_name == "Pointing Finger":
            self._move_cursor(bbox)
            result = {"action": "cursor", "message": "Cursor moved"}
        elif gesture_name == "Pinch":
            self._left_click()
            result = {"action": "click", "message": "Left click"}
        elif gesture_name == "Thumbs Up":
            self._volume_up()
            result = {"action": "volume_up", "message": "Volume up"}
        elif gesture_name == "Thumbs Down":
            self._volume_down()
            result = {"action": "volume_down", "message": "Volume down"}
        elif gesture_name == "Peace Sign":
            self._screenshot(frame)
            result = {"action": "screenshot", "message": "Screenshot saved"}
        elif gesture_name == "OK Sign":
            self._open_calculator()
            result = {"action": "calculator", "message": "Calculator opened"}
        elif gesture_name == "Rock Sign":
            self._open_browser()
            result = {"action": "browser", "message": "Browser opened"}
        elif gesture_name == "Call Me Sign":
            self._mute_system()
            result = {"action": "mute", "message": "System muted"}
        return result

    def _toggle_media(self) -> None:
        if sys.platform.startswith("win"):
            os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys(' ')" )
        else:
            subprocess.run(["xdg-open", ""], check=False)

    def _move_cursor(self, bbox: dict[str, Any] | None) -> None:
        if bbox is None:
            return
        screen_width, screen_height = pyautogui.size()
        target_x = int((bbox["x_min"] + bbox["x_max"]) / 2)
        target_y = int((bbox["y_min"] + bbox["y_max"]) / 2)
        x = int((target_x / 1000) * screen_width)
        y = int((target_y / 1000) * screen_height)
        pyautogui.moveTo(x, y, duration=0.01)
        self.last_cursor = (x, y)

    def _left_click(self) -> None:
        now = time.time()
        if now - self.last_click_time > 0.25:
            pyautogui.click()
            self.last_click_time = now

    def _volume_up(self) -> None:
        if sys.platform.startswith("win"):
            os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]175)")

    def _volume_down(self) -> None:
        if sys.platform.startswith("win"):
            os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]174)")

    def _screenshot(self, frame: Any) -> None:
        save_frame(frame, prefix="gesture")

    def _open_calculator(self) -> None:
        if sys.platform.startswith("win"):
            os.startfile("calc")

    def _open_browser(self) -> None:
        if sys.platform.startswith("win"):
            os.startfile("https://www.google.com")

    def _mute_system(self) -> None:
        if sys.platform.startswith("win"):
            os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]173)")
