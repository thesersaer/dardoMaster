import customtkinter as ctk

import basicf
import plgrid
import plturn
import control.plgrid
import control.plturn
import control.game


class GameFrame(basicf.AppFrame):
    def __init__(self, root, controller):
        super().__init__(root)

        self._ctrl = controller

        self.grid_frame = plgrid.PlayerGrid(self.frame, self._ctrl)
        self.turn_frame = plturn.PlayerTurn(self.frame, self._ctrl)

    def pack_frame(self, **kwargs):
        self.grid_frame.pack_frame(side=ctk.LEFT, padx=10, pady=10)
        self.turn_frame.pack_frame(side=ctk.RIGHT, padx=10, pady=10)
        basicf.AppFrame.pack_frame(self, **kwargs)


if __name__ == '__main__':
    basicf.test_frame(GameFrame, control.game.GameFrame)
