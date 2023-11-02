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
    def __init__(self, rules: CricketRules, name: str = 'Player'):
        super(CricketPlayer, self).__init__(rules, name)

        self.numbers = {
            key: -3 for key in definitions.cricket_scoring_numbers
        }


class Rules:
    @staticmethod
    def get_player_score(player: Player):
        pass


class CricketRules(Rules):

    """
    @staticmethod
    def get_player_score(player: CricketPlayer):
        throw = player.dart_log[-1]
        if throw.score in definitions.cricket_scoring_numbers:
            if player.numbers[throw.score] < 3:
                number_total = player.numbers[throw.score] + throw.modifier
                if number_total <= 3:
                    player.numbers[throw.score] = number_total
                else:
                    player.numbers[throw.score] = 3
                    player.score += (number_total - 3) * throw.score
            else:
                player.score += throw.score * throw.modifier
    """

    @staticmethod
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


class Game:
    def __init__(self, players: typing.List[Player]):
        self.turn = 0
        self.round = 0
        self.players: typing.List[Player] = players

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

    def advance_play(self):
        player = self.players[self.turn]
        if not player.has_remaining_throws():
            if not self.next_turn():
                if not self.next_round():
                    return False
                else:
                    self.reset_throw_count()

        player = self.players[self.turn]
        if player.has_penalty():
            player.penalty_rounds -= 1
            player.throws = 0
            self.advance_play()
        return True

    #TODO: Add method to undo self.advance_play going back the necessary turns/rounds if any penalties considered
    def undo_play(self):
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
