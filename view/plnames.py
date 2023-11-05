import customtkinter as ctk
import basicf
import control.plnames


class PlayerNames(basicf.AppFrame):
    def __init__(self, root, controller: control.plnames.PlayerNames):
        super(PlayerNames, self).__init__(root)

        self._ctrl = controller

        self.frame = ctk.CTkFrame(root)

        self.player_names = [ctk.StringVar(self.frame, value=f'P{index + 1}')
                             for index in range(self._ctrl.max_players)]
        for variable in self.player_names:
            variable.trace_add('write', self.on_entry_write)
        self.player_entries = [ctk.CTkEntry(self.frame, textvariable=self.player_names[index])
                               for index in range(self._ctrl.max_players)]

    def pack_entries(self, player_amount: int):
        for ii_player in range(self._ctrl.max_players):
            self.player_entries[ii_player].pack_forget()

        for ii_player in range(player_amount):
            self.player_entries[ii_player].pack(side=ctk.TOP, padx=10, pady=10)

    def pack_frame(self):
        self.pack_entries(self._ctrl.number_of_players)
        basicf.AppFrame.pack_frame(self)

    def pack_forget_frame(self):
        for index in range(self._ctrl.number_of_players):
            self._ctrl.set_player_name(self.player_names[index].get(), index)
        basicf.AppFrame.pack_forget_frame(self)

    def on_entry_write(self, *args):
        index = int(args[0][-1])
        name = self.player_names[index].get()
        self._ctrl.set_player_name(name, index)


if __name__ == '__main__':
    basicf.test_frame(PlayerNames, control.plnames.PlayerNames)
