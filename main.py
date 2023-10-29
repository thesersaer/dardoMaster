from __future__ import annotations
import tkinter as tk


class PlayerSelection:
    def __init__(self, tk_main):
        self.players_frame = tk.Frame(tk_main)
        self.players_frame.columnconfigure(0)
        self.players_frame.columnconfigure(1)
        self.players_frame.rowconfigure(0)
        self.players_frame.pack()

        self.players_amount = tk.Frame(self.players_frame)

        self.amount_var = tk.IntVar(self.players_amount, value=2)

        self.radio_2 = tk.Radiobutton(self.players_amount, text='2', variable=self.amount_var, value=2,
                                      command=self.textbox_update)
        self.radio_2.pack()

        self.radio_3 = tk.Radiobutton(self.players_amount, text='3', variable=self.amount_var, value=3,
                                      command=self.textbox_update)
        self.radio_3.pack()

        self.radio_4 = tk.Radiobutton(self.players_amount, text='4', variable=self.amount_var, value=4,
                                      command=self.textbox_update)
        self.radio_4.pack()

        self.radio_5 = tk.Radiobutton(self.players_amount, text='5', variable=self.amount_var, value=5,
                                      command=self.textbox_update)
        self.radio_5.pack()

        self.players_amount.grid(row=0, column=0)

        self.players_names = tk.Frame(self.players_frame)

        self.strvar_1 = tk.StringVar(self.players_names, value='1')
        self.textbox_1 = tk.Entry(self.players_names, textvariable=self.strvar_1)

        self.strvar_2 = tk.StringVar(self.players_names, value='2')
        self.textbox_2 = tk.Entry(self.players_names, textvariable=self.strvar_2)

        self.strvar_3 = tk.StringVar(self.players_names, value='3')
        self.textbox_3 = tk.Entry(self.players_names, textvariable=self.strvar_3)

        self.strvar_4 = tk.StringVar(self.players_names, value='4')
        self.textbox_4 = tk.Entry(self.players_names, textvariable=self.strvar_4)

        self.strvar_5 = tk.StringVar(self.players_names, value='5')
        self.textbox_5 = tk.Entry(self.players_names, textvariable=self.strvar_5)

        self.textbox_list = [self.textbox_1, self.textbox_2, self.textbox_3, self.textbox_4, self.textbox_5]
        self.strvar_list = [self.strvar_1, self.strvar_2, self.strvar_3, self.strvar_4, self.strvar_5]

        self.players_names.grid(row=0, column=1)

    def textbox_update(self):
        for textbox in self.textbox_list:
            textbox.pack_forget()
        player_count = self.amount_var.get()
        for ii_pl in range(player_count):
            self.textbox_list[ii_pl].pack()


class GameGrid:
    numbers_list = ['J', 'PTS', '15', '16', '17', '18', '19', '20', '25']

    def __init__(self, tk_main):

        self.game_frame = tk.Frame(tk_main)

        self.game_table = []
        self.textbox_table = []

    def set_players(self, strvar_list):
        names_list = [strvar.get() for strvar in strvar_list]

        self.game_table = [self.numbers_list]
        for ii_name in names_list:
            self.game_table.append([ii_name, '', '', '', '', '', '', '', ''])

        self.textbox_table = [[0]*len(self.numbers_list)]*len(names_list)

        for ii_row in range(1, len(self.game_table), 1):
            for jj_col in range(1, len(self.game_table[0]), 1):
                self.textbox_table[ii_row][jj_col] = tk.Entry(self.game_frame, width=20, font=('Arial', 20, 'bold'))

                self.textbox_table[ii_row][jj_col].grid(row=ii_row, column=jj_col)
                self.textbox_table[ii_row][jj_col].insert(tk.END, self.game_table[ii_row][jj_col])


def next_click():
    global main_frame_index
    global main_frame_list

    if main_frame_index == 0:
        main_frame_list[main_frame_index].players_frame.pack_forget()
        main_frame_index = 1
        main_frame_list[main_frame_index].set_players(main_frame_list[0].strvar_list)
        main_frame_list[main_frame_index].game_frame.pack()


def back_click():
    global main_frame_index
    global main_frame_list

    if main_frame_index == 1:
        main_frame_list[main_frame_index].game_frame.pack_forget()
        main_frame_index = 0
        main_frame_list[main_frame_index].players_frame.pack()


# ______main_______
main = tk.Tk()

player_selection = PlayerSelection(main)
game_grid = GameGrid(main)
main_frame_list = [player_selection, game_grid]
main_frame_index = 0

next_button = tk.Button(main, text='>', command=next_click)
next_button.pack()

back_button = tk.Button(main, text='<', command=back_click)
back_button.pack()


main.mainloop()
