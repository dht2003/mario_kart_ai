import time
import pygetwindow
import pyautogui
from PIL import Image, ImageTk
import numpy as np
from cv2 import cv2


def fps_counter(func):
    def wrap(s):
        s.new_frame_time = time.time()
        fps = 1 / (s.new_frame_time - s.prev_frame_time)
        frame = func(s)
        cv2.putText(frame, str(int(fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)
        s.prev_frame_time = s.new_frame_time
        return frame

    return wrap


class ScreenCapture:
    # TODO : Add crop methods
    def __init__(self, window_title, frame_size=(820, 400)):
        self.window = pygetwindow.getWindowsWithTitle(window_title)[0]
        self.window.activate()
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.frame_size = frame_size
        self.rows_from_ = 0
        self.rows_to = frame_size[0]
        self.cols_from_ = 0
        self.cols_to = frame_size[1]

    def capture_frame(self):
        img = pyautogui.screenshot(region=(self.window.left, self.window.top, self.window.width, self.window.height))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frame = ScreenCapture.crop_frame(frame, self.rows_from_, self.rows_to, self.cols_from_, self.cols_to)
        frame = cv2.resize(frame, self.frame_size)
        return frame

    @staticmethod
    def cv2_to_imageTK(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        imagePIL = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=imagePIL)
        return imgtk

    @fps_counter
    def capture_frame_fps(self):
        return self.capture_frame()

    def set_crop_row(self, from_, to):
        self.rows_from_ = from_
        self.rows_to = to

    def set_crop_cols(self, from_, to):
        self.cols_from_ = from_
        self.cols_to = to

    @staticmethod
    def crop_frame(frame, rows_from_, rows_to, cols_from_, cols_to):
        frame = frame.copy()
        cropped_frame = frame[rows_from_:rows_to, cols_from_:cols_to]
        return cropped_frame
