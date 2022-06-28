import pygame
from Data_Recorder import DataRecorder


def main():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    recorder = DataRecorder()
    recorder.mainloop()


if __name__ == '__main__':
    main()
