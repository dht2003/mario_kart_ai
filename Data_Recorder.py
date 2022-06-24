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
        self.geometry('500x200')
        self.controller_state = ControllerState()
        self.Mk_screen_capture = MKScreenCapture()
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.fps = fps

        self.visual_controller = VisualController()
        self.recorder_thread = Thread(target=self.record)
        self.frame_idx = 0
        self.current_frame = 0
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
        self.start_button.pack()
        self.stop_button.pack()
        self.pause_button.pack()
        self.next_button.pack()
        self.prev_button.pack()
        self.save_file_path_entry.pack()
        self.save_button.pack()

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
                showen_frame = copy.copy(self.frames[self.current_frame])
                showen_state = self.controller_states[self.current_frame]
                showen_frame = self.visual_controller.draw_controller(showen_frame, showen_state)
                cv2.imshow("mario kart wii", showen_frame)

                self.current_frame = self.current_frame if self.paused else self.frame_idx
                if not self.paused:
                    self.frame_idx += 1

            cv2.destroyAllWindows()
            if not self.app_open:
                break

    def start_record(self):
        if not self.started:
            self.recorder_thread.start()
            self.started = True
        if not self.recording:
            self.recording = True

    def stop_record(self):
        self.recording = False
        self.paused = False
        self.frames.clear()
        self.controller_states.clear()
        self.frame_idx = self.current_frame = 0

    def pause_record(self):
        if self.recording:
            self.paused = not self.paused

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1

    def next_frame(self):
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1

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

    def close_app(self):
        self.recording = False
        self.app_open = False
        self.destroy()
