import customtkinter as ctk

from gui.frame.control import ControlFrame
from gui.frame.settings import SettingsFrame
from gui.frame.table import TableFrame
from preset import preset

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ytdl-gui")
        self.geometry("1152x648")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.set_appearance_mode("light")
        self._toplevel_window = None
        self._download_list = []
        preset.setup()
        self._preset = preset.get_all()
        self._current_preset = self._preset[0]

        self._control_frame = ControlFrame(self)
        self._control_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nswe", columnspan=20)
        
        self._settings_frame = SettingsFrame(self)
        self._settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe", columnspan=4)

        self._table_frame = TableFrame(self)
        self._table_frame.grid(row=1, column=4, padx=(5, 10), pady=(5, 10), sticky="nswe", columnspan=16)

    @property
    def toplevel_window(self):
        return self._toplevel_window

    @toplevel_window.setter
    def toplevel_window(self, toplevel_window):
        self._toplevel_window = toplevel_window

    @property
    def download_list(self):
        return self._download_list

    @download_list.setter
    def download_list(self, download_list):
        self._download_list = download_list

    @property
    def preset(self):
        return self._preset

    @preset.setter
    def preset(self, preset):
        self._preset = preset

    @property
    def current_preset(self):
        return self._current_preset

    @current_preset.setter
    def current_preset(self, current_preset):
        self._current_preset = current_preset

    def on_add_urls(self, entries):
        existing_urls = {entry.get("webpage_url") or entry.get("url") for entry in self._download_list}
        num_entries_before_add = len(entries)
        entries = [entry for entry in entries if (entry.get("webpage_url") or entry.get("url")) not in existing_urls]
        len_before_add = len(self._download_list)
        self._download_list += entries
        added = len(self._download_list) - len_before_add
        self._table_frame.data = self._download_list
        self._table_frame.display(self._download_list)
        return {
            "added": added,
            "not_added": num_entries_before_add - added
        }


