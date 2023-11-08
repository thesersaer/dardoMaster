import typing
import model.player as pl
import model.definitions as mdef

class Game:
    def __init__(self, player_list: typing.List[pl.Player]):
        self.turn = 0
        self.round = 0

        self.player_list: typing.List[pl.Player] = player_list
        self._winner: typing.Set[pl.Player] = set()

    @property
    def winner(self):
        return self._winner

    @property
    def current_player(self):
        return self.player_list[self.turn]

    def next(self):
        if self.turn < len(self.player_list) - 1:
            self.turn += 1
        else:
            self.turn = 0
            self.round += 1
            self.reset_player_throws()

    def back(self):
        if self.turn > 0:
            self.turn -= 1
        else:
            if self.round > 0:
                self.turn = len(self.player_list) - 1
                self.round -= 1

    def add_player_throw(self, score: typing.Union[str, int], modifier: int = 1, valid: bool = True):
        if self.current_player.add_throw(score, modifier, valid):
            self.update_winner()
            return True
        return False

    def undo_player_throw(self):
        if self.current_player.undo_throw():
            self.current_player.update_score()
            self.update_winner()
            return True
        return False

    def reset_player_throws(self):
        for player in self.player_list:
            player.reset_throws()

    def reset_game(self):
        self.turn = 0
        self.round = 0
        self._winner = set()

        for player in self.player_list:
            player.reset_player()

    def update_winner(self):
        pass


class CricketGame(Game):
    def __init__(self, player_list: typing.List[pl.Player]):
        super().__init__(player_list)

        self._closed_numbers = set()
        self.player_open_numbers = {
            key: [] for key in mdef.cricket_scoring_numbers
        }

    def reset_game(self):
        self.turn = 0
        self.round = 0
        self._winner = set()
        self._closed_numbers = set()
        self.reset_player_open_numbers()

    def reset_player_open_numbers(self):
        self.player_open_numbers = {
            key: [] for key in mdef.cricket_scoring_numbers
        }

    def update_winner(self):
        top_score = 0
        has_top_score = []
        has_all_numbers = []
        for player in self.player_list:
            if player.score.get > top_score:
                top_score = player.score.get
                has_top_score = [player,]
            elif player.score.get == top_score:
                has_top_score.append(player)
            if player.score.has_all_numbers():
                has_all_numbers.append(player)

        self._winner = set(*[has_top_score]).intersection(set(*[has_all_numbers]))

    def update_available_numbers(self):
        self._closed_numbers = set()
        for number in self.player_open_numbers:
            if self.player_open_numbers[number] == self.player_list:
                self._closed_numbers.add(number)

    def update_player_open_numbers(self):
        self.reset_player_open_numbers()
        for player in self.player_list:
            for number in player.score.open_numbers():
                self.player_open_numbers[number].append(player)
        self.update_available_numbers()

    def last_to_open(self, number: int, player):
        players_with_open_number = self.player_open_numbers[number]
        if player not in players_with_open_number:
            player_list_without_player = [ii_player for ii_player in self.player_list if ii_player != player]
            if player_list_without_player == players_with_open_number:
                return True
        return False

    def add_player_throw(self, score: typing.Union[str, int], modifier: int = 1, __valid: bool = True):
        valid = False

        if score in mdef.cricket_scoring_numbers:
            if score not in self._closed_numbers:
                score_value = self.current_player.score.numbers[score]
                if score_value < 0:
                    remainder = score_value + modifier
                    if remainder > 0:
                        if self.last_to_open(score, self.current_player):
                            valid = False
                        else:
                            valid = True, remainder
                    else:
                        valid = False
                else:
                    valid = True

        if self.current_player.add_throw(score, modifier, valid):
            self.current_player.update_score(self.update_player_open_numbers)
            self.update_winner()
            return True
        return False

    def undo_player_throw(self):
        if self.current_player.undo_throw():
            self.current_player.update_score(self.update_player_open_numbers)
            self.update_winner()
            return True
        return False