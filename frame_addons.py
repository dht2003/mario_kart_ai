from cv2 import cv2


class Button:
    def __init__(self, button_str, is_pressed, position, button_radius=10):
        self._button_str = button_str
        self._isPressed = is_pressed
        self._position = position
        self._button_radius = button_radius
        self.button_color = (255, 0, 0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_scale = 1
        self.text_thickness = 2
        self._button_text_size, _ = cv2.getTextSize(button_str, self.font, self.text_scale, self.text_thickness)
        self._text_position = (
            self._position[0] - self._button_text_size[0] // 2, self._position[1] + self._button_text_size[1] // 2)

    def draw_button(self, frame):
        cv2.circle(frame, self.position, self._button_radius, self.button_color, 2)
        cv2.putText(frame, self.button_str, self.text_position, self.font, self.text_scale, self.button_color,
                    self.text_thickness)
        return frame

    @property
    def button_str(self):
        return self._button_str

    @button_str.setter
    def button_str(self, button_str):
        self._button_str = button_str

    @property
    def is_pressed(self):
        return self._isPressed

    @is_pressed.setter
    def is_pressed(self, value):
        self._isPressed = value

    @property
    def position(self):
        return self._position

    @property
    def text_position(self):
        return self._text_position

    @property
    def button_radius(self):
        return self._button_radius
