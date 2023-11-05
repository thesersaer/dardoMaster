import os
import model.gamemodel


class CricketConsole:
    def __init__(self, game_manager: model.gamemodel.GameManager):
        self.game_manager = game_manager

    def update(self):
        lines = []
        lines += self.scoreboard()
        lines += self.header()
        lines += self.player_info()

        os.system('cls')
        for line in lines:
            print(line)

    def announce_winners(self):
        os.system('cls')
        print(f'GANADOR: {[self.game_manager.game.player_list[winner].name for winner in self.game_manager.winners]}')

    def header(self):
        lines = [f'RONDA {self.game_manager.game.round}',
                 f'TURNO de {self.game_manager.game.player_list[self.game_manager.game.turn].name}\n']
        return lines

    def scoreboard(self):
        lines = []
        for player in self.game_manager.game.player_list:
            line = f'{player.name} ({player.score}): {player.numbers}'
            lines.append(line)
        return lines

    def player_info(self):
        lines = []
        player = self.game_manager.game.player_list[self.game_manager.game.turn]
        for ii_throw in range(player.throws):
            lines.append(' - ')

        for jj_throw in range(3 - player.throws):
            lines.append(f'{player.throw_log[- (jj_throw + 1)].score} x {player.throw_log[- (jj_throw + 1)].modifier}')

        return lines

    def console_entry(self):
        entry = input('\\>')
        if entry == 'undo':
            self.game_manager.undo_throw()
        elif entry == 'undo turn':
            self.game_manager.undo_turn()
        elif entry == 'undo round':
            self.game_manager.undo_round()
        else:
            if self.game_manager.game.player_list[self.game_manager.game.turn].throws > 0:
                if not entry == 'f' and not entry == 'o':
                    throw_info = entry.split(',')
                    try:
                        modif = int(throw_info[1])
                    except IndexError:
                        modif = 1
                    throw = model.gamemodel.Throw(int(throw_info[0]), modif)
                else:
                    throw = model.gamemodel.Throw(entry)

                if self.game_manager.add_throw(throw):
                    self.game_manager.next_turn()
            else:
                self.game_manager.next_turn()
                self.update()

    def init(self):
        self.game_manager.start_game()

        while self.game_manager.started:
            self.update()
            self.console_entry()

        self.announce_winners()


if __name__ == '__main__':
    import sys

    number_of_players = int(sys.argv[1])

    player_list = []
    for ii_player in range(number_of_players):
        player_list.append(model.gamemodel.CricketPlayer(sys.argv[2 + ii_player]))

    game = model.gamemodel.Game(player_list, model.gamemodel.CricketScore)

    manager = model.gamemodel.GameManager(game)

    console = CricketConsole(manager)

    console.init()
