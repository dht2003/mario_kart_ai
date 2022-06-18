from cv2 import cv2


class Button:
    def __init__(self, button_str, button_radius=10):
        self._button_str = button_str
        self._button_radius = button_radius
        self.button_color = (255, 0, 0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_scale = 1
        self.text_thickness = 2
        self._button_text_size, _ = cv2.getTextSize(button_str, self.font, self.text_scale, self.text_thickness)

    def draw_button(self, frame, position, is_pressed):
        frame = frame.copy()
        text_position = (
            position[0] - self._button_text_size[0] // 2, position[1] + self._button_text_size[1] // 2)
        if is_pressed:
            cv2.circle(frame, position, self._button_radius, self.button_color, -1)
            cv2.putText(frame, self.button_str, text_position, self.font, self.text_scale, (100, 255, 255),
                        self.text_thickness)
        else:
            cv2.circle(frame, position, self._button_radius, self.button_color, 2)
            cv2.putText(frame, self.button_str, text_position, self.font, self.text_scale, self.button_color,
                        self.text_thickness)
        return frame

    @property
    def button_str(self):
        return self._button_str

    @button_str.setter
    def button_str(self, button_str):
        self._button_str = button_str

    @property
    def button_radius(self):
        return self._button_radius


class Joystick:
    def __init__(self, radius):
        self.outer_joystick = radius
        self.inner_joystick = int(radius / 2)
        self.joystick_color = (255, 0, 0)
        self.joystick_thickness = 2

    def draw_joystick(self, frame, position, steer_x, steer_y):
        frame = frame.copy()
        inner_x_position = int(position[0] + (steer_x * self.outer_joystick))
        inner_y_position = int(position[1] + (steer_y * self.outer_joystick))
        cv2.circle(frame, (inner_x_position, inner_y_position), self.inner_joystick, self.joystick_color,
                   self.joystick_thickness)
        cv2.circle(frame, position, self.outer_joystick, self.joystick_color, self.joystick_thickness)
        return frame


class VisualController:
    def __init__(self):
        self.a_button = Button("A", 20)
        self.b_button = Button("B", 20)
        self.y_button = Button("Y", 20)
        self.x_button = Button("X", 20)
        self.l_button = Button("L", 20)
        self.joystick = Joystick(40)

    def draw_controller(self, frame, controller_state):
        frame = frame.copy()
        h, w, _ = frame.shape
        offset_x = offset_y = 20
        frame = self.joystick.draw_joystick(frame, (
            w - offset_x - self.joystick.outer_joystick, h - offset_y - self.joystick.outer_joystick),
                                            controller_state.steer_x, controller_state.steer_y)
        frame = self.a_button.draw_button(frame, (
            self.a_button.button_radius + offset_x, h - self.a_button.button_radius - offset_y),
                                          controller_state.a_pressed())
        offset_y += 50
        frame = self.b_button.draw_button(frame, (
            self.b_button.button_radius + offset_x, h - self.b_button.button_radius - offset_y),
                                          controller_state.b_pressed())
        offset_y += 50
        frame = self.x_button.draw_button(frame, (
            self.x_button.button_radius + offset_x, h - self.a_button.button_radius - offset_y),
                                          controller_state.x_pressed())
        offset_y += 50
        frame = self.y_button.draw_button(frame, (
            self.y_button.button_radius + offset_x, h - self.a_button.button_radius - offset_y),
                                          controller_state.y_pressed())

        return frame
