import customtkinter as ctk
from PIL import Image

class PresetButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.callbacks = {}

        self._icon_save = ctk.CTkImage(light_image=Image.open("gui/icons/save.png"), dark_image=Image.open("gui/icons/save.png"), size=(24, 24))

        self._button_save_preset_changes = ctk.CTkButton(self, image=self._icon_save, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center")
        self._button_save_preset_changes.grid(row=0, column=0)

        self._icon_rename = ctk.CTkImage(light_image=Image.open("gui/icons/rename.png"), dark_image=Image.open("gui/icons/rename.png"), size=(24, 24))

        self._button_rename_preset = ctk.CTkButton(self, image=self._icon_rename, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center")
        self._button_rename_preset.grid(row=0, column=1)

        self._icon_delete = ctk.CTkImage(light_image=Image.open("gui/icons/delete.png"), dark_image=Image.open("gui/icons/delete.png"), size=(24, 24))

        self._button_delete_preset = ctk.CTkButton(self, image=self._icon_delete, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center")
        self._button_delete_preset.grid(row=0, column=2)


