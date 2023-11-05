import customtkinter as ctk


class AppFrame:
    def __init__(self, root):
        self.frame = ctk.CTkFrame(root)

    def pack_frame(self):
        self.frame.pack(side=ctk.TOP, expand=ctk.YES)

    def pack_forget_frame(self):
        self.frame.pack_forget()


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
