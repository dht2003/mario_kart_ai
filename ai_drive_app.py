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
from PIL import Image
from torchvision import transforms


class AiDriveApp(tk.Tk):
    def __init__(self):
        super(AiDriveApp, self).__init__()
        self.title("AI Drive App")
        self.geometry("550x400")
        self.controller_sate = ControllerState()
        self.visual_controller = VisualController()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.started = False
        self.Mk_screen_capture = None
        self.app_open = True
        self.recording = False
        self.model_loaded = False
        self.show_prediction = False
        self.model_path = tk.StringVar()
        self.model_path_entry = tk.Entry(self, width=200, textvariable=self.model_path)
        self.model = Model()
        self.model.to(self.device)
        self.load_model_button = tk.Button(self, text="Load Model", command=self.load_model)
        self.transformations = transforms.Compose([transforms.ToTensor()])
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
        self.show_predictions_buttons = tk.Button(self, text="Show Predictions", command=self.prediction_visibility)
        self.recorder_thread = Thread(target=self.record)
        self.start_button.pack()
        self.model_path_entry.pack()
        self.load_model_button.pack()
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def pack_record_ui(self):
        self.show_predictions_buttons.pack()

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

        self.show_predictions_buttons.forget()

    def start_record(self):
        try:
            if not self.started:
                self.Mk_screen_capture = MKScreenCapture()
                self.started = True
                self.recorder_thread.start()

            self.recording = True
            self.start_button.forget()
            self.stop_button.pack()
            self.pack_record_ui()
        except Exception as e:
            print("[AiDriveApp] Cannot find mario kart window")

    def stop_record(self):
        self.recording = False
        self.start_button.pack()
        self.pack_record_ui()
        self.forget_record_gui()
        self.stop_button.forget()

    def load_model(self):
        model_path = self.model_path.get()
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path)
            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.model.eval()
            self.model_loaded = True
        else:
            tkMessageBox.showerror(title="Invalid Model Path", message="Invalid Model Path")

    def record(self):
        while True:
            while self.recording:
                showen_frame = self.Mk_screen_capture.capture_frame()
                if self.show_prediction and self.model_loaded:
                    frame = cv2.cvtColor(showen_frame, cv2.COLOR_RGB2BGR)
                    pil_frame = Image.fromarray(frame)
                    pil_frame.show()
                    frame_tensor = torch.unsqueeze(self.transformations(pil_frame), 0)
                    frame_tensor = frame_tensor.to(self.device)
                    prediction = self.model(frame_tensor)
                    prediction_list = prediction.tolist()[0]
                    print(prediction_list)
                    self.controller_sate.load_state(prediction_list)
                    showen_frame = self.visual_controller.draw_controller(showen_frame, self.controller_sate)
                cv2.imshow("Mario kart", showen_frame)
                cv2.waitKey(1)
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

    def prediction_visibility(self):
        if self.show_prediction and self.model_loaded:
            self.show_predictions_buttons.config(text="Hide Predictions")
        else:
            self.show_predictions_buttons.config(text="Show Predictions")
        self.show_prediction = not self.show_prediction

    def close_app(self):
        self.started = False
        self.app_open = False
        self.recording = False
        self.destroy()
