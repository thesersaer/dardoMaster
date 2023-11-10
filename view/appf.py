import customtkinter as ctk
import threading
import time

import control.game
import control.app
import plselect
import plnames
import gamef


class App:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.ctk = ctk.CTk()
        self.ctk.title('DardoMaster')

        self.buttons_frame = ctk.CTkFrame(self.ctk)

        self.next_button = ctk.CTkButton(self.buttons_frame, text='>', command=self.next_button_event)
        self.next_button.pack(side=ctk.RIGHT, padx=10, pady=10)

        self.back_button = ctk.CTkButton(self.buttons_frame, text='<', command=self.back_button_event)
        self.back_button.pack(side=ctk.LEFT, padx=10, pady=10)

        self.buttons_frame.pack(fill=ctk.X, side=ctk.BOTTOM)

        # _______________
        self.controller = control.game.GameFrame()
        self.app_controller = control.app.App()

        player_selection = plselect.PlayerSelection(self.ctk, self.controller)
        player_names = plnames.PlayerNames(self.ctk, self.controller)
        game_frame = gamef.GameFrame(self.ctk, self.controller)

        player_selection.pack_frame()

        self.app_frames = [player_selection, player_names, game_frame]

        self.exit_game_confirmation = False

    def main(self):
        self.ctk.mainloop()

    def next_button_event(self):
        if self.app_controller.frame_index == 2:
            self.update_start_game_button_state('disabled')
            self.app_controller.start_game(self.controller.player_names)
            return

        self.app_controller.next_button_event()
        self.raise_frame(self.app_controller.frame_index)

    def back_button_event(self):
        if self.app_controller.frame_index == 2:
            if not self.exit_game_confirmation:
                self.exit_game_confirmation = True
                self.back_button.configure(text='Confirmar Abandono')
                threading.Thread(target=self.on_forfeit_game_confirmation_countdown).start()
                return
            else:
                self.update_start_game_button_state('normal')
                self.app_controller.forfeit_game()

        self.app_controller.back_button_event()
        self.raise_frame(self.app_controller.frame_index)

    def on_forfeit_game_confirmation_countdown(self):
        time.sleep(1)
        self.exit_game_confirmation = False
        if self.app_controller.frame_index == 2:
            self.back_button.configure(text='Abandonar')

    def on_game_load_buttons_resprite(self):
        self.next_button.configure(text='Empezar', fg_color="#2CC985", hover_color="#209361")
        self.back_button.configure(text='Abandonar', fg_color="#D3367A", hover_color="#9E295B")

    def on_forfeit_game_buttons_resprite(self):
        self.next_button.configure(text='>', fg_color=['#3a7ebf', '#1f538d'], hover_color=["#325882", "#14375e"])
        self.back_button.configure(text='<', fg_color=['#3a7ebf', '#1f538d'], hover_color=["#325882", "#14375e"])

    def update_start_game_button_state(self, state: str):
        self.next_button.configure(state=state)

    def raise_frame(self, index: int):
        for frame in self.app_frames:
            frame.pack_forget_frame()
        self.app_frames[index].pack_frame()
        if index == 2:
            self.on_game_load_buttons_resprite()
        else:
            self.on_forfeit_game_buttons_resprite()


def main():
    root = App()
    root.main()


if __name__ == '__main__':
    main()
