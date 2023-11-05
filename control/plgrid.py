import copy
from control.plnames import PlayerNames
from model import definitions


class PlayerGrid(PlayerNames):
    ROW_HEADER = definitions.cricket_row_header

    COLS = len(ROW_HEADER)
    ROWS = definitions.max_players

    def __init__(self):
        super().__init__()

        self.grid_cells = {
            'H': {
                key: key for key in self.ROW_HEADER
            }
        }

        for ii in range(self.ROWS):
            self.grid_cells[ii] = {
                key: '' for key in self.ROW_HEADER
            }

        self.empty_grid_cells = copy.deepcopy(self.grid_cells)

    def init_fill_grid(self):
        self.grid_cells = copy.deepcopy(self.empty_grid_cells)
        for index in range(self._number_of_players):
            for key in self.grid_cells[index].keys():
                if key == 'J':
                    self.grid_cells[index][key] = self._player_names[index]
                else:
                    self.grid_cells[index][key] = '0'

    def get_grid_value(self, row: int, col: int):
        col_key = self.ROW_HEADER[col]
        if row == 0:
            row = 'H'
        else:
            row -= 1

        value = self.grid_cells[row][col_key]
        if col > 1:
            if value == '0':
                return definitions.cricket_number_0_str
            elif value == '1':
                return definitions.cricket_number_1_str
            elif value == '2':
                return definitions.cricket_number_2_str
            elif value == '3':
                return definitions.cricket_number_3_str

        return value


def main():
    plgrid = PlayerGrid()
    plgrid.set_player_name('Sergio', 0)
    plgrid.set_player_name('David', 1)
    plgrid.init_fill_grid()


if __name__ == '__main__':
    main()

    input('END')
