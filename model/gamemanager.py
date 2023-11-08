import typing
import model.game as gm


class GameManager:
    def __init__(self, game: gm.Game):
        self.game = game

        self._started = False
        self.turns_skipped = 0
        self._winners: typing.Set[gm.pl.Player] = set()

    @property
    def winners(self):
        return self._winners

    @property
    def started(self):
        return self._started

    def start_game(self):
        if not self._started:
            self.game.reset_game()
            self._started = True
            return True
        return False

    def end_game(self):
        if self._started:
            self._started = False
            return True
        return False

    def update_winners(self):
        self._winners = self.game.winner

    def add_throw(self, score: typing.Union[str, int], modifier: int = 1):
        if self.game.add_player_throw(score, modifier):
            self.update_winners()
            return True
        return False

    def undo_throw(self):
        if self.game.undo_player_throw():
            self.update_winners()
            return True
        return False

    def next(self):
        if not self.game.current_player.has_throws_left():
            self.game.next()
            while not self.game.current_player.no_penalty():
                self.game.current_player.subtract_penalty_turn()
                self.turns_skipped += 1
                self.game.next()
            return True
        return False

    def back(self):
        if not self.game.current_player.has_thrown():
            self.game.back()
            while self.game.current_player.has_throws_left() and self.turns_skipped > 0:
                self.game.current_player.add_penalty_turn()
                self.turns_skipped -= 1
                self.game.back()
            return True
        return False

    def reset_game(self):
        self.game.reset_game()
        self._started = False
        self.turns_skipped = 0
        self._winners = set()