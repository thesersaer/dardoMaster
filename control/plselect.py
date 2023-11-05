from control.controls import AppController
from model import definitions


class PlayerSelection(AppController):
    min_players = definitions.min_players
    max_players = definitions.max_players

    def __init__(self):

        self._number_of_players = 2

    def set_players(self, value: int):
        if value in range(self.min_players, self.max_players + 1, 1):
            self._number_of_players = value
            pass

    @property
    def number_of_players(self):
        return self._number_of_players
