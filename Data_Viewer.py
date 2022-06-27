import tkinter as tk
import tkinter.messagebox as tkMessageBox
from cv2 import cv2
from controller import ControllerState
import os
import shutil
import numpy as np


class DataViewer(tk.Tk):
    def __init__(self):
        super(DataViewer, self).__init__()
        self.geometry('500x300')
        self.frames = []
        self.controller_states = []
        self.save_dir_path = tk.StringVar()
        self.save_dir_path_entry = tk.Entry(self, width=200, textvariable=self.save_dir_path)
        self.read_save_button = tk.Button(self, text="Read Recording", command=self.read_save)

    def read_save(self):
        save_dir_path = self.save_dir_path.get()
        recording_path = os.path.join(save_dir_path, "recording")
        data_csv_path = os.path.join(save_dir_path, "data.csv")
        if os.path.exists(save_dir_path) and os.path.exists(recording_path) and os.path.exists(data_csv_path):
            pass
        else:
            tkMessageBox.showerror(title="Invalid recording path", message="Recording Path is invalid")
