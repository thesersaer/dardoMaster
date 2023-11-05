import customtkinter as ctk
import control.plgrid
import control.app
import plselect
import plnames
import plgrid


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
        self.controller = control.plgrid.PlayerGrid()
        self.app_controller = control.app.App()

        player_selection = plselect.PlayerSelection(self.ctk, self.controller)
        player_names = plnames.PlayerNames(self.ctk, self.controller)
        game_grid = plgrid.PlayerGrid(self.ctk, self.controller)

        player_selection.pack_frame()

        self.app_frames = [player_selection, player_names, game_grid]

    def main(self):
        self.ctk.mainloop()

    def next_button_event(self):
        self.app_controller.next_button_event()
        self.raise_frame(self.app_controller.frame_index)

    def back_button_event(self):
        self.app_controller.back_button_event()
        self.raise_frame(self.app_controller.frame_index)

    def raise_frame(self, index: int):
        for frame in self.app_frames:
            frame.pack_forget_frame()
        self.app_frames[index].pack_frame()


def main():
    root = App()
    root.main()


if __name__ == '__main__':
    main()
