import json
import os
import numpy as np
import vgamepad as vg
import time

L2_MAP = 15
R2_MAP = 16


class ControllerState:

    def __init__(self, translator=None):
        self._a_button = 0
        self._b_button = 0
        self._l_button = 0
        self._x_button = 0
        self._y_button = 0
        self._z_button = 0
        self._start_button = 0
        self.button_threshold = 0.85
        self._dpad_up = 0
        self._dpad_down = 0
        self._dpad_left = 0
        self._dpad_right = 0
        self._steer_x = 0
        self._steer_y = 0
        self.gc_translator = GameCubeTranslator() if translator is None else translator
        self.ps_translator = PsTranslator()
        self.gamepad = vg.VDS4Gamepad()

    def state(self):
        return np.array([self.steer_x, self.steer_y, self._a_button, self._b_button, self._l_button, self._x_button,
                         self._y_button,
                         self.z_button, self._dpad_up, self._dpad_down, self._dpad_left, self._dpad_right],
                        dtype=np.float32)

    def __str__(self):
        return f"Controller State:\njoystick: x:{self.steer_x},y:{self.steer_y}\nA:{self.a_button}\nB:{self.b_button}\nL:{self.l_button}\nX:{self.x_button}\nY:{self.y_button}\nZ:{self.z_button}\nSTART:{self.start_button}\nDPAD: up:{self.dpad_up},down:{self.dpad_down},left:{self.dpad_left},right:{self.dpad_right}"

    def writefile(self, file):
        np.savetxt(file, self.state(), newline=',')

    def __getitem__(self, key):
        key = self.gc_translator[key]
        key = key.lower()
        if key == "a":
            return self.a_button
        elif key == "b":
            return self.b_button
        elif key == "l":
            return self.l_button
        elif key == "x":
            return self.x_button
        elif key == "y":
            return self.y_button
        elif key == "z":
            return self.z_button
        elif key == "dpad-up":
            return self.dpad_up
        elif key == "dpad-down":
            return self.dpad_down
        elif key == "dpad-left":
            return self.dpad_left
        elif key == "dpad-right":
            return self.dpad_right
        elif key == "start":
            return self._start_button
        elif key == "steer_x":
            return self.steer_x
        elif key == "steer_y":
            return self.steer_y
        else:
            raise KeyError("[ControllerState] Invalid key")

    def __setitem__(self, key, value):
        key = self.gc_translator[key]
        key = key.lower()
        if key == "a":
            self.a_button = value
        elif key == "b":
            self.b_button = value
        elif key == "l":
            self.l_button = value
        elif key == "x":
            self.x_button = value
        elif key == "y":
            self.y_button = value
        elif key == "z":
            self.z_button = value
        elif key == "start":
            self._start_button = value
        elif key == "dpad-up":
            self.dpad_up = value
        elif key == "dpad-down":
            self.dpad_down = value
        elif key == "dpad-left":
            self.dpad_left = value
        elif key == "dpad-right":
            self.dpad_right = value
        elif key == "steer_x":
            self.steer_x = value
        elif key == "steer_y":
            self.steer_y = value

    def press_button(self, button):
        self.__setitem__(button, 1)

    def release_button(self, button):
        self.__setitem__(button, 0)

    @property
    def a_button(self):
        return self._a_button

    @a_button.setter
    def a_button(self, value):
        self._a_button = 1 if value > self.button_threshold else 0

    @property
    def b_button(self):
        return self._b_button

    @b_button.setter
    def b_button(self, value):
        self._b_button = 1 if value > self.button_threshold else 0

    @property
    def l_button(self):
        return self._l_button

    @l_button.setter
    def l_button(self, value):
        self._l_button = 1 if value > self.button_threshold else 0

    @property
    def x_button(self):
        return self._x_button

    @x_button.setter
    def x_button(self, value):
        self._x_button = 1 if value > self.button_threshold else 0

    @property
    def y_button(self):
        return self._y_button

    @y_button.setter
    def y_button(self, value):
        self._y_button = 1 if value > self.button_threshold else 0

    @property
    def z_button(self):
        return self._z_button

    @z_button.setter
    def z_button(self, value):
        self._z_button = 1 if value > self.button_threshold else 0

    @property
    def start_button(self):
        return self._start_button

    @start_button.setter
    def start_button(self, value):
        self._start_button = 1 if value > self.button_threshold else 0

    @property
    def dpad_up(self):
        return self._dpad_up

    @dpad_up.setter
    def dpad_up(self, value):
        self._dpad_up = 1 if value > self.button_threshold else 0

    @property
    def dpad_down(self):
        return self._dpad_down

    @dpad_down.setter
    def dpad_down(self, value):
        self._dpad_down = 1 if value > self.button_threshold else 0

    @property
    def dpad_left(self):
        return self._dpad_left

    @dpad_left.setter
    def dpad_left(self, value):
        self._dpad_left = 1 if value > self.button_threshold else 0

    @property
    def dpad_right(self):
        return self._dpad_right

    @dpad_right.setter
    def dpad_right(self, value):
        self._dpad_right = 1 if value > self.button_threshold else 0

    @property
    def steer_x(self):
        return self._steer_x

    @steer_x.setter
    def steer_x(self, value):
        self._steer_x = value

    @property
    def steer_y(self):
        return self._steer_y

    @steer_y.setter
    def steer_y(self, value):
        self._steer_y = value

    def a_pressed(self):
        return self._a_button == 1

    def b_pressed(self):
        return self._b_button == 1

    def y_pressed(self):
        return self._y_button == 1

    def x_pressed(self):
        return self._x_button == 1

    def l_pressed(self):
        return self._l_button == 1

    def start_pressed(self):
        return self._start_button == 1

    def z_pressed(self):
        return self._z_button == 1

    def dpad_up_pressed(self):
        return self._dpad_up == 1

    def dpad_down_pressed(self):
        return self._dpad_down == 1

    def dpad_left_pressed(self):
        return self._dpad_left == 1

    def dpad_right_pressed(self):
        return self._dpad_right == 1

    def steer(self, value, axis):
        triggers_threshold = 0.9
        joystick_threshold = 0.1
        axis = self.gc_translator.get_axis(axis)
        if axis == "X":
            value = 0 if abs(value) <= joystick_threshold else value
            self.steer_x = value
        elif axis == "Y":
            value = 0 if abs(value) <= joystick_threshold else value
            self.steer_y = value
        elif axis == "Left-trigger":
            value = 1 if value > triggers_threshold else 0
            self.__setitem__(L2_MAP, value)
        elif axis == "Right-trigger":
            value = 1 if value > triggers_threshold else 0
            self.__setitem__(R2_MAP, value)

    def load_state(self, state_list):
        self.steer_x = state_list[0]
        self.steer_y = state_list[1]
        self.a_button = state_list[2]
        self.b_button = state_list[3]
        self.l_button = state_list[4]
        self.x_button = state_list[5]
        self.y_button = state_list[6]
        self.z_button = state_list[7]
        self.dpad_up = state_list[8]
        self.dpad_down = state_list[9]
        self.dpad_left = state_list[10]
        self.dpad_right = state_list[11]

    def emulate_outputs(self):
        if self.a_pressed():
            self.emulate_button_press("A")
        else:
            self.emulate_button_release("A")
        if self.b_pressed():
            self.emulate_button_press("B")
        else:
            self.emulate_button_release("B")
        if self.l_pressed():
            self.emulate_button_press("L-TRIGGER")
        else:
            self.emulate_button_release("L-TRIGGER")
        if self.x_pressed():
            self.emulate_button_press("X")
        else:
            self.emulate_button_release("X")
        if self.y_pressed():
            self.emulate_button_press("Y")
        else:
            self.emulate_button_release("Y")
        if self.z_pressed():
            self.emulate_button_press("Z")
        else:
            self.emulate_button_release("Z")
        if self.start_pressed():
            self.emulate_button_press("START")
        else:
            self.emulate_button_release("START")
        if self.dpad_up_pressed():
            self.emulate_button_press("DPAD-UP")
        else:
            self.emulate_button_release("DPAD-UP")
        if self.dpad_down_pressed():
            self.emulate_button_press("DPAD-DOWN")
        else:
            self.emulate_button_release("DPAD-DOWN")
        if self.dpad_left_pressed():
            self.emulate_button_press("DPAD-LEFT")
        else:
            self.emulate_button_release("DPAD-LEFT")
        if self.dpad_right_pressed():
            self.emulate_button_press("DPAD-RIGHT")
        else:
            self.emulate_button_release("DPAD-RIGHT")
        self.gamepad.left_joystick_float(self.steer_x, self.steer_y)
        self.gamepad.update()

    def emulate_button_press(self, key):
        key = self.ps_translator[key]
        if key == "square":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
        elif key == "triangle":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        elif key == "x":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
        elif key == "circle":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        elif key == "options":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        elif key == "hat-north":
            self.gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH)
        elif key == "hat-south":
            self.gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH)
        elif key == "hat-west":
            self.gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST)
        elif key == "hat-east":
            self.gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST)
        elif key == "r-trigger":
            self.gamepad.right_trigger_float(1)
        elif key == "l-trigger":
            self.gamepad.left_trigger_float(1)
        elif key == "r1":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
        elif key == "l1":
            self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
        elif key == "touchpad":
            self.gamepad.press_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD)
        elif key == "ps":
            self.gamepad.press_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)

    def emulate_button_release(self, key):
        key = self.ps_translator[key]
        if key == "square":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
        elif key == "triangle":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        elif key == "x":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
        elif key == "circle":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        elif key == "options":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        elif key == "r-trigger":
            self.gamepad.right_trigger_float(0)
        elif key == "l-trigger":
            self.gamepad.left_trigger_float(0)
        elif key == "r1":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
        elif key == "l1":
            self.gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
        elif key == "touchpad":
            self.gamepad.release_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD)
        elif key == "ps":
            self.gamepad.release_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)


class ControllerTranslator:
    def __init__(self, keys_file, axis_file):
        self.keys_file = keys_file
        with open(os.path.join(keys_file)) as file:
            self.button_keys = json.load(file)
        self.axis_file = axis_file
        with open(os.path.join(axis_file)) as file:
            self.axis_dict = json.load(file)

    def __getitem__(self, key):
        return self.button_keys[key]

    def get_axis(self, axis):
        return self.axis_dict[axis]


class PsTranslator(ControllerTranslator):
    def __init__(self, ps4_key_file="ps4_keys.json", ps4_axis_file="ps4_axis.json"):
        super(PsTranslator, self).__init__(ps4_key_file, ps4_axis_file)


class GameCubeTranslator(ControllerTranslator):
    def __init__(self, gamecube_keys_file="gamecube_keys.json", gamecube_axis_file="gamecube_axis.json"):
        super(GameCubeTranslator, self).__init__(gamecube_keys_file, gamecube_axis_file)
        self.button_keys = {int(k): v for k, v in self.button_keys.items()}
        self.axis_dict = {int(k): v for k, v in self.axis_dict.items()}
