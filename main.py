import pygetwindow
import pyautogui
import PIL
import numpy as np
from cv2 import cv2
import time
import pygame
import mk_capture
import frame_addons


def main():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    sc = mk_capture.MKScreenCapture()
    b = frame_addons.Button("A", 0, (100, 100), 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print("button: ", event.button)
            if event.type == pygame.JOYAXISMOTION:
                print(f"axis:{event.axis} , value:{event.value}")
        frame = sc.capture_frame_fps()
        b.draw_button(frame)
        cv2.imshow("mario kart wii", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
