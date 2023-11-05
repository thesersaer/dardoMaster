from __future__ import annotations
import typing
import model.definitions


class Throw:
    def __init__(self, score: typing.Union[int, str], modif=1):
        self.modifier = modif
        self.out = False
        self.foul = False

        if isinstance(score, int):
            self.score = score
        else:
            if score == 'o':
                self.score = 0
                self.out = True
            elif score == 'f':
                self.score = 0
                self.foul = True

    def __eq__(self, other: Throw):
        return self.score == other.score and self.modifier == other.modifier and self.out == other.out and \
               self.foul == other.foul


class Player:
    def __init__(self, name: str = 'Player'):
        self.name = name
        self.penalty_rounds = 0
        self.throws = 3
        self.score = 0
        self.throw_log: typing.List[Throw] = []
        self.numbers = None

    def has_penalty(self):
        return self.penalty_rounds > 0

    def has_remaining_throws(self):
        return self.throws > 0

    def add_throw(self, throw: Throw):
        if self.throws > 0:
            self.throw_log.append(throw)
            if throw.foul:
                self.penalty_rounds += model.definitions.foul_penalty_rounds
            self.throws -= 1
            return True
        return False

    def remove_throw(self, throw: Throw):
        match, r_index = self.has_throw(throw)
        if match:
            throws_done_in_turn = len(self.throw_log) % 3
            if throws_done_in_turn == 0:
                throws_done_in_turn = 3
            if throw.foul and self.penalty_rounds > 0 and - r_index <= throws_done_in_turn:
                self.penalty_rounds = 0
            self.throw_log.reverse()
            self.throw_log.remove(throw)
            self.throw_log.reverse()
            return True
        return False

    def undo_throw(self):
        if self.throws < 3:
            self.remove_throw(self.throw_log[-1])
            self.throws += 1
            return True
        return False

    def has_throw(self, throw: Throw):
        match = False
        index = None
        self.throw_log.reverse()
        try:
            index = - (self.throw_log.index(throw) + 1)
            match = True
        finally:
            self.throw_log.reverse()
            return match, index


class CricketPlayer(Player):
    available_numbers = {
        key: True for key in model.definitions.cricket_scoring_numbers
    }

    def __init__(self, name: str = 'Player'):
        super(CricketPlayer, self).__init__(name)

        self.numbers = {
            key: -3 for key in model.definitions.cricket_scoring_numbers
        }

    @staticmethod
    def reset_available_numbers():
        for number in CricketPlayer.available_numbers:
            CricketPlayer.available_numbers[number] = True

    def reset_player_numbers(self):
        for key in self.numbers:
            self.numbers[key] = -3


class Score:
    def __init__(self, player_list: typing.List[Player]):
        self.player_list = player_list

    def check_winner(self):
        pass

    def update_player_score(self, player_index: int):
        pass

    def player_update_sequence(self, player_index: int):
        pass


class CricketScore(Score):
    def __init__(self, player_list: typing.List[CricketPlayer]):
        super().__init__(player_list)
        self.player_list: typing.List[CricketPlayer] = player_list

        self.top_score = set()
        self.all_numbers_closed = set()

        self.closed_numbers = set()

    def _check_top_score(self):
        top_score = max([player.score for player in self.player_list])
        self.top_score = set()

        for player_index, player in enumerate(self.player_list):
            if player.score == top_score:
                if player_index not in self.top_score:
                    self.top_score.add(player_index)

    def _check_all_closed(self):
        for player_index, player in enumerate(self.player_list):
            for number in player.numbers.values():
                if number < 0:
                    break
            else:
                if player_index not in self.all_numbers_closed:
                    self.all_numbers_closed.add(player_index)

    def check_winner(self):
        winners = self.top_score.intersection(self.all_numbers_closed)
        if winners:
            return True, winners
        else:
            return False, []

    def _check_closed_numbers(self):
        for number in model.definitions.cricket_scoring_numbers:
            for player in self.player_list:
                if player.numbers[number] < 0:
                    break
            else:
                if number not in self.closed_numbers:
                    self.closed_numbers.add(number)

    def update_player_numbers_from_last_throw(self, player_index: int):
        player = self.player_list[player_index]
        try:
            throw = player.throw_log[-1]
            if throw.score in model.definitions.cricket_scoring_numbers:
                player_number = player.numbers[throw.score]

                if throw.score in self.closed_numbers and player_number < 0:
                    player_number_final = player_number + throw.modifier
                    if player_number_final > 0:
                        player.numbers[throw.score] = 0
                    else:
                        player.numbers[throw.score] = player_number_final

                elif throw.score not in self.closed_numbers:
                    player.numbers[throw.score] += throw.modifier

        except IndexError:
            player.reset_player_numbers()

    def update_player_score(self, player_index: int):
        player = self.player_list[player_index]
        score_buffer = 0
        for key, value in player.numbers.items():
            if value > 0:
                score_buffer += key * value
        player.score = score_buffer

    def player_update_sequence(self, player_index: int):
        self.update_player_numbers_from_last_throw(player_index)
        self.update_player_score(player_index)
        self._check_closed_numbers()
        self._check_all_closed()
        self._check_top_score()
        return self.check_winner()


class Game:
    def __init__(self, player_list: typing.List[Player], score: typing.Type[Score]):
        self.score_type = score
        self.score = score(player_list)
        self.turn = 0
        self.round = 0
        self.player_list: typing.List[Player] = player_list
        self.turns_skipped = 0
        self.winners = (False,[])

    def add_throw(self, throw: Throw, player_index: int = None):
        if player_index is None:
            player_index = self.turn
        player = self.player_list[player_index]
        if player.add_throw(throw):
            if not throw.out and not throw.foul:
                self.winners = self.score.player_update_sequence(player_index)
            return True
        return False

    def remove_throw(self, throw: Throw, player_index: int):
        player = self.player_list[player_index]
        if player.remove_throw(throw):
            if not throw.out and not throw.foul:
                self.winners = self.score.player_update_sequence(player_index)
            return True
        return False

    def undo_throw(self):
        player = self.player_list[self.turn]
        try:
            throw = player.throw_log[-1]
            if player.undo_throw():
                if not throw.out and not throw.foul:
                    self.winners = self.score.player_update_sequence(self.turn)
                return True
            return False
        except IndexError:
            return False

    def has_throws_left(self, player_index: int = None):
        if player_index is None:
            player_index = self.turn
        return self.player_list[player_index].throws > 0

    def reset_throw_count(self, player=None):
        if player is None:
            for player in self.player_list:
                player.throws = 3
        else:
            if isinstance(player, int):
                self.player_list[player].throws = 3

    def next_turn(self):
        if self.turn < len(self.player_list) - 1:
            self.turn += 1
            return True
        return False

    def prev_turn(self):
        if self.turn > 0:
            self.turn -= 0
            return True
        return False

    def undo_turn(self):
        player = self.player_list[self.turn]
        if player.throws < 3:
            for _ in range(3 - player.throws):
                self.undo_throw()
            return True
        return False

    def next_round(self):
        if self.turn == len(self.player_list) - 1:
            self.turn = 0
            self.round += 1
            return True
        return False

    def undo_round(self):
        if self.turn > 0:
            for _ in range(self.turn):
                if not self.undo_turn():
                    return False
                self.prev_turn()
            return self.undo_turn()
        return self.undo_turn()


class GameManager:
    def __init__(self, game: Game):
        self.game = game

        self.started = False
        self.winners = None

    def start_game(self):
        if not self.started:
            self.game.score = self.game.score_type(self.game.player_list)
            self.game.turn = 0
            self.game.round = 0
            self.game.turns_skipped = 0
            self.started = True

    def add_throw(self, throw: Throw):
        if self.started:
            self.game.add_throw(throw)
            if self.game.winners[0]:
                self.winners = self.game.winners[1]
                self.end_game()

    def undo_throw(self):
        if self.started:
            return self.game.undo_throw()

    def end_game(self):
        if self.started:
            self.started = False

    def next_turn(self):
        if self.started:
            if not self.game.has_throws_left():
                if not self.game.next_turn():
                    if not self.game.next_round():
                        return False
                    else:
                        self.game.reset_throw_count()

    def undo_turn(self):
        return self.game.undo_turn()

    def undo_round(self):
        return self.game.undo_round()


def main3():
    import os
    import time
    for ii in range(4):
        print(f'TEST{ii}')
        time.sleep(1)
        os.system('cls')


if __name__ == '__main__':
    main3()
