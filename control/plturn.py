import control.plgrid

class PlayerTurn(control.plgrid.PlayerGrid):
    def __init__(self):
        super().__init__()

        self.selected_modifier = 1
        self.throws = []

    def set_modifier(self, modifier: int):
        self.selected_modifier = modifier

    def add_throw(self, score):
        if len(self.throws) < 3:
            self.throws.append((score, self.selected_modifier))

    def undo_throw(self):
        if self.throws:
            self.throws.pop()