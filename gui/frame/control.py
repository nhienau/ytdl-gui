import customtkinter as ctk
from PIL import Image

from gui.window.add_url import AddUrlWindow

class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._toplevel_window = None
        self.callbacks = {
            "on_add_urls": master.on_add_urls,
        }

        self._icon_add = ctk.CTkImage(light_image=Image.open("gui/icons/add.png"), dark_image=Image.open("gui/icons/add.png"), size=(32, 32))

        self._button_add_url = ctk.CTkButton(self, image=self._icon_add, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self._on_add_url_click)
        self._button_add_url.grid(row=0, column=0)

        self._icon_download = ctk.CTkImage(light_image=Image.open("gui/icons/download.png"), dark_image=Image.open("gui/icons/download.png"), size=(32, 32))

        self._button_download = ctk.CTkButton(self, image=self._icon_download, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center")
        self._button_download.grid(row=0, column=1)

    def _on_add_url_click(self):
        if self._toplevel_window is None or not self._toplevel_window.winfo_exists():
            self._toplevel_window = AddUrlWindow(self) # create window if its None or destroyed
            self._toplevel_window.add_callbacks(self.callbacks)
        else:
            self._toplevel_window.focus() # if window exists focus it

    
