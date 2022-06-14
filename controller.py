from dataclasses import dataclass


@dataclass
class ControllerState:
    A_BUTTON: int
    B_BUTTON: int
    L_BUTTON: int
    START_BUTTON: int
    D_PAD_UP: int
    D_PAD_DOWN: int
    D_PAD_RIGHT: int
    D_PAD_LEFT: int
    STEER_X: float
    STEER_Y: float

    def translate_joy_motion(self, axis, value):
        if axis == 0:
            self.STEER_X = value
        elif axis == 1:
            self.STEER_Y = value

