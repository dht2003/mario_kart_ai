import json
import os
import numpy as np

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
        self._dpad_up = 0
        self._dpad_down = 0
        self._dpad_left = 0
        self._dpad_right = 0
        self._steer_x = 0
        self._steer_y = 0
        self.translator = GameCubeTranslator() if translator is None else translator

    def state(self):
        return np.array([self.steer_x, self.steer_y, self._a_button, self._b_button, self._l_button, self._x_button,
                         self._y_button,
                         self.z_button, self._dpad_up, self._dpad_down, self._dpad_left, self._dpad_right],
                        dtype=np.float32)

    def writefile(self, file):
        np.savetxt(file, self.state(), newline=',')

    def __getitem__(self, key):
        key = self.translator[key]
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
        key = self.translator[key]
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
        self._a_button = round(value)

    @property
    def b_button(self):
        return self._b_button

    @b_button.setter
    def b_button(self, value):
        self._b_button = round(value)

    @property
    def l_button(self):
        return self._l_button

    @l_button.setter
    def l_button(self, value):
        self._l_button = round(value)

    @property
    def x_button(self):
        return self._x_button

    @x_button.setter
    def x_button(self, value):
        self._x_button = round(value)

    @property
    def y_button(self):
        return self._y_button

    @y_button.setter
    def y_button(self, value):
        self._y_button = round(value)

    @property
    def z_button(self):
        return self._z_button

    @z_button.setter
    def z_button(self, value):
        self._z_button = round(value)

    @property
    def start_button(self):
        return self._start_button

    @start_button.setter
    def start_button(self, value):
        self._start_button = value

    @property
    def dpad_up(self):
        return self._dpad_up

    @dpad_up.setter
    def dpad_up(self, value):
        self._dpad_up = round(value)

    @property
    def dpad_down(self):
        return self._dpad_down

    @dpad_down.setter
    def dpad_down(self, value):
        self._dpad_down = round(value)

    @property
    def dpad_left(self):
        return self._dpad_left

    @dpad_left.setter
    def dpad_left(self, value):
        self._dpad_left = round(value)

    @property
    def dpad_right(self):
        return self._dpad_right

    @dpad_right.setter
    def dpad_right(self, value):
        self._dpad_right = round(value)

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
        l2_r2_threshold = 0.9
        if axis == 0:
            self.steer_x = value
        elif axis == 1:
            self.steer_y = value
        elif axis == 4:
            value = 1 if value > l2_r2_threshold else 0
            self.__setitem__(L2_MAP, value)
        elif axis == 5:
            value = 1 if value > l2_r2_threshold else 0
            self.__setitem__(R2_MAP, value)


class ControllerTranslator:
    def __init__(self, keys_file):
        self.keys_file = keys_file
        with open(os.path.join(keys_file)) as file:
            self.button_keys = json.load(file)

    def __getitem__(self, key):
        return self.button_keys[key]


class Ps4ControllerTranslator(ControllerTranslator):
    def __init__(self, ps4_key_file="ps4_keys.json"):
        super(Ps4ControllerTranslator, self).__init__(ps4_key_file)


class GameCubeTranslator(ControllerTranslator):
    def __init__(self, gamecube_keys_file="gamecube_keys.json"):
        super(GameCubeTranslator, self).__init__(gamecube_keys_file)
        self.button_keys = {int(k): v for k, v in self.button_keys.items()}
