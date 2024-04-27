import customtkinter as ctk

class PresetButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self._button_rename_preset = ctk.CTkButton(self, text="Rename", width=24, fg_color="#EBEEF2", hover_color="#D4D6DA", text_color="#2F3C4E")
        self._button_rename_preset.grid(row=0, column=0)

        self._button_save_preset_changes = ctk.CTkButton(self, text="Save", width=24, fg_color="#EBEEF2", hover_color="#D4D6DA", text_color="#2F3C4E")
        self._button_save_preset_changes.grid(row=0, column=1, padx=(5, 0))


