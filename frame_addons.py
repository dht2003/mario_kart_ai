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
        thickness = -1 if is_pressed else 2
        text_color = (100, 255, 255) if is_pressed else (255, 0, 0)
        cv2.circle(frame, position, self._button_radius, self.button_color, thickness)
        cv2.putText(frame, self.button_str, text_position, self.font, self.text_scale, text_color,
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


class DpadVisualizer:
    def __init__(self, dpad_size, dpad_offset=10):
        self.dpad_color = (255, 0, 0)
        self.dpad_size = dpad_size
        self.dpad_offset = dpad_offset

    def draw_dpad(self, frame, position, d_up, d_down, d_left, d_right):
        frame = frame.copy()
        up_center = (position[0], position[1] - self.dpad_offset)
        down_center = (position[0], position[1] + self.dpad_offset)
        left_center = (position[0] - self.dpad_offset, position[1])
        right_center = (position[0] + self.dpad_offset, position[1])
        up_thickness = -1 if d_up else 2
        down_thickness = -1 if d_down else 2
        left_thickness = -1 if d_left else 2
        right_thickness = -1 if d_right else 2
        cv2.rectangle(frame, (up_center[0] - self.dpad_size, up_center[1] + self.dpad_size),
                      (up_center[0] + self.dpad_size, up_center[1] - self.dpad_size), self.dpad_color, up_thickness)
        cv2.rectangle(frame, (down_center[0] - self.dpad_size, down_center[1] + self.dpad_size),
                      (down_center[0] + self.dpad_size, down_center[1] - self.dpad_size), self.dpad_color,
                      down_thickness)
        cv2.rectangle(frame, (left_center[0] - self.dpad_size, left_center[1] + self.dpad_size),
                      (left_center[0] + self.dpad_size, left_center[1] - self.dpad_size), self.dpad_color,
                      left_thickness)
        cv2.rectangle(frame, (right_center[0] - self.dpad_size, right_center[1] + self.dpad_size),
                      (right_center[0] + self.dpad_size, right_center[1] - self.dpad_size), self.dpad_color,
                      right_thickness)
        return frame


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
        self.z_button = Button("Z", 20)
        self.joystick = Joystick(40)
        self.dpad = DpadVisualizer(10, 20)

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

        offset_y += 50
        frame = self.z_button.draw_button(frame, (
            self.y_button.button_radius + offset_x, h - self.a_button.button_radius - offset_y),
                                          controller_state.z_pressed())

        offset_y += 50
        frame = self.l_button.draw_button(frame, (
            self.y_button.button_radius + offset_x, h - self.a_button.button_radius - offset_y),
                                          controller_state.l_pressed())

        frame = self.dpad.draw_dpad(frame, (w - 50, 100), controller_state.dpad_up_pressed(),
                                    controller_state.dpad_down_pressed(), controller_state.dpad_left_pressed(),
                                    controller_state.dpad_right_pressed())

        return frame
