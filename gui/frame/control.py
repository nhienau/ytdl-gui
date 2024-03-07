import customtkinter as ctk
from PIL import Image

from gui.window.add_url import AddUrlWindow

class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.toplevel_window = None
        self.callbacks = {}

        self.icon_add = ctk.CTkImage(light_image=Image.open("gui/icons/add.png"), dark_image=Image.open("gui/icons/add.png"), size=(32, 32))

        self.button_add_url = ctk.CTkButton(self, image=self.icon_add, text="", width=32, fg_color="transparent", anchor="center", command=self.on_add_url_click)
        self.button_add_url.grid(row=0, column=0)

    def on_add_url_click(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddUrlWindow(self) # create window if its None or destroyed
        else:
            self.toplevel_window.focus() # if window exists focus it