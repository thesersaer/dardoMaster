import customtkinter as ctk


class AppFrame:
    def __init__(self, root):
        self.frame = ctk.CTkFrame(root, fg_color='transparent')

    def pack_frame(self, **kwargs):
        if kwargs:
            self.frame.pack(**kwargs)
        else:
            self.frame.pack(side=ctk.TOP, expand=ctk.YES)

    def pack_forget_frame(self):
        self.frame.pack_forget()

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def grid_forget(self):
        self.frame.grid_forget()

class GridCell:
    def __init__(self, root, row: int, col: int):
        self.frame = ctk.CTkFrame(root, fg_color='transparent')

        self.row = row
        self.col = col

    def pack_cell(self):
        self.frame.grid(row=self.row, column=self.col)

    def pack_forget_cell(self):
        self.frame.grid_forget()


def test_frame(frame_cls, ctrl_cls):
    root = ctk.CTk()
    ctrl = ctrl_cls()
    frame = frame_cls(root, ctrl)
    frame.pack_frame()
    root.mainloop()


def main():
    root = ctk.CTk()
    app_frame = AppFrame(root)
    app_frame.pack_frame()
    root.mainloop()


if __name__ == '__main__':
    main()
