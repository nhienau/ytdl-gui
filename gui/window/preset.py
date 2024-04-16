import customtkinter as ctk
from tksheet import Sheet

from gui.frame.preset_detail import PresetDetailFrame
from gui.frame.preset_table import PresetTableFrame

class PresetWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ytdl-gui")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._root_data = list(args)[0]._parent

        self._preset_table_frame = PresetTableFrame(self)
        self._preset_table_frame.grid(row = 0, column = 0, sticky = "nswe", columnspan = 5, padx = 10, pady = 10)

        self._preset_detail_frame = PresetDetailFrame(self)
        self._preset_detail_frame.grid(row = 0, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)

        self._button_confirm_choose_preset = ctk.CTkButton(self, text="OK")
        self._button_confirm_choose_preset.grid(row = 1, column=19, sticky="e", padx = (0, 10), pady = (0, 10))

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    def on_table_cell_selected(self, e):
        currently_selected = self._preset_table_frame._sheet.get_currently_selected()
        row = currently_selected.row
        self._preset_detail_frame.preset = self.root_data.preset[row]
