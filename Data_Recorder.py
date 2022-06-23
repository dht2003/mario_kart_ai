import tkinter as tk
from cv2 import cv2
from controller import ControllerState
from mk_capture import MKScreenCapture
from frame_addons import VisualController
from threading import Thread
import pygame


class DataRecorder(tk.Tk):
    def __init__(self, fps=12):
        super(DataRecorder, self).__init__()

        self.title('Data Recorder')
        self.geometry('500x50')
        self.controller_state = ControllerState()
        self.Mk_screen_capture = MKScreenCapture()
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.fps = fps
        self.video_writer = cv2.VideoWriter("recorder_test/test.avi", self.fourcc, fps,
                                            self.Mk_screen_capture.frame_size)
        self.visual_controller = VisualController()
        self.recorder_thread = Thread(target=self.record)
        self.recording = False
        self.started = False
        self.app_open = True
        self.paused = False
        self.start_button = tk.Button(self, text="Start", command=self.start_record)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_record)
        self.pause_button = tk.Button(self, text="Pause", command=self.pause_record)
        self.start_button.pack()
        self.stop_button.pack()
        self.pause_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def record(self):
        # TODO : add keyboard recordings
        while True:
            while self.recording:
                for event in pygame.event.get():
                    self.handle_inputs(event)
                frame = self.Mk_screen_capture.capture_frame()
                self.video_writer.write(frame)
                frame = self.visual_controller.draw_controller(frame, self.controller_state)
                cv2.imshow("mario kart wii", frame)

                if not self.recording:
                    break

                while self.paused and self.recording:
                    cv2.imshow("mario kart wii", frame)

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

    def pause_record(self):
        self.paused = not self.paused

    def handle_inputs(self, input_event):
        if input_event.type == pygame.JOYBUTTONDOWN:
            self.controller_state.press_button(input_event.button)
        if input_event.type == pygame.JOYBUTTONUP:
            self.controller_state.release_button(input_event.button)
        if input_event.type == pygame.JOYAXISMOTION:
            self.controller_state.steer(input_event.value, input_event.axis)

    def close_app(self):
        self.recording = False
        self.app_open = False
        self.destroy()
