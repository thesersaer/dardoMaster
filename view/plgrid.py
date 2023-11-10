import customtkinter as ctk
import basicf
import control.plgrid


class PlayerGrid(basicf.AppFrame):
    def __init__(self, root, controller: control.plgrid.PlayerGrid):
        super(PlayerGrid, self).__init__(root)

        self._ctrl = controller
        self.frame = ctk.CTkFrame(root, fg_color='transparent')

        for index in range(self._ctrl.ROWS + 1):
            self.frame.rowconfigure(index, weight=1)

        for index in range(self._ctrl.COLS):
            self.frame.columnconfigure(index, weight=1)

        self.grid_cells = []

        for ii_rows in range(self._ctrl.ROWS + 1):
            row_list = []
            for jj_cols in range(self._ctrl.COLS):
                row_list.append(PlayerGridCell(self.frame, ii_rows, jj_cols))
            self.grid_cells.append(row_list)

    def pack_grid(self):
        for ii_rows in range(self._ctrl.ROWS + 1):
            for jj_cols in range(self._ctrl.COLS):
                self.grid_cells[ii_rows][jj_cols].pack_cell()

    def update_grid(self):
        for ii_rows in range(self._ctrl.ROWS + 1):
            for jj_cols in range(self._ctrl.COLS):
                value = self._ctrl.get_grid_value(ii_rows, jj_cols)
                self.grid_cells[ii_rows][jj_cols].update_value(value)

    def pack_frame(self, **kwargs):
        self._ctrl.init_fill_grid()
        self.pack_grid()
        self.update_grid()
        basicf.AppFrame.pack_frame(self, **kwargs)


class PlayerGridCell(basicf.GridCell):
    def __init__(self, root, row: int, col: int, value: str = 'bar'):
        super().__init__(root, row, col)

        self.value = value
        self.label = ctk.CTkLabel(self.frame, text=value, font=('', 20))

        self.label.pack(expand=ctk.YES, fill=ctk.BOTH, padx=5, pady=5)

    def update_value(self, value):
        self.value = value
        self.label.configure(text=value)


if __name__ == '__main__':
    basicf.test_frame(PlayerGrid, control.plgrid.PlayerGrid)
