import customtkinter as ctk
from PIL import Image

from gui.window.add_url import AddUrlWindow
from gui.window.preset import PresetWindow

class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._parent = master

        self._icon_add = ctk.CTkImage(light_image=Image.open("gui/icons/add.png"), dark_image=Image.open("gui/icons/add.png"), size=(32, 32))

        self._button_add_url = ctk.CTkButton(self, image=self._icon_add, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self._on_add_url_click)
        self._button_add_url.grid(row=0, column=0)

        self._icon_settings = ctk.CTkImage(light_image=Image.open("gui/icons/settings.png"), dark_image=Image.open("gui/icons/settings.png"), size=(32, 32))

        self._button_preset = ctk.CTkButton(self, image=self._icon_settings, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self._on_button_preset_click)
        self._button_preset.grid(row=0, column=1)

        self._icon_download = ctk.CTkImage(light_image=Image.open("gui/icons/download.png"), dark_image=Image.open("gui/icons/download.png"), size=(32, 32))

        self._button_download = ctk.CTkButton(self, image=self._icon_download, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=master.on_start_download_clicked)
        self._button_download.grid(row=0, column=2)

        self._icon_stop = ctk.CTkImage(light_image=Image.open("gui/icons/stop.png"), dark_image=Image.open("gui/icons/stop.png"), size=(32, 32))

        self._button_stop = ctk.CTkButton(self, image=self._icon_stop, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=master.on_stop_downloading_clicked, state="disabled")
        self._button_stop.grid(row=0, column=3)

    def _on_add_url_click(self):
        if self._parent.toplevel_window is None or not self._parent.toplevel_window.winfo_exists():
            self._parent.toplevel_window = AddUrlWindow(self)
        else:
            self._parent.toplevel_window.focus()
            self._parent.toplevel_window.lift()

    def _on_button_preset_click(self):
        if self._parent.toplevel_window is None or not self._parent.toplevel_window.winfo_exists():
            self._parent.toplevel_window = PresetWindow(self)
        else:
            self._parent.toplevel_window.focus()
            self._parent.toplevel_window.lift()


