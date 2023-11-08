import typing

import model.definitions
import model.throw as th
import model.score as sc


class Player:
    def __init__(self, name: str, score_system: typing.Type[sc.Score]):
        self.name = name
        self._penalty_rounds = 0
        self._throws = 3
        self._throw_log: typing.List[th.Throw] = []

        self.score = score_system(self)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name and self.throw_log == other.throw_log and self.score == other.score

    def __hash__(self):
        return hash(self.name)

    def reset_player(self):
        self._penalty_rounds = 0
        self._throws = 3
        self._throw_log = []
        self.score.reset_score()

    @property
    def throws(self):
        return self._throws

    @property
    def throw_log(self):
        return self._throw_log

    def no_penalty(self):
        return self._penalty_rounds == 0

    def subtract_penalty_turn(self):
        self._penalty_rounds -= 1

    def add_penalty_turn(self):
        self._penalty_rounds += 1

    def revoke_penalty(self):
        self._penalty_rounds = 0

    def has_thrown(self):
        return self._throws < 3

    def has_throws_left(self):
        return self._throws > 0

    def reset_throws(self):
        if not self.has_throws_left():
            self._throws = 3
            return True
        return False

    def add_throw(self, score: typing.Union[str, int], modifier: int = 1, valid: bool = True):
        if self.has_throws_left() and self.no_penalty():
            throw = th.Throw(score, modifier, valid)
            if throw.foul:
                self._penalty_rounds += model.definitions.foul_penalty_turns
            self._throw_log.append(throw)
            self._throws -= 1
            return True
        return False

    def undo_throw(self):
        if self.has_thrown() and self._throw_log:
            throw = self._throw_log.pop()
            if throw.foul:
                self._penalty_rounds -= model.definitions.foul_penalty_turns
            self._throws += 1
            return throw
        return False

    def update_score(self, mid_callback: typing.Callable = None, mid_callback_args = None):
        self.score.update(mid_callback, mid_callback_args)
