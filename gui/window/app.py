import customtkinter as ctk

from helper.gui import set_textbox_value
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
        self._displaying_video_settings = False

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

    @property
    def displaying_video_settings(self):
        return self._displaying_video_settings

    @displaying_video_settings.setter
    def displaying_video_settings(self, displaying_video_settings):
        self._displaying_video_settings = displaying_video_settings

    def on_add_urls(self, entries):
        existing_urls = {entry.get("webpage_url") or entry.get("url") for entry in self._download_list}
        num_entries_before_add = len(entries)
        entries = [entry for entry in entries if (entry.get("webpage_url") or entry.get("url")) not in existing_urls]
        len_before_add = len(self._download_list)
        self.apply_preset_to_urls(entries, self.current_preset)
        self._download_list += entries
        added = len(self._download_list) - len_before_add
        self._table_frame.data = self._download_list
        self._table_frame.display(self._download_list)
        return {
            "added": added,
            "not_added": num_entries_before_add - added
        }

    def apply_preset_to_urls(self, urls, preset):
        for url in urls:
            url.update({ "preset": preset.copy() })

    def on_table_rows_clicked(self, selected_rows):
        title = ""
        preset_found = False
        if len(selected_rows) == 0:
            set_textbox_value(self._settings_frame._textbox_title, "(No videos selected)")
            set_textbox_value(self._settings_frame._textbox_preset, "")
            return
        elif len(selected_rows) == 1:
            entry = self.download_list[selected_rows[0]]
            title = entry["title"]
            self._settings_frame.display(entry["preset"])
            self._displaying_video_settings = True
            current_preset_settings = [p for p in self.preset if p["id"] == entry["preset"]["id"]]
            preset_found = len(current_preset_settings) != 0 and entry["preset"] == current_preset_settings[0]
        else:
            title = f"({len(selected_rows)} videos selected)"
            preset_found = False
            
        set_textbox_value(self._settings_frame._textbox_title, title)
        if preset_found == False:
            set_textbox_value(self._settings_frame._textbox_preset, "(Custom)")
        self._settings_frame.set_visibility_buttons_frame(preset_found)

    def on_confirm_apply_preset(self):
        self._settings_frame.hide_message()

        preset_data = self._settings_frame.get_form_data()
        if self._displaying_video_settings is True:
            settings = preset_data.copy()
        else:
            settings = self._current_preset.copy()
            settings.update(preset_data.copy())

        if self._settings_frame.apply_option == "all":
            for entry in self.download_list:
                entry["preset"].update(settings.copy())
        else:
            selected_rows = self._table_frame._selected_rows
            if len(selected_rows) == 0:
                self._settings_frame.show_message(message = "No videos selected.", show_button = False)
                return

            for i in selected_rows:
                self._download_list[i]["preset"].update(settings.copy())
            
        self._table_frame.data = self._download_list
        self._table_frame.display(data = self._download_list, deselect = False)


