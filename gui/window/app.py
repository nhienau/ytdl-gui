import customtkinter as ctk
import threading

from downloader.download import download
from helper.gui import set_textbox_value
from gui.frame.control import ControlFrame
from gui.frame.settings import SettingsFrame
from gui.frame.table import TableFrame
from gui.frame.download_info import DownloadInfoFrame
from preset import preset

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ytdl-gui")
        self.geometry("1152x648")
        self.grid_columnconfigure(0, minsize=360)
        self.grid_columnconfigure(tuple([val for val in range(1, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.set_appearance_mode("light")
        self._toplevel_window = None
        self._download_list = []
        preset.setup()
        self._preset = preset.get_all()
        self._current_preset = self._preset[0]
        self._displaying_video_settings = False
        self._download_thread = None
        self._stop_thread_event = threading.Event()
        self._download_extension_info = {} # {'initial': bool, 'extension': str}
        self._download_info = {
            "finished": 0,
            "error": 0,
            "pending": 0,
            "downloading_title": "",
            "stopped": False
        }

        self._control_frame = ControlFrame(self)
        self._control_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nswe", columnspan=20)
        
        self._settings_frame = SettingsFrame(self)
        self._settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe")

        self._table_frame = TableFrame(self)
        self._table_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky="nswe", columnspan=19)

        self._download_info_frame = DownloadInfoFrame(self)
        
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

    @property
    def download_extension_info(self):
        return self._download_extension_info

    @download_extension_info.setter
    def download_extension_info(self, download_extension_info):
        self._download_extension_info = download_extension_info

    @property
    def download_info(self):
        return self._download_info

    @download_info.setter
    def download_info(self, download_info):
        self._download_info = download_info

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

    def on_start_download_clicked(self):
        self.set_visibility_download_info_frame(False)
        self._settings_frame.hide_message()
        self._settings_frame.set_visibility_download_confirm_buttons(False)
        download_list = [entry for entry in self.download_list if entry["selected"] is True]
        if len(download_list) == 0:
            self._settings_frame.show_message(message = "No videos selected.", show_button = False)
            return
        else:
            self._settings_frame.show_message(
                message = f"{len(download_list)} URL{'' if len(download_list) == 1 else 's'} will be downloaded.",
                show_button = False)
            self._settings_frame.set_visibility_download_confirm_buttons(True)
    
    def on_confirm_download_clicked(self):
        self._settings_frame.hide_message()
        self._settings_frame.set_visibility_download_confirm_buttons(False)

        download_url_tuples = [(index, entry) for index, entry in enumerate(self.download_list) if entry["selected"] is True]
        if len(download_url_tuples) == 0:
            self._settings_frame.show_message(message = "No videos selected.", show_button = False)
            return

        self.disable_app()
        for index, entry in download_url_tuples:
            self._table_frame.set_download_status(entry, index, "pending")
        self.download_info = {
            "finished": 0,
            "error": 0,
            "pending": len(download_url_tuples),
            "downloading_title": "",
            "stopped": False,
        }
        self._download_info_frame.display(self.download_info)

        callbacks = {
            "on_url_start_downloading": self.on_url_start_downloading,
            "progress": self._table_frame.display_progress,
            "postprocessing": self._table_frame.on_url_postprocessing,
            "on_download_error": self.on_download_error,
            "on_download_stopped": self._table_frame.on_download_stopped,
            "on_all_urls_finished": self.enable_app
        }
        self._stop_thread_event.clear()
        self._download_thread = threading.Thread(target=download, args=(self._stop_thread_event, download_url_tuples, callbacks), daemon=True)
        self._download_thread.start()

    def set_visibility_progress_frame(self, visibility):
        if visibility is True:
            self._table_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky="nswe", columnspan=19)
            self._progress_frame.grid(row=2, column=1, padx=(5, 10), pady=(5, 10), sticky="nswe", columnspan=19)
        else:
            self._table_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky="nswe", rowspan=2, columnspan=19)
            self._progress_frame.grid_forget()

    def disable_app(self):
        if self.toplevel_window is not None and self.toplevel_window.winfo_exists():
            self.toplevel_window.destroy()
            self.toplevel_window = None

        self._control_frame._button_add_url.configure(state="disabled")
        self._control_frame._button_download.configure(state="disabled")
        self._control_frame._button_stop.configure(state="normal")

        self.set_visibility_download_info_frame(True)
        self._table_frame._table_buttons_frame.set_buttons_state("disabled")
        self._table_frame.set_buttons_state("disabled")
        self._table_frame.set_table_functionality_and_bindings(False)
        
    def enable_app(self):
        self._control_frame._button_add_url.configure(state="normal")
        self._control_frame._button_download.configure(state="normal")
        self._control_frame._button_stop.configure(state="disabled")

        self._table_frame.set_buttons_state("normal")
        self._table_frame.set_table_functionality_and_bindings(True)
        self.download_extension_info = {}

    def on_stop_downloading_clicked(self):
        self._stop_thread_event.set()
        self.download_info["stopped"] = True
        self.download_info["pending"] = 0
        self._download_info_frame.display(self.download_info)
        self.enable_app()

    def on_url_start_downloading(self, entry, index):
        self.download_extension_info = {
            "initial": True,
            "extension": None
        }
        self._table_frame.set_download_status(entry, index, "starting")
        self.download_info["pending"] = len([entry for entry in self.download_list if entry["status"] == "pending"])
        self.download_info["downloading_title"] = entry["title"]
        self._download_info_frame.display(self.download_info)

    def on_download_error(self, entry, index):
        self._table_frame.set_download_status(entry, index, "error", False)
        self.download_info["error"] = len([entry for entry in self.download_list if entry["status"] == "error"])
        self._download_info_frame.display(self.download_info)

    def on_entry_finish_downloading(self):
        self.download_info["finished"] = len([entry for entry in self.download_list if entry["status"] == "finished"])
        self.download_info["downloading_title"] = ""
        self._download_info_frame.display(self.download_info)

    def set_visibility_download_info_frame(self, visibility):
        if visibility:
            self._settings_frame.grid_forget()
            self._download_info_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe")
        else:
            self._download_info_frame.grid_forget()
            self._settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe")


