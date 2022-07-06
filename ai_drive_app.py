import torch

from controller import ControllerState
from model import Model
from cv2 import cv2
import os
import numpy as np
import shutil
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from threading import Thread
from mk_capture import MKScreenCapture
from frame_addons import VisualController


class AiDriveApp(tk.Tk):
    def __init__(self):
        super(AiDriveApp, self).__init__()
        self.title("AI Drive App")
        self.geometry("550x400")
        self.controller_sate = ControllerState()
        self.visual_controller = VisualController()
        self.started = False
        self.Mk_screen_capture = None
        self.app_open = True
        self.recording = False
        self.model_loaded = False
        self.model_path = tk.StringVar()
        self.model_path_entry = tk.Entry(self, width=200, textvariable=self.model_path)
        self.model = Model()
        self.load_model_button = tk.Button(self, text="Load Model", command=self.load_model)
        self.crop_up = tk.IntVar()
        self.crop_left = tk.IntVar()
        self.crop_down = tk.IntVar()
        self.crop_right = tk.IntVar()
        self.crop_frame = tk.Frame(self)
        self.crop_up_entry = tk.Entry(self.crop_frame, textvariable=self.crop_up)
        self.crop_down_entry = tk.Entry(self.crop_frame, textvariable=self.crop_down)
        self.crop_left_entry = tk.Entry(self.crop_frame, textvariable=self.crop_left)
        self.crop_right_entry = tk.Entry(self.crop_frame, textvariable=self.crop_right)
        self.crop_button = tk.Button(self.crop_frame, text="Crop", command=self.crop)
        self.start_button = tk.Button(self, text="Start", command=self.start_record)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_record)
        self.recorder_thread = Thread(target=self.record)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def pack_record_ui(self):
        self.crop_frame.pack(side=tk.LEFT)
        self.crop_up_entry.pack(side=tk.LEFT)
        self.crop_down_entry.pack(side=tk.LEFT)
        self.crop_left_entry.pack(side=tk.LEFT)
        self.crop_right_entry.pack(side=tk.LEFT)
        self.crop_button.pack()

    def forget_record_gui(self):
        self.crop_frame.forget()
        self.crop_up_entry.forget()
        self.crop_down_entry.forget()
        self.crop_left_entry.forget()
        self.crop_right_entry.forget()
        self.crop_button.forget()

    def start_record(self):
        if not self.started:
            try:
                self.Mk_screen_capture = MKScreenCapture()
                self.started = True
                self.recorder_thread.start()
            except Exception as e:
                print("[AiDriveApp] Cannot find mario kart window")
        self.recording = True
        self.start_button.forget()
        self.stop_button.pack()
        self.pack_record_ui()

    def stop_record(self):
        self.recording = False
        self.forget_record_gui()
        self.stop_button.forget()
        self.pack_record_ui()

    def load_model(self):
        model_path = self.model_path.get()
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()
            self.model_loaded = True
        else:
            tkMessageBox.showerror(title="Invalid Model Path", message="Invalid Model Path")

    def record(self):
        while True:
            while self.recording:
                frame = self.Mk_screen_capture.capture_frame()
                # TODO add model prediction
                showen_frame = self.visual_controller.draw_controller(showen_frame, showen_state)
                cv2.imshow("mario kart wii", showen_frame)

            cv2.destroyAllWindows()
            if not self.app_open:
                break

    def crop(self):
        try:
            self.Mk_screen_capture.crop_up = self.crop_up.get()
            self.Mk_screen_capture.crop_down = self.crop_down.get()
            self.Mk_screen_capture.crop_left = self.crop_left.get()
            self.Mk_screen_capture.crop_right = self.crop_right.get()
        except tk.TclError as e:
            self.Mk_screen_capture.crop_up = 0
            self.Mk_screen_capture.crop_down = 0
            self.Mk_screen_capture.crop_left = 0
            self.Mk_screen_capture.crop_right = 0

    def close_app(self):
        self.started = False
        self.app_open = False
        self.destroy()
