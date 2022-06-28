import tkinter as tk
from cv2 import cv2
from controller import ControllerState
from mk_capture import MKScreenCapture
from frame_addons import VisualController
from threading import Thread
import copy
import pygame
import os
import shutil
import tkinter.messagebox as tkMessageBox
from datetime import datetime
import numpy as np

IMAGE_TYPE = ".png"


class DataRecorder(tk.Tk):
    def __init__(self):
        super(DataRecorder, self).__init__()

        self.title('Data Recorder')
        self.geometry('500x300')
        self.controller_state = ControllerState()
        self.Mk_screen_capture = MKScreenCapture()

        self.visual_controller = VisualController()
        self.recorder_thread = Thread(target=self.record)
        self.frame_idx = 0
        self.current_frame_idx = 0
        self.playing_recording = False
        self.frames = []
        self.controller_states = []
        self.recording = False
        self.started = False
        self.app_open = True
        self.paused = False
        self.start_button = tk.Button(self, text="Start", command=self.start_record)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_record)
        self.pause_button = tk.Button(self, text="Pause", command=self.pause_record)
        self.next_button = tk.Button(self, text="Next Frame", command=self.next_frame)
        self.prev_button = tk.Button(self, text="Previous Frame", command=self.prev_frame)
        self.save_dir_path = tk.StringVar()
        self.save_dir_path_entry = tk.Entry(self, width=200, textvariable=self.save_dir_path)
        self.save_button = tk.Button(self, text="Save", command=self.save_footage)
        self.go_start_button = tk.Button(self, text="Go Start", command=self.go_start)
        self.go_end_button = tk.Button(self, text="Go End", command=self.go_end)
        self.cut_footage_button = tk.Button(self, text="Cut Footage", command=self.cut_footage)
        self.play_recording_button = tk.Button(self, text="Show Recording", command=self.start_recording_play)
        self.start_scale = tk.Scale(self, orient=tk.HORIZONTAL)
        self.end_scale = tk.Scale(self, orient=tk.HORIZONTAL)
        self.crop_row_from = tk.IntVar()
        self.crop_col_from = tk.IntVar()
        self.crop_row_to = tk.IntVar()
        self.crop_col_to = tk.IntVar()
        self.crop_frame = tk.Frame(self)
        self.crop_row_from_entry = tk.Entry(self.crop_frame, textvariable=self.crop_row_from)
        self.crop_row_to_entry = tk.Entry(self.crop_frame, textvariable=self.crop_row_to)
        self.crop_col_from_entry = tk.Entry(self.crop_frame, textvariable=self.crop_col_from)
        self.crop_col_to_entry = tk.Entry(self.crop_frame, textvariable=self.crop_col_to)
        self.crop_button = tk.Button(self.crop_frame, text="Crop", command=self.crop)
        self.pack_record_gui()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def record(self):
        while True:
            while self.recording:
                if self.playing_recording:
                    if self.current_frame_idx < len(self.frames) - 1:
                        self.current_frame_idx += 1
                    else:
                        self.playing_recording = False
                for event in pygame.event.get():
                    self.handle_inputs(event)
                if not self.paused:
                    frame = self.Mk_screen_capture.capture_frame()
                    self.frames.append(frame)
                    self.controller_states.append(copy.copy(self.controller_state))
                showen_frame = copy.copy(self.frames[self.current_frame_idx])
                showen_state = self.controller_states[self.current_frame_idx]
                showen_frame = self.visual_controller.draw_controller(showen_frame, showen_state)
                cv2.imshow("mario kart wii", showen_frame)

                self.current_frame_idx = self.current_frame_idx if self.paused else self.frame_idx
                if not self.paused:
                    self.frame_idx += 1

            cv2.destroyAllWindows()
            if not self.app_open:
                break

    def forget_pause_gui(self):
        self.next_button.forget()
        self.prev_button.forget()
        self.save_dir_path_entry.forget()
        self.save_button.forget()
        self.go_start_button.forget()
        self.go_end_button.forget()
        self.start_scale.forget()
        self.end_scale.forget()
        self.cut_footage_button.forget()
        self.play_recording_button.forget()

    def pack_pause_ui(self):
        self.next_button.pack()
        self.prev_button.pack()
        self.save_dir_path_entry.pack()
        self.save_dir_path.set("samples/" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
        self.save_button.pack()
        self.go_start_button.pack()
        self.go_end_button.pack()
        self.start_scale.pack()
        self.end_scale.pack()
        self.cut_footage_button.pack()
        self.play_recording_button.pack()
        self.crop_row_from.set(0)
        self.crop_col_from.set(0)
        self.crop_row_to.set(self.Mk_screen_capture.frame_size[0])
        self.crop_col_to.set(self.Mk_screen_capture.frame_size[1])

    def pack_record_gui(self):
        self.start_button.pack()
        self.stop_button.pack()
        self.crop_frame.pack()
        self.crop_row_from_entry.pack()
        self.crop_row_to_entry.pack()
        self.crop_col_from_entry.pack()
        self.crop_col_to_entry.pack()
        self.crop_button.pack()

    def forget_record_gui(self):
        self.start_button.forget()
        self.stop_button.forget()
        self.crop_frame.forget()
        self.crop_row_from_entry.forget()
        self.crop_row_to_entry.forget()
        self.crop_col_from_entry.forget()
        self.crop_col_to_entry.forget()
        self.crop_button.forget()

    def update_sliders(self):
        self.start_scale.config(from_=0, to=self.frame_idx)
        self.end_scale.config(from_=0, to=self.frame_idx)
        self.start_scale.set(0)
        self.end_scale.set(self.frame_idx)

    def start_record(self):
        if not self.started:
            self.recorder_thread.start()
            self.started = True
        if not self.recording:
            self.recording = True

    def stop_record(self):
        self.recording = False
        if self.paused:
            self.forget_pause_gui()
        self.paused = False
        self.frames.clear()
        self.controller_states.clear()
        self.frame_idx = self.current_frame_idx = 0

    def pause_record(self):
        if self.recording:
            self.paused = not self.paused
            if self.paused:
                self.update_sliders()
                self.end_scale.set(self.frame_idx)
                self.pack_pause_ui()
                self.forget_record_gui()
            else:
                self.forget_pause_gui()
                self.pack_record_gui()

    def prev_frame(self):
        if self.current_frame_idx > 0:
            self.current_frame_idx -= 1

    def next_frame(self):
        if self.current_frame_idx < len(self.frames) - 1:
            self.current_frame_idx += 1

    def handle_inputs(self, input_event):
        if input_event.type == pygame.JOYBUTTONDOWN:
            self.controller_state.press_button(input_event.button)
        if input_event.type == pygame.JOYBUTTONUP:
            self.controller_state.release_button(input_event.button)
        if input_event.type == pygame.JOYAXISMOTION:
            self.controller_state.steer(input_event.value, input_event.axis)

    def save_footage(self):
        save_dir_path = self.save_dir_path.get()
        if os.path.exists(save_dir_path):

            if tkMessageBox.askyesno(title='Warning!', message='Output Directory Exists - Overwrite Data?',
                                     parent=self):
                shutil.rmtree(save_dir_path)
                os.mkdir(save_dir_path)
            else:
                return

        else:
            os.mkdir(save_dir_path)

        recording_path = os.path.join(save_dir_path, "recording")
        os.mkdir(recording_path)
        data_csv_path = os.path.join(save_dir_path, "data.csv")
        with open(data_csv_path, 'w') as f:
            for i in range(self.frame_idx):
                frame_path = os.path.join(recording_path, f"{i + 1}" + IMAGE_TYPE)
                cv2.imwrite(frame_path, self.frames[i])
                f.write(frame_path + ',')
                # np.savetxt(f, self.controller_states[i].state(), newline=',')
                self.controller_states[i].writefile(f)
                f.write('\n')

    def go_start(self):
        self.current_frame_idx = self.start_scale.get()

    def go_end(self):
        self.current_frame_idx = self.end_scale.get()

    def start_recording_play(self):
        self.current_frame_idx = 0
        self.playing_recording = True

    def cut_footage(self):
        self.current_frame_idx = 0
        self.frames = self.frames[self.start_scale.get():self.end_scale.get()]
        self.controller_states = self.controller_states[self.start_scale.get():self.end_scale.get()]
        self.frame_idx = len(self.frames) - 1
        self.update_sliders()

    def crop(self):
        self.Mk_screen_capture.set_crop_row(self.crop_row_from.get(), self.crop_row_to.get())
        self.Mk_screen_capture.set_crop_cols(self.crop_col_from.get(), self.crop_col_to.get())

    def close_app(self):
        self.recording = False
        self.paused = False
        self.app_open = False
        self.destroy()
