from __future__ import annotations
import typing
import definitions


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
    def __init__(self, rules: Rules, name: str = 'Player'):
        self.rules = rules
        self.name = name
        self.penalty_rounds = 0
        self.throws = 3
        self.score = 0
        self.throw_log: typing.List[Throw] = []

    def has_penalty(self):
        return self.penalty_rounds > 0

    def has_remaining_throws(self):
        return self.throws > 0

    def add_throw(self, throw: Throw):
        if self.throws > 0:
            self.throw_log.append(throw)
            if throw.foul:
                self.penalty_rounds += definitions.foul_penalty_rounds
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
        key: True for key in definitions.cricket_scoring_numbers
    }

    def __init__(self, rules: CricketRules, name: str = 'Player'):
        super(CricketPlayer, self).__init__(rules, name)

        self.numbers = {
            key: -3 for key in definitions.cricket_scoring_numbers
        }

    @staticmethod
    def reset_available_numbers():
        for number in CricketPlayer.available_numbers:
            CricketPlayer.available_numbers[number] = True


class Rules:
    @staticmethod
    def get_player_score(player: Player):
        pass


class CricketRules(Rules):

    @staticmethod
    # TODO: Block scores once number is not available
    def get_player_score(player: CricketPlayer):
        numbers_buffer = player.numbers.copy()
        numbers_buffer = dict.fromkeys(numbers_buffer, -3)
        score_buffer = 0

        for throw in player.throw_log:
            if throw.score in definitions.cricket_scoring_numbers:
                numbers_buffer[throw.score] += throw.modifier

        for key, value in numbers_buffer.items():
            if value > 0:
                score_buffer += key * value

        player.numbers = numbers_buffer
        player.score = score_buffer

    @staticmethod
    def check_winner(player_list: typing.List[CricketPlayer]):
        winners = []
        scores_maximum = max([player.score for player in player_list])
        for index, player in enumerate(player_list):
            score_condition = player.score == scores_maximum
            numbers_condition = all([value >= 0 for value in player.numbers])
            if score_condition and numbers_condition:
                winners.append(index)
        return winners

    @staticmethod
    def check_available_numbers(player_list: typing.List[CricketPlayer]):
        for number in definitions.cricket_scoring_numbers:
            closed_number = [player.numbers[number] >= 0 for player in player_list]
            if all(closed_number):
                CricketPlayer.available_numbers[number] = False


class Score:
    pass

    def check_winner(self):
        pass

    def update_player_score(self, player_index: int):
        pass


class CricketScore(Score):
    def __init__(self, player_list: typing.List[CricketPlayer]):
        self.player_list = player_list

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
            return False

    def _check_closed_numbers(self):
        for number in definitions.cricket_scoring_numbers:
            for player in self.player_list:
                if player.numbers[number] < 0:
                    break
            else:
                if number not in self.closed_numbers:
                    self.closed_numbers.add(number)

    def update_player_numbers_from_last_throw(self, player_index: int):
        player = self.player_list[player_index]
        throw = player.throw_log[-1]
        if throw.score in definitions.cricket_scoring_numbers:
            if player.numbers[throw.score] < 0:
                player.numbers[throw.score] += 1
            else:
                if throw.score not in self.closed_numbers:
                    player.numbers[throw.score] += 1

    def update_player_score(self, player_index: int):
        player = self.player_list[player_index]
        score_buffer = 0
        for key, value in player.numbers.items():
            if value > 0:
                score_buffer += key * value
        player.score = score_buffer


class Game:
    def __init__(self, players: typing.List[Player]):
        self.turn = 0
        self.round = 0
        self.players: typing.List[Player] = players
        self.turns_skipped = 0

    def add_throw(self, throw: Throw, player_position: int):
        player = self.players[player_position]
        if player.add_throw(throw):
            if not throw.out and not throw.foul:
                player.rules.get_player_score(player)
            return True
        return False

    def remove_throw(self, throw: Throw, player_position: int):
        player = self.players[player_position]
        if player.remove_throw(throw):
            if not throw.out and not throw.foul:
                player.rules.get_player_score(player)
            return True
        return False

    def undo_throw(self):
        player = self.players[self.turn]
        throw = player.throw_log[-1]
        if player.undo_throw():
            if not throw.out and not throw.foul:
                player.rules.get_player_score(player)
            return True
        return False

    def reset_throw_count(self, player=None):
        if player is None:
            for player in self.players:
                player.throws = 3
        else:
            if isinstance(player, int):
                self.players[player].throws = 3

    def next_turn(self):
        if self.turn < len(self.players) - 1:
            self.turn += 1
            return True
        return False

    def prev_turn(self):
        if self.turn > 0:
            self.turn -= 0
            return True
        return False

    def undo_turn(self):
        player = self.players[self.turn]
        if player.throws < 3:
            for _ in range(3 - player.throws):
                self.undo_throw()
            return True
        return False

    def next_round(self):
        if self.turn == len(self.players) - 1:
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

    def start_game(self):
        pass


def main():
    rules = CricketRules()
    p1 = CricketPlayer(rules, 'P1')
    p2 = CricketPlayer(rules, 'P2')

    game = Game([p1, p2])
    t1 = Throw(15, 1)
    t2 = Throw('f')
    t3 = Throw(15, 3)

    t4 = Throw(17, 2)
    t5 = Throw('o')
    t6 = Throw(25)

    t7 = Throw(25, 2)
    t8 = Throw('f')
    t9 = Throw(15, 3)

    t10 = Throw(16, 2)

    tl = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    game.add_throw(t1)
    game.add_throw(t2)
    game.add_throw(t3)

    game.advance_play()
    game.add_throw(t2)
    game.add_throw(t4)
    game.add_throw(t5)

    game.advance_play()
    game.add_throw(t6)
    game.add_throw(t7)
    game.add_throw(t9)

    game.advance_play()
    game.undo_turn()

    input('END')


def main2():
    p1 = Player(CricketRules(), 'P1')
    t1 = Throw(15, 2)
    t2 = Throw(15, 2)
    t3 = Throw('f')
    t4 = Throw('f')
    t5 = Throw(17)
    p1.add_throw(t1)
    p1.add_throw(t4)
    p1.add_throw(t2)
    r = p1.remove_throw(t3)
    input('END')


if __name__ == '__main__':
    main2()
