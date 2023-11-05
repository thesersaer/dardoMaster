import customtkinter as ctk
import basicf
import control.plselect


class PlayerSelection(basicf.AppFrame):
    def __init__(self, root, controller: control.plselect.PlayerSelection):
        super(PlayerSelection, self).__init__(root)

        self.frame = ctk.CTkFrame(root)
        self._ctrl = controller

        self.player_slider_var = ctk.IntVar(self.frame, value=self._ctrl.min_players)
        self.player_slider = ctk.CTkSlider(self.frame, from_=self._ctrl.min_players, to=self._ctrl.max_players,
                                           number_of_steps=(self._ctrl.max_players - self._ctrl.min_players),
                                           variable=self.player_slider_var, command=self.player_slider_event)
        self.player_slider.pack(padx=10, pady=10)

        self.player_label = ctk.CTkLabel(self.frame, text=self.player_slider_var.get(), font=('', 20))
        self.player_label.pack(padx=10, pady=5)

    def player_slider_event(self, event):
        self._ctrl.set_players(int(event))
        self.player_label.configure(text=self._ctrl.number_of_players)


if __name__ == '__main__':
    basicf.test_frame(PlayerSelection, control.plselect.PlayerSelection)
