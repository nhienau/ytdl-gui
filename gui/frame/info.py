import customtkinter as ctk

class InfoFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Info")
        self.label.grid(row=0, column=0)

        