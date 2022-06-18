class ControllerState:

    def __init__(self):
        self._a_button = 0
        self._b_button = 0
        self._l_button = 0
        self._x_button = 0
        self._y_button = 0
        self._steer_x = 0
        self._steer_y = 0

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
