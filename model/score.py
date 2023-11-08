import typing

import model.definitions


class Score:
    def __init__(self, player):
        self._player = player

        self._score = 0

    def __eq__(self, other):
        if isinstance(other, Score):
            return self.get == other.get

    def reset_score(self):
        self._score = 0

    @property
    def get(self):
        return self._score

    def _update_score(self):
        pass

    def update(self, mid_callback: typing.Callable = None, mid_callback_args =  None):
        self._update_score()


class CricketScore(Score):
    def __init__(self, player):
        super().__init__(player)

        self._numbers = {
            key: -3 for key in model.definitions.cricket_scoring_numbers
        }

    def __eq__(self, other):
        if isinstance(other, CricketScore):
            return self.get == other.get and self._numbers == other._numbers

    @property
    def numbers(self):
        return self._numbers

    def has_all_numbers(self):
        for value in self._numbers.values():
            if value < 0:
                return False
        return True

    def open_numbers(self):
        return [number for number, value in self._numbers.items() if value >= 0]

    def reset_score(self):
        self._score = 0
        self._numbers = {
            key: -3 for key in model.definitions.cricket_scoring_numbers
        }

    def _update_score(self):
        score = 0

        for throw in self._player.throw_log:
            if throw.score in model.definitions.cricket_scoring_numbers and throw.valid:
                if isinstance(throw.valid, tuple):
                    score += throw.score * throw.valid[1]
                else:
                    score += throw.score * throw.modifier

        self._score = score

    def _update_numbers(self):
        numbers = {
            key: -3 for key in model.definitions.cricket_scoring_numbers
        }

        for throw in self._player.throw_log:
            if throw.score in model.definitions.cricket_scoring_numbers:
                numbers[throw.score] += throw.modifier

        self._numbers = numbers

    def update(self, mid_callback: typing.Callable = None, mid_callback_args: typing.Tuple =  None):
        self._update_numbers()
        if mid_callback is not None:
            if mid_callback_args is not None:
                mid_callback(*mid_callback_args)
            else:
                mid_callback()
        self._update_score()
