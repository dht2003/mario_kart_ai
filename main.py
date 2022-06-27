from cv2 import cv2
import pygame
import mk_capture
import frame_addons
import controller
from Data_Recorder import DataRecorder
import numpy as np


def main():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    path = "D:/dev/mario_kart_ai/samples/2022-06-27_22_44_28/data.csv"
    npcsv_str = np.genfromtxt(path, delimiter=',', encoding='utf8', usecols=0, dtype=str)
    print(type(npcsv_str))

    recorder = DataRecorder()
    recorder.mainloop()


if __name__ == '__main__':
    main()
