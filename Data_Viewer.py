import os
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from threading import Thread

import matplotlib
import numpy as np
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

matplotlib.use('TkAgg')

CONTROLLER_STATE_END_COL = 13


class DataViewer(tk.Tk):
    def __init__(self):
        super(DataViewer, self).__init__()
        self.geometry('900x1000')
        self.frames_paths = None
        self.controller_states = None
        self.save_dir_path = tk.StringVar()
        self.go_frame_var = tk.IntVar()
        self.save_dir_path_entry = tk.Entry(self, width=200, textvariable=self.save_dir_path)
        self.read_save_button = tk.Button(self, text="Read Recording", command=self.read_save)
        self.next_button = tk.Button(self, text="Next Frame", command=self.next_frame)
        self.prev_button = tk.Button(self, text="Previous Frame", command=self.prev_frame)
        self.go_start_button = tk.Button(self, text="Go Start", command=self.go_start)
        self.go_end_button = tk.Button(self, text="Go End", command=self.go_end)
        self.path_label = tk.Label(self, text="")
        self.play_recording_button = tk.Button(self, text="Show Recording", command=self.start_recording_play)
        self.go_frame_entry = tk.Entry(self, textvariable=self.go_frame_var)
        self.go_frame_button = tk.Button(self, text="GO Frame", command=self.go_frame)
        self.fig = None
        self.axes = None
        self.init_plot()
        self.PlotCanvas = FigCanvas(figure=self.fig)
        self.panel = None
        self.save_dir_path_entry.pack()
        self.read_save_button.pack()
        self.next_button.pack()
        self.prev_button.pack()
        self.go_start_button.pack()
        self.go_end_button.pack()
        self.go_frame_entry.pack()
        self.go_frame_button.pack()
        self.play_recording_button.pack()
        self.path_label.pack()
        self.PlotCanvas.get_tk_widget().pack()
        self.current_frame_idx = 0
        self.video_loop_thread = Thread(target=self.video_loop)
        self.started = False
        self.playing_recording = False
        self.app_open = True
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def read_save(self):
        save_dir_path = self.save_dir_path.get()
        recording_path = os.path.join(save_dir_path, "recording")
        data_csv_path = os.path.join(save_dir_path, "data.csv")
        if os.path.exists(save_dir_path) and os.path.exists(recording_path) and os.path.exists(data_csv_path):
            self.frames_paths = np.genfromtxt(data_csv_path, delimiter=',', encoding='utf8', usecols=0, dtype=str)
            self.controller_states = np.genfromtxt(data_csv_path, delimiter=',', encoding='utf8',
                                                   usecols=range(1, CONTROLLER_STATE_END_COL),
                                                   dtype=np.float32)  # TODO: Improve this line
            self.current_frame_idx = 0
            if not self.started:
                self.video_loop_thread.start()
                self.started = True
        else:
            tkMessageBox.showerror(title="Invalid recording path", message="Recording Path is invalid")

    def init_plot(self):
        self.fig = Figure(figsize=(4, 3), dpi=80)
        self.axes = self.fig.add_subplot(111)

    def draw_plot(self):
        self.axes.clear()
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 0], 'r')  # X
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 1], 'b')  # Y
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 2], 'g')  # A
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 3], 'k')  # B
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 4], 'y')  # l
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 5], 'm')  # x
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 6], 'k')  # y
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 7], 'c')  # z
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 8],
                       'tab:pink')  # up
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 9],
                       'tab:orange')  # dd
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 10],
                       'tab:purple')  # dl
        self.axes.plot(range(0, self.current_frame_idx), self.controller_states[:self.current_frame_idx, 11],
                       'tab:brown')  # dr
        self.PlotCanvas.draw()

    def video_loop(self):
        while self.app_open:
            if self.playing_recording:
                if self.current_frame_idx < len(self.frames_paths) - 1:
                    self.current_frame_idx += 1
                else:
                    self.playing_recording = False
            current_path = self.frames_paths[self.current_frame_idx]
            image = ImageTk.PhotoImage(Image.open(current_path))
            self.path_label.config(text=current_path)

            if self.panel is None:
                self.panel = tk.Label(image=image)
                self.panel.image = image
                self.panel.pack(padx=10, pady=10)

            else:
                self.panel.configure(image=image)
                self.panel.image = image
            self.draw_plot()

    def prev_frame(self):
        if self.current_frame_idx > 0:
            self.current_frame_idx -= 1

    def next_frame(self):
        if self.current_frame_idx < len(self.frames_paths) - 1:
            self.current_frame_idx += 1

    def go_start(self):
        self.current_frame_idx = 0

    def go_end(self):
        self.current_frame_idx = len(self.frames_paths) - 1

    def go_frame(self):
        if self.go_frame_var.get() < len(self.frames_paths) - 1:
            self.current_frame_idx = self.go_frame_var.get()

    def start_recording_play(self):
        self.current_frame_idx = 0
        self.playing_recording = True

    def on_close(self):
        self.app_open = False
        self.started = False
        self.destroy()
