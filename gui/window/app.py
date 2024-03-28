import customtkinter as ctk

from gui.frame.control import ControlFrame
from gui.frame.settings import SettingsFrame
from gui.frame.table import TableFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ytdl-gui")
        self.geometry("1152x648")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.set_appearance_mode("light")
        self._data = []
        
        self._control_frame = ControlFrame(self)
        self._control_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nswe", columnspan=20)
        
        self._settings_frame = SettingsFrame(self)
        self._settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe", columnspan=4)

        self._table_frame = TableFrame(self, data=self._data)
        self._table_frame.grid(row=1, column=4, padx=(5, 10), pady=10, sticky="nswe", columnspan=16)
        self._table_frame.display(self._data)

    def on_add_urls(self, entries):
        existing_urls = {entry.get("webpage_url") or entry.get("url") for entry in self._data}
        num_entries_before_add = len(entries)
        entries = [entry for entry in entries if (entry.get("webpage_url") or entry.get("url")) not in existing_urls]
        len_before_add = len(self._data)
        self._data += entries
        added = len(self._data) - len_before_add
        self._table_frame.data = self._data
        self._table_frame.display(self._data)
        return {
            "added": added,
            "not_added": num_entries_before_add - added
        }


