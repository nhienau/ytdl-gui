import customtkinter as ctk
from PIL import Image
from pathlib import Path
import tkinter as tk

from .input_size_limit import InputSizeLimitFrame
from .preset_buttons import PresetButtonsFrame
from helper.get_download_folder import get_download_folder
from helper.gui import set_textbox_value
from gui.window.preset import PresetWindow
import preset.preset as preset

class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)
        self._parent = master
        self._temp_preset_name = ""
        self.apply_option = ""

        self._label_title = ctk.CTkLabel(self, text="Title")
        self._label_title.grid(row=0, column=0, pady=(0, 10), sticky="nw")

        self._textbox_title = ctk.CTkTextbox(self)
        self._textbox_title.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="ew", columnspan=3)
        self._textbox_title.insert("0.0", "(No videos selected)")
        self._textbox_title.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_preset = ctk.CTkLabel(self, text="Preset")
        self._label_preset.grid(row=1, column=0, pady=(0, 10), sticky="nsw")

        self._textbox_preset = ctk.CTkTextbox(self)
        self._textbox_preset.grid(row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="ew", columnspan=2)
        self._textbox_preset.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_choose_preset = ctk.CTkButton(self, text="Choose", width=24, command=self._on_choose_preset)
        self._button_choose_preset.grid(row=1, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

        self._preset_buttons_frame = PresetButtonsFrame(self)
        self._preset_buttons_frame.grid(row=2, column=2, pady=(0, 10), sticky="e", columnspan=2)
        self._preset_buttons_frame._button_rename_preset.configure(command=self._on_change_preset_name_clicked)
        self._preset_buttons_frame._button_save_preset_changes.configure(command=self._on_save_preset_changes_clicked)

        self._label_download_option = ctk.CTkLabel(self, text="Include")
        self._label_download_option.grid(row=3, column=0, pady=(0, 10), sticky="nsw")

        self._download_option_value = ctk.StringVar(value="Video + audio")
        self._download_option_value.trace("w", self._on_option_change)
        self._combobox_download_option = ctk.CTkComboBox(self, values=["Video + audio", "Video only", "Audio only"], state="readonly", variable=self._download_option_value, command=self._on_download_option_change)
        self._combobox_download_option.grid(row=3, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_download_option.set("Video + audio")

        self._split_video_audio = ctk.BooleanVar(value=False)
        self._split_video_audio.trace("w", self._on_option_change)
        self._checkbox_split_video_audio = ctk.CTkCheckBox(self, text="Split into separate files", onvalue=True, offvalue=False, variable=self._split_video_audio)
        self._checkbox_split_video_audio.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_chapter = ctk.CTkLabel(self, text="Chapter")
        self._label_chapter.grid(row=5, column=0, pady=(0, 10), sticky="nw")

        self._split_by_chapters = ctk.BooleanVar(value=False)
        self._split_by_chapters.trace("w", self._on_option_change)
        self._checkbox_chapter = ctk.CTkCheckBox(self, text="Split video by chapters", onvalue=True, offvalue=False, variable=self._split_by_chapters)
        self._checkbox_chapter.grid(row=5, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        
        self._label_resolution = ctk.CTkLabel(self, text="Resolution")
        self._label_resolution.grid(row=6, column=0, pady=(0, 10), sticky="nw")

        self._resolution = ctk.StringVar(value="Best")
        self._resolution.trace("w", self._on_option_change)
        self._combobox_resolution = ctk.CTkComboBox(self, values=["Best", "2160p (4K)", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"], state="readonly", variable=self._resolution)
        self._combobox_resolution.grid(row=6, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_size_limit = ctk.CTkLabel(self, text="File size")
        self._label_size_limit.grid(row=7, column=0, pady=(0, 10), sticky="nw")

        self._size_limit = ctk.StringVar(value="Best")
        self._size_limit.trace("w", self._on_option_change)
        self._combobox_size_limit = ctk.CTkComboBox(self, values=["Best", "Custom"], state="readonly", variable=self._size_limit, command=self._on_size_limit_option_change)
        self._combobox_size_limit.grid(row=7, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._frame_size_limit = InputSizeLimitFrame(self)
        self._frame_size_limit.size_limit.trace("w", self._handle_size_limit_change)

        self._label_subtitle = ctk.CTkLabel(self, text="Subtitle")
        self._label_subtitle.grid(row=9, column=0, pady=(0, 10), sticky="nw")

        self._subtitle = ctk.BooleanVar(value=False)
        self._subtitle.trace("w", self._on_option_change)
        self._checkbox_subtitle = ctk.CTkCheckBox(self, text="Download subtitle (if available)", onvalue=True, offvalue=False, variable=self._subtitle)
        self._checkbox_subtitle.grid(row=9, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_thumbnail = ctk.CTkLabel(self, text="Thumbnail")
        self._label_thumbnail.grid(row=10, column=0, pady=(0, 10), sticky="nw")

        self._thumbnail = ctk.BooleanVar(value=False)
        self._thumbnail.trace("w", self._on_option_change)
        self._checkbox_thumbnail = ctk.CTkCheckBox(self, text="Save thumbnail (if available)", onvalue=True, offvalue=False, variable=self._thumbnail)
        self._checkbox_thumbnail.grid(row=10, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_sponsorblock = ctk.CTkLabel(self, text="Sponsorblock")
        self._label_sponsorblock.grid(row=11, column=0, pady=(0, 10), sticky="nw")

        self._sponsorblock = ctk.BooleanVar(value=False)
        self._sponsorblock.trace("w", self._on_option_change)
        self._checkbox_sponsorblock = ctk.CTkCheckBox(self, text="Remove sponsor sections", onvalue=True, offvalue=False, variable=self._sponsorblock)
        self._checkbox_sponsorblock.grid(row=11, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_output_folder = ctk.CTkLabel(self, text="Output folder")
        self._label_output_folder.grid(row=12, column=0, pady=(0, 10), sticky="nw")

        self._output_path = ctk.StringVar(value="")
        self._output_path.trace("w", self._on_option_change)
        self._input_output_folder = ctk.CTkEntry(self, state="disabled", textvariable=self._output_path)
        self._input_output_folder.grid(row=12, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=2)

        self._button_browse = ctk.CTkButton(self, text="Browse", width=24, command=self._on_browse_dir_clicked)
        self._button_browse.grid(row=12, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

        self._button_apply_to_all = ctk.CTkButton(self, text="Apply to all", width=24, command=self._on_apply_preset_click)
        self._button_apply_to_all.grid(row=13, column=2, pady=(0, 10), sticky="e")

        self._button_apply_single = ctk.CTkButton(self, text="Apply", width=24, command=lambda: self._on_apply_preset_click(apply_all=False))
        self._button_apply_single.grid(row=13, column=3, pady=(0, 10), sticky="e")

        self._textbox_message = ctk.CTkTextbox(self)
        self._textbox_message.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_cancel_apply = ctk.CTkButton(self, text="Cancel", width=24, command=self._on_button_cancel_apply_clicked)

        self._button_confirm_apply = ctk.CTkButton(self, text="OK", width=24, command=master.on_confirm_apply_preset)

        self._button_cancel_download = ctk.CTkButton(self, text="Cancel", width=24, command=self.on_button_download_clicked)

        self._button_confirm_download = ctk.CTkButton(self, text="OK", width=24, command=master.on_confirm_download_clicked)

        # For toggling combobox state
        self._combobox_elements = [self._combobox_download_option, self._combobox_resolution, self._combobox_size_limit]

        self.display(master.current_preset)

    def get_form_data(self):
        return {
            "name": self._temp_preset_name,
            "include_video": "video" in self._download_option_value.get().strip().lower(),
            "include_audio": "audio" in self._download_option_value.get().strip().lower(),
            "split_video_and_audio": self._split_video_audio.get() if all(el in self._download_option_value.get().lower() for el in ["video", "audio"]) else False,
            "split_by_chapters": self._split_by_chapters.get(),
            "resolution": None if self._resolution.get().lower() == "best" else self._resolution.get(),
            "max_file_size": None if self._size_limit.get().lower() == "best" else self._frame_size_limit.size_limit.get(),
            "subtitle": self._subtitle.get(),
            "thumbnail": self._thumbnail.get(),
            "sponsorblock": self._sponsorblock.get(),
            "output_path": self._output_path.get(),
        }

    def _on_choose_preset(self):
        if self._parent.toplevel_window is None or not self._parent.toplevel_window.winfo_exists():
            self._parent.toplevel_window = PresetWindow(self)
            self._parent.toplevel_window.choose = True
        else:
            self._parent.toplevel_window.focus()
            self._parent.toplevel_window.lift()
        
    def display(self, preset):
        elements_state = "normal" if preset["editable"] is True else "disabled"
        self.set_elements_state(elements_state)

        # Temporarily set combobox states back to "normal" since we are displaying preset info (therefore modifying combobox values)
        for element in self._combobox_elements:
            element.configure(state="normal")

        if preset["include_video"] and preset["include_audio"]:
            self._combobox_download_option.set("Video + audio")
            self._checkbox_split_video_audio.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        elif preset["include_video"] and not preset["include_audio"]:
            self._combobox_download_option.set("Video only")
            self._checkbox_split_video_audio.grid_forget()
        else:
            self._combobox_download_option.set("Audio only")
            self._checkbox_split_video_audio.grid_forget()

        self._split_video_audio.set(preset["split_video_and_audio"])
        self._split_by_chapters.set(preset["split_by_chapters"])
        self._resolution.set("Best" if preset["resolution"] is None else preset["resolution"])

        self._size_limit.set("Best" if preset["max_file_size"] is None else "Custom")
        if preset["max_file_size"] is None:
            self._frame_size_limit.grid_forget()
        else:
            self._frame_size_limit.grid(row=8, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)
            self._frame_size_limit.size_limit.set(preset["max_file_size"])

        self._subtitle.set(preset["subtitle"])
        self._thumbnail.set(preset["thumbnail"])
        self._sponsorblock.set(preset["sponsorblock"])
        self._output_path.set(preset["output_path"])
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()

        # Set comboboxes state back to "readonly"/"normal" after modifying them
        combobox_state = "readonly" if elements_state == "normal" else "disabled"
        for element in self._combobox_elements:
            element.configure(state=combobox_state)

        set_textbox_value(self._textbox_preset, preset["name"])
        self._temp_preset_name = preset["name"]
        self._preset_buttons_frame._button_rename_preset.configure(state="normal" if preset["editable"] is True else "disabled")
        self._preset_buttons_frame._button_save_preset_changes.configure(state="disabled")
        self.hide_message()
        self.set_visibility_buttons_frame(False)
        self.set_visibility_download_confirm_buttons(False)

    def set_elements_state(self, state):
        for element in [self._checkbox_split_video_audio, self._checkbox_chapter, self._frame_size_limit._input_size_limit, self._checkbox_subtitle, self._checkbox_thumbnail, self._checkbox_sponsorblock]:
            element.configure(state=state)

        combobox_state = "readonly" if state == "normal" else "disabled"
        for element in self._combobox_elements:
            element.configure(state=combobox_state)

    def _on_option_change(self, _, __, ___):
        self._preset_buttons_frame._button_save_preset_changes.configure(state="normal")
        if self._parent.displaying_video_settings is False:
            set_textbox_value(self._textbox_preset, self._temp_preset_name + " (*)")

    def _on_download_option_change(self, value):
        if value == "Video + audio":
            self._checkbox_split_video_audio.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        else:
            self._checkbox_split_video_audio.grid_forget()

    def _on_size_limit_option_change(self, value):
        if value == "Best":
            self._frame_size_limit.grid_forget()
        else:
            self._frame_size_limit.grid(row=8, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)
        
    def _handle_size_limit_change(self, _, __, ___):
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()
        value = self._frame_size_limit.size_limit.get()

        try:
            value = float(value)
        except:
            set_textbox_value(self._textbox_message, "File size limit must be a float number.")
            self._textbox_message.grid(row=14, column=0, pady=(0, 10), sticky="ew", columnspan=4)

    def _on_browse_dir_clicked(self):
        dir_path = tk.filedialog.askdirectory(parent=self._parent, title="Change output folder to...", initialdir=get_download_folder())
        if dir_path == "" or dir_path == self._output_path:
            return
        self._output_path.set(dir_path)

    def _on_change_preset_name_clicked(self):
        dialog = ctk.CTkInputDialog(title="ytdl-gui", text="Preset name:")
        value = dialog.get_input().strip()
        if value == "":
            set_textbox_value(self._textbox_message, "Preset name cannot be empty.")
            self._textbox_message.grid(row=14, column=0, pady=(0, 10), sticky="ew", columnspan=4)
        else:
            self._temp_preset_name = value
            self._on_option_change(None, None, None)

    def validate_form_data(self):
        valid = True
        error_message = ""
        output_path = self._output_path.get()
        path = Path(output_path)
        if self._temp_preset_name == "":
            error_message = "Preset name cannot be empty."
            valid = False
        elif self._size_limit.get().strip().lower() == "custom":
            try:
                size_limit = float(self._frame_size_limit.size_limit.get())
            except:
                error_message = "File size limit must be a float number."
                valid = False
        elif output_path == "":
            error_message = "Output path cannot be empty."
            valid = False
        elif not path.exists() or not path.is_dir():
            error_message = "Output path is not a directory or cannot be found."
            valid = False

        return {
            "valid": valid,
            "error_message": error_message
        }

    def _on_save_preset_changes_clicked(self):
        self._textbox_message.grid_forget()
        validation = self.validate_form_data()
        
        if validation["valid"] is True:
            modified_preset = self._parent.current_preset.copy()
            form_data = self.get_form_data()
            modified_preset.update(form_data)
            preset.update(modified_preset)
            self._parent.current_preset.update(modified_preset)
            set_textbox_value(self._textbox_preset, self._parent.current_preset["name"])
            self._preset_buttons_frame._button_save_preset_changes.configure(state="disabled")

            if self._parent.toplevel_window is not None and self._parent.toplevel_window.winfo_exists() and isinstance(self._parent.toplevel_window, PresetWindow) is True:
                self._parent.toplevel_window.on_main_window_preset_updated()

        else:
            set_textbox_value(self._textbox_message, validation["error_message"])
            self._textbox_message.grid(row=14, column=0, pady=(0, 10), sticky="ew", columnspan=4)

    def set_visibility_buttons_frame(self, visibility):
        if visibility is True:
            self._preset_buttons_frame.grid(row=2, column=2, pady=(0, 10), sticky="e", columnspan=2)
        else:
            self._preset_buttons_frame.grid_forget()

    def set_visibility_textbox_message(self, visibility):
        if visibility is True:
            self._textbox_message.grid(row=14, column=0, pady=(0, 10), sticky="ew", columnspan=4)
        else:
            self._textbox_message.grid_forget()

    def _on_apply_preset_click(self, apply_all=True):
        self._textbox_message.grid_forget()
        validation = self.validate_form_data()

        if validation["valid"] is False:
            self.show_message(message = validation["error_message"], show_button = False)
            return

        self.apply_option = "all" if apply_all is True else "selected"

        num_vids_to_apply = 0
        if apply_all is True:
            num_vids_to_apply = len(self._parent.download_list)

        else:
            selected_rows = self._parent._table_frame._selected_rows
            if len(selected_rows) == 0:
                self.show_message(message = "No videos selected.", show_button = False)
                self.apply_option = ""
                return
            num_vids_to_apply = len(selected_rows)
        
        self.show_message(message = f"Settings above will be applied to {num_vids_to_apply} url{'' if num_vids_to_apply == 1 else 's'}.", show_button = True)

    def show_message(self, message, show_button=False):
        set_textbox_value(self._textbox_message, message)
        self._textbox_message.grid(row=14, column=0, pady=(0, 10), sticky="ew", columnspan=4)
        if show_button is True:
            self._button_cancel_apply.grid(row=15, column=2, pady=(0, 10), sticky="e")
            self._button_confirm_apply.grid(row=15, column=3, pady=(0, 10), sticky="e")

    def hide_message(self):
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()
        self._button_cancel_apply.grid_forget()
        self._button_confirm_apply.grid_forget()

    def _on_button_cancel_apply_clicked(self):
        self.apply_option = ""
        self.hide_message()

    def set_visibility_download_confirm_buttons(self, visibility):
        if visibility is True:
            self._button_cancel_download.grid(row=16, column=2, pady=(0, 10), sticky="e")
            self._button_confirm_download.grid(row=16, column=3, pady=(0, 10), sticky="e")
        else:
            self._button_cancel_download.grid_forget()
            self._button_confirm_download.grid_forget()

    def on_button_download_clicked(self):
        self.hide_message()
        self.set_visibility_buttons_frame(False)
        self.set_visibility_download_confirm_buttons(False)


