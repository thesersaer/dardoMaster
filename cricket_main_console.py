import os
import model.gamemanager as gmm


class CricketConsole:
    def __init__(self, game_manager: gmm.GameManager):
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
        print(f'GANADOR: {[winner.name for winner in self.game_manager.winners]}')

    def header(self):
        lines = [f'RONDA {self.game_manager.game.round}',
                 f'TURNO de {self.game_manager.game.player_list[self.game_manager.game.turn].name}\n']
        return lines

    def scoreboard(self):
        lines = []
        for player in self.game_manager.game.player_list:
            line = f'{player.name} ({player.score.get}): {player.score.numbers}'
            lines.append(line)
        return lines

    def player_info(self):
        lines = []
        player = self.game_manager.game.player_list[self.game_manager.game.turn]
        for ii_throw in range(player.throws):
            lines.append(' - ')

        for jj_throw in range(3 - player.throws):
            throw = player.throw_log[- (jj_throw + 1)]
            if throw.out:
                lines.append('Fuera')
            elif throw.foul:
                lines.append('Falta')
            else:
                lines.append(f'{throw.score} x {throw.modifier}')

        return lines

    def console_entry(self):
        entry = input('\\>')
        if entry == 'undo':
            if not self.game_manager.undo_throw():
                self.game_manager.back()
        else:
            parsed_entry = entry.split(',')
            if len(parsed_entry) > 1:
                score = int(parsed_entry[0])
                modifier = int(parsed_entry[1])
                if modifier >= 3:
                    if score == 25:
                        modifier = 2
                    else:
                        modifier = 3

                self.game_manager.add_throw(score, modifier)
            else:
                score = parsed_entry[0]
                try:
                    score = int(parsed_entry[0])
                except ValueError:
                    pass
                finally:
                    if score == 'o' or score == 'f' or isinstance(score, int):
                        self.game_manager.add_throw(score)
                    else:
                        self.game_manager.next()

        if self.game_manager.winners:
            self.game_manager.end_game()


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
        player_list.append(gmm.gm.pl.Player(sys.argv[2 + ii_player], gmm.gm.pl.sc.CricketScore))

    game = gmm.gm.CricketGame(player_list)

    manager = gmm.GameManager(game)

    console = CricketConsole(manager)

    console.init()
