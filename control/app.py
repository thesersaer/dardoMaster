

class App:
    def __init__(self):
        self._number_of_frames = 3
        self._frame_index = 0

    def next_button_event(self):
        if self._frame_index < self._number_of_frames - 1:
            self._frame_index += 1

    def back_button_event(self):
        if self._frame_index > 0:
            self._frame_index -= 1

    @property
    def frame_index(self):
        return self._frame_index
