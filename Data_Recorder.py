import tkinter as tk
from cv2 import cv2
from controller import ControllerState
from mk_capture import MKScreenCapture
from frame_addons import VisualController
from threading import Thread
import copy
import pygame


class DataRecorder(tk.Tk):
    def __init__(self, fps=12):
        super(DataRecorder, self).__init__()

        self.title('Data Recorder')
        self.geometry('500x300')
        self.controller_state = ControllerState()
        self.Mk_screen_capture = MKScreenCapture()
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.fps = fps

        self.visual_controller = VisualController()
        self.recorder_thread = Thread(target=self.record)
        self.frame_idx = 0
        self.current_frame_idx = 0
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
        self.save_file_path_entry = tk.Entry(self, width=200)
        self.save_button = tk.Button(self, text="Save", command=self.save_footage)
        self.go_start_button = tk.Button(self, text="Go Start", command=self.go_start)
        self.go_end_button = tk.Button(self, text="Go End", command=self.go_end)
        self.cut_footage_button = tk.Button(self, text="Cut Footage", command=self.cut_footage)
        self.start_scale = tk.Scale(self, orient=tk.HORIZONTAL)
        self.end_scale = tk.Scale(self, orient=tk.HORIZONTAL)
        self.pause_button.pack()
        self.start_button.pack()
        self.stop_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def record(self):
        # TODO : add keyboard recordings
        while True:
            while self.recording:
                if not self.recording:
                    break
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
        self.save_file_path_entry.forget()
        self.save_button.forget()
        self.go_start_button.forget()
        self.go_end_button.forget()
        self.start_scale.forget()
        self.end_scale.forget()
        self.cut_footage_button.forget()

    def pack_pause_ui(self):
        self.next_button.pack()
        self.prev_button.pack()
        self.save_file_path_entry.pack()
        self.save_button.pack()
        self.go_start_button.pack()
        self.go_end_button.pack()
        self.start_scale.pack()
        self.end_scale.pack()
        self.cut_footage_button.pack()

    def pack_record_gui(self):
        self.start_button.pack()
        self.stop_button.pack()

    def forget_record_gui(self):
        self.start_button.forget()
        self.stop_button.forget()

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
        video_writer = cv2.VideoWriter(self.save_file_path_entry.get(), self.fourcc, self.fps,
                                       self.Mk_screen_capture.frame_size)
        for frame in self.frames:
            video_writer.write(frame)

    def go_start(self):
        self.current_frame_idx = self.start_scale.get()

    def go_end(self):
        self.current_frame_idx = self.end_scale.get()

    def cut_footage(self):
        self.current_frame_idx = 0
        self.frames = self.frames[self.start_scale.get():self.end_scale.get()]
        self.controller_states = self.controller_states[self.start_scale.get():self.end_scale.get()]
        self.frame_idx = len(self.frames) - 1
        self.update_sliders()

    def close_app(self):
        self.recording = False
        self.paused = False
        self.app_open = False
        self.destroy()
