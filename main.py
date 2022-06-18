from cv2 import cv2
import pygame
import mk_capture
import frame_addons
import controller
import json
import os


def main():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    sc = mk_capture.MKScreenCapture()
    vc = frame_addons.VisualController()
    cs = controller.ControllerState()

    with open(os.path.join("ps4_keys.json"), 'r+') as file:
        button_keys = json.load(file)

    print(button_keys)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 3:
                    cs.a_button = 1
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 3:
                    cs.a_button = 0
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    cs.steer_x = event.value
                elif event.axis == 1:
                    cs.steer_y = event.value
        frame = sc.capture_frame_fps()
        frame = vc.draw_controller(frame, cs)
        cv2.imshow("mario kart wii", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
