import typing
import customtkinter as ctk

import basicf
import control.plturn
import model.definitions


class PlayerTurn(basicf.AppFrame):
    def __init__(self, root, controller: control.plturn.PlayerTurn):
        super().__init__(root)

        self._ctrl = controller

        self.selected_color = '#029CFF'
        self.unselected_color = '#1F6AA5'
        self.disabled_color = '#154870'

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=3)
        self.frame.rowconfigure(2, weight=3)
        self.frame.rowconfigure(3, weight=3)
        self.frame.rowconfigure(4, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.round_label = ctk.CTkLabel(self.frame, text='RONDA: 0', font=('', 18))
        self.round_label.grid(row=0, column=0, padx=10, pady=5)

        self.turn_label = ctk.CTkLabel(self.frame, text='TURNO: ', font=('', 18))
        self.turn_label.grid(row=0, column=1, padx=10, pady=5)

        self.numbers_frame = ctk.CTkFrame(self.frame, fg_color='transparent')
        for row in range(4):
            self.numbers_frame.rowconfigure(row, weight=1)
        for col in range(7):
            self.numbers_frame.columnconfigure(col, weight=1)

        self.number_cells = [
            [NumberButtonCell(self.numbers_frame,
                              row,
                              col,
                              model.definitions.dartboard_numbers[col + row*7],
                              self.on_number_button_click) for col in range(7)] for row in range(3)
        ]

        self.out_button = ctk.CTkButton(self.numbers_frame, text='Fuera', command=self.on_out_button_click, height=30, width=110)
        self.out_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        self.foul_button = ctk.CTkButton(self.numbers_frame, text='Falta', command=self.on_foul_button_click, height=30, width=110)
        self.foul_button.grid(row=7, column=4, columnspan=3, padx=5, pady=5)

        self.pack_number_cells()

        self.numbers_frame.grid(row=1, columnspan=2, padx=10, pady=5)

        self.modifier_frame = ctk.CTkFrame(self.frame, fg_color='transparent')

        for row in range(3):
            self.modifier_frame.rowconfigure(row, weight=1)

        modifier_1_button = ctk.CTkButton(self.modifier_frame, text='x1', command=self.on_modifier1_button_click)
        modifier_2_button = ctk.CTkButton(self.modifier_frame, text='x2', command=self.on_modifier2_button_click)
        modifier_3_button = ctk.CTkButton(self.modifier_frame, text='x3', command=self.on_modifier3_button_click)

        self.modifier_buttons = [modifier_1_button, modifier_2_button, modifier_3_button]

        for row, button in enumerate(self.modifier_buttons):
            button.grid(row=row, padx=10, pady=5)
        self.update_modifier_buttons()

        self.modifier_frame.grid(row=2, columnspan=2, padx=10, pady=5)

        self.throws_frame = ctk.CTkFrame(self.frame)

        self.throws_frame.grid(row=3, columnspan=2, padx=10, pady=10)

        self.throw_labels = [ctk.CTkLabel(self.throws_frame, text='-') for _ in range(3)]

        for index, label in enumerate(self.throw_labels):
            label.grid(row=0, column=index, padx=5, pady=5)

        self.progress_frame = ctk.CTkFrame(self.frame, fg_color='transparent')

        self.next_button = ctk.CTkButton(self.progress_frame, text='>', command=self.on_next_button_click)
        self.undo_button = ctk.CTkButton(self.progress_frame, text='<', command=self.on_undo_button_click)
        self.next_button.pack(side=ctk.RIGHT, padx=5, pady=5)
        self.undo_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.progress_frame.grid(row=4, columnspan=2, padx=10, pady=5)

        self.frame._canvas.bind('<KeyPress-Control_L>',self.on_ctrl_press_event)
        self.frame._canvas.bind('<KeyRelease-Control_L>', self.on_ctrl_release_event)

        self.frame._canvas.bind('<KeyPress-Shift_L>', self.on_shift_press_event)
        self.frame._canvas.bind('<KeyRelease-Shift_L>', self.on_shift_release_event)

        self.frame._canvas.bind('<BackSpace>', self.on_undo_button_click)
        self.frame._canvas.bind('<Return>', self.on_next_button_click)

        self.frame._canvas.focus_set()

        self.modifier_sequence = 0

    def pack_number_cells(self):
        for number_cell_row in self.number_cells:
            for number_cell in number_cell_row:
                number_cell.pack_cell()

    def on_ctrl_press_event(self, event):
        if not self.modifier_sequence & model.definitions.ctrl_mask:
            self.modifier_sequence += model.definitions.ctrl_mask
        self.on_modifier_sequence_event()

    def on_ctrl_release_event(self, event):
        if self.modifier_sequence & model.definitions.ctrl_mask:
            self.modifier_sequence -= model.definitions.ctrl_mask
        self.on_modifier_sequence_event()

    def on_shift_press_event(self, event):
        if not self.modifier_sequence & model.definitions.shift_mask:
            self.modifier_sequence += model.definitions.shift_mask
        self.on_modifier_sequence_event()

    def on_shift_release_event(self, event):
        if self.modifier_sequence & model.definitions.shift_mask:
            self.modifier_sequence -= model.definitions.shift_mask
        self.on_modifier_sequence_event()

    def on_modifier_sequence_event(self):
        if self.modifier_sequence & model.definitions.ctrl_mask and self.modifier_sequence & model.definitions.shift_mask:
            self.on_modifier3_button_click()
        elif self.modifier_sequence & model.definitions.ctrl_mask:
            self.on_modifier2_button_click()
        else:
            self.on_modifier1_button_click()

    def on_modifier1_button_click(self):
        self._ctrl.set_modifier(1)
        self.update_modifier_buttons()
        self.update_number_buttons()

    def on_modifier2_button_click(self):
        self._ctrl.set_modifier(2)
        self.update_modifier_buttons()
        self.update_number_buttons()

    def on_modifier3_button_click(self):
        self._ctrl.set_modifier(3)
        self.update_modifier_buttons()
        self.update_number_buttons()

    def on_number_button_click(self, score):
        self._ctrl.add_throw(score)
        self.update_throws()
        if self.modifier_sequence == 0:
            self.on_modifier1_button_click()

    def on_out_button_click(self):
        self.on_number_button_click('o')

    def on_foul_button_click(self):
        self.on_number_button_click('f')

    def on_next_button_click(self, event=None):
        print('>')

    def on_undo_button_click(self, event=None):
        print('<')
        self._ctrl.undo_throw()
        self.update_throws()

    def update_modifier_buttons(self):
        selected_modifier = self._ctrl.selected_modifier
        for button in self.modifier_buttons:
            button.configure(fg_color=self.unselected_color)
        self.modifier_buttons[selected_modifier - 1].configure(fg_color=self.selected_color)

    def update_number_buttons(self):
        selected_modifier = self._ctrl.selected_modifier
        if selected_modifier == 3:
            self.update_button_state(self.out_button, 'disabled')
            self.update_button_state(self.foul_button, 'disabled')
            self.update_button_state(self.number_cells[-1][-1].number_button, 'disabled')
        elif selected_modifier == 2:
            self.update_button_state(self.out_button, 'disabled')
            self.update_button_state(self.foul_button, 'disabled')
            self.update_button_state(self.number_cells[-1][-1].number_button, 'normal')
        else:
            self.update_button_state(self.out_button, 'normal')
            self.update_button_state(self.foul_button, 'normal')
            self.update_button_state(self.number_cells[-1][-1].number_button, 'normal')

    def update_button_state(self, button, state):
        if state == 'normal':
            button.configure(state='normal', fg_color=self.unselected_color)
        elif state == 'disabled':
            button.configure(state='disabled', fg_color=self.disabled_color)

    def update_throws(self):
        for index, label in enumerate(self.throw_labels):
            try:
                score = self._ctrl.throws[index][0]
                if score == 'o':
                    label.configure(text='O')
                elif score == 'f':
                    label.configure(text='F')
                else:
                    label.configure(text=f'{score}x{self._ctrl.throws[index][1]}')
            except IndexError:
                label.configure(text='-')


class NumberButtonCell(basicf.GridCell):
    def __init__(self, root, row: int, col: int, button_text: str, callback: typing.Callable):
        super().__init__(root, row, col)

        self.callback = callback

        self.number_button = ctk.CTkButton(self.frame, text=button_text, command=self.on_number_button_click, width=30, height=30)
        self.number_button.pack(padx=5, pady=5)

    def on_number_button_click(self):
        self.callback(model.definitions.dartboard_numbers[self.col + self.row * 7])


if __name__ == '__main__':
    basicf.test_frame(PlayerTurn, control.plturn.PlayerTurn)
