from control.plselect import PlayerSelection


class PlayerNames(PlayerSelection):
    def __init__(self):
        super(PlayerNames, self).__init__()

        self._player_names = [''] * self.max_players

    def set_player_name(self, name: str, index: int):
        self._player_names[index] = name

    @property
    def player_names(self):
        return self._player_names
