from cv2 import cv2
import pygame
import mk_capture
import frame_addons
import controller


def main():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    sc = mk_capture.MKScreenCapture()
    vc = frame_addons.VisualController()
    cs = controller.ControllerState()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                cs.press_button(event.button)
            if event.type == pygame.JOYBUTTONUP:
                cs.release_button(event.button)
            if event.type == pygame.JOYAXISMOTION:
                cs.steer(event.value, event.axis)

        frame = sc.capture_frame_fps()
        frame = vc.draw_controller(frame, cs)
        cv2.imshow("mario kart wii", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
