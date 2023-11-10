import model.gamemanager
import model.player
import model.score


class App:
    def __init__(self):
        self._number_of_frames = 3
        self._frame_index = 0

        self.game_manager = None

    def next_button_event(self):
        if self._frame_index < self._number_of_frames - 1:
            self._frame_index += 1


    def back_button_event(self):
        if self._frame_index > 0:
            self._frame_index -= 1

    @property
    def frame_index(self):
        return self._frame_index

    def start_game(self, player_names):
        if not self.game_manager:
            player_list = [model.player.Player(name, model.score.CricketScore) for name in player_names]
            game = model.gamemanager.gm.Game(player_list)
            self.game_manager = model.gamemanager.GameManager(game)
            self.game_manager.start_game()

    def forfeit_game(self):
        if self.game_manager:
            self.game_manager = None