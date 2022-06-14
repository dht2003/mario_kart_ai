import time
import pygetwindow
import pyautogui
import PIL
import numpy as np
from cv2 import cv2


def fps_counter(func):
    def wrap(s):
        s.new_frame_time = time.time()
        fps = 1 / (s.new_frame_time - s.prev_frame_time)
        frame = func(s)
        cv2.putText(frame, str(int(fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        s.prev_frame_time = s.new_frame_time
        return frame

    return wrap


class ScreenCapture:
    # TODO : add save footage
    def __init__(self, window_title):
        self.window = pygetwindow.getWindowsWithTitle(window_title)[0]
        self.window.activate()
        self.prev_frame_time = 0
        self.new_frame_time = 0

    def capture_frame(self):
        img = pyautogui.screenshot(region=(self.window.left, self.window.top, self.window.width, self.window.height))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    @fps_counter
    def capture_frame_fps(self):
        return self.capture_frame()
