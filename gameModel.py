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


class Player:
    def __init__(self, rules: Rules, name: str = 'Player'):
        self.rules = rules
        self.name = name
        self.penalty_rounds = 0
        self.throws = 3
        self.score = 0
        self.dart_log = []

    def add_throw(self, throw: Throw):
        if self.throws > 0:
            self.dart_log.append(throw)
            if throw.foul:
                self.penalty_rounds += definitions.foul_penalty_rounds
            elif not throw.out:
                self.rules.get_player_score(self)
            self.throws -= 1
            return True
        else:
            return False


class CricketPlayer(Player):
    def __init__(self, rules: CricketRules, name: str = 'Player'):
        super(CricketPlayer, self).__init__(rules, name)

        self.numbers = {
            key: 0 for key in definitions.cricket_scoring_numbers
        }


class Rules:
    @staticmethod
    def get_player_score(player: Player):
        pass


class CricketRules(Rules):

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


class Game:
    def __init__(self, players: typing.List[Player]):
        self.players: typing.List[Player] = players
        self.turn = 0
        self.round = 0

    def next_round(self):
        for player in self.players:
            player.throws = 3
        self.turn = 0
        self.round += 1

    def next_turn(self):
        if self.turn >= len(self.players) - 1:
            self.next_round()
        else:
            self.turn += 1
        if self.players[self.turn].penalty_rounds > 0:
            self.players[self.turn].penalty_rounds -= 1
            self.next_turn()

    def add_throw(self, throw: Throw):
        if not self.players[self.turn].add_throw(throw):
            self.next_turn()
            self.add_throw(throw)


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

    for throw in tl:
        game.add_throw(throw)

    input('END')


if __name__ == '__main__':
    main()
