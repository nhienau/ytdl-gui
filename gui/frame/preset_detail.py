import customtkinter as ctk
from pathlib import Path
import tkinter as tk

from .input_size_limit import InputSizeLimitFrame
from helper.gui import set_textbox_value
from helper.get_download_folder import get_download_folder

class PresetDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)
        self._parent = master
        self._root_data = master.root_data
        self._preset = master.root_data.current_preset

        self._label_preset = ctk.CTkLabel(self, text="Preset")
        self._label_preset.grid(row=0, column=0, pady=(0, 10), sticky="nsw")

        self._var_preset_name = ctk.StringVar(value="")
        self._var_preset_name.trace("w", master.enable_button_save)
        self._entry_preset_name = ctk.CTkEntry(self, textvariable=self._var_preset_name)
        self._entry_preset_name.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_download_option = ctk.CTkLabel(self, text="Include")
        self._label_download_option.grid(row=1, column=0, pady=(0, 10), sticky="nsw")

        self._download_option_value = ctk.StringVar(value="Video + audio")
        self._download_option_value.trace("w", master.enable_button_save)
        self._combobox_download_option = ctk.CTkComboBox(self, values=["Video + audio", "Video only", "Audio only"], state="readonly", variable=self._download_option_value, command=self._on_download_option_change)
        self._combobox_download_option.grid(row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_download_option.set("Video + audio")

        self._split_video_audio = ctk.BooleanVar(value=False)
        self._split_video_audio.trace("w", master.enable_button_save)
        self._checkbox_split_video_audio = ctk.CTkCheckBox(self, text="Split into separate files", onvalue=True, offvalue=False, variable=self._split_video_audio)
        self._checkbox_split_video_audio.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_chapter = ctk.CTkLabel(self, text="Chapter")
        self._label_chapter.grid(row=3, column=0, pady=(0, 10), sticky="nw")

        self._split_by_chapters = ctk.BooleanVar(value=False)
        self._split_by_chapters.trace("w", master.enable_button_save)
        self._checkbox_chapter = ctk.CTkCheckBox(self, text="Split video by chapters", onvalue=True, offvalue=False, variable=self._split_by_chapters)
        self._checkbox_chapter.grid(row=3, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        
        self._label_resolution = ctk.CTkLabel(self, text="Resolution")
        self._label_resolution.grid(row=4, column=0, pady=(0, 10), sticky="nw")

        self._resolution = ctk.StringVar(value="Best")
        self._resolution.trace("w", master.enable_button_save)
        self._combobox_resolution = ctk.CTkComboBox(self, values=["Best", "2160p (4K)", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"], state="readonly", variable=self._resolution)
        self._combobox_resolution.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_size_limit = ctk.CTkLabel(self, text="File size")
        self._label_size_limit.grid(row=5, column=0, pady=(0, 10), sticky="nw")

        self._size_limit = ctk.StringVar(value="Best")
        self._size_limit.trace("w", master.enable_button_save)
        self._combobox_size_limit = ctk.CTkComboBox(self, values=["Best", "Custom"], state="readonly", variable=self._size_limit, command=self._on_size_limit_option_change)
        self._combobox_size_limit.grid(row=5, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._frame_size_limit = InputSizeLimitFrame(self)
        self._frame_size_limit.size_limit.trace("w", self._handle_size_limit_change)

        self._label_subtitle = ctk.CTkLabel(self, text="Subtitle")
        self._label_subtitle.grid(row=7, column=0, pady=(0, 10), sticky="nw")

        self._subtitle = ctk.BooleanVar(value=False)
        self._subtitle.trace("w", master.enable_button_save)
        self._checkbox_subtitle = ctk.CTkCheckBox(self, text="Download subtitle (if available)", onvalue=True, offvalue=False, variable=self._subtitle)
        self._checkbox_subtitle.grid(row=7, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_thumbnail = ctk.CTkLabel(self, text="Thumbnail")
        self._label_thumbnail.grid(row=8, column=0, pady=(0, 10), sticky="nw")

        self._thumbnail = ctk.BooleanVar(value=False)
        self._thumbnail.trace("w", master.enable_button_save)
        self._checkbox_thumbnail = ctk.CTkCheckBox(self, text="Save thumbnail (if available)", onvalue=True, offvalue=False, variable=self._thumbnail)
        self._checkbox_thumbnail.grid(row=8, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_output_folder = ctk.CTkLabel(self, text="Output folder")
        self._label_output_folder.grid(row=9, column=0, pady=(0, 10), sticky="nw")

        self._output_path = ctk.StringVar(value="")
        self._output_path.trace("w", master.enable_button_save)
        self._input_output_folder = ctk.CTkEntry(self, state="disabled", textvariable=self._output_path)
        self._input_output_folder.grid(row=9, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=2)

        self._button_browse = ctk.CTkButton(self, text="Browse", width=24, command=self._on_browse_dir_clicked)
        self._button_browse.grid(row=9, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

        self._textbox_message = ctk.CTkTextbox(self)
        self._textbox_message.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_cancel = ctk.CTkButton(self, text="Cancel", width=24, command=master.on_new_preset_cancel_clicked)

        self._button_ok = ctk.CTkButton(self, text="OK", width=24, command=self._on_new_preset_submit)

        self._button_cancel_delete = ctk.CTkButton(self, text="Cancel", width=24, command=self._on_cancel_delete_clicked)

        self._button_confirm_delete = ctk.CTkButton(self, text="OK", width=24, command=lambda: master.on_preset_confirm_delete_clicked(self._preset))

        # For toggling combobox state
        self._combobox_elements = [self._combobox_download_option, self._combobox_resolution, self._combobox_size_limit]

        self.display(self.root_data.current_preset)
        master._button_save_preset.configure(state="disabled")

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    @property
    def preset(self):
        return self._preset

    @preset.setter
    def preset(self, preset):
        self._preset = preset
        if preset is not None:
            self.display(self._preset)

    def get_form_data(self):
        return {
            "name": self._var_preset_name.get().strip(),
            "include_video": "video" in self._download_option_value.get().strip().lower(),
            "include_audio": "audio" in self._download_option_value.get().strip().lower(),
            "split_video_and_audio": self._split_video_audio.get() if all(el in self._download_option_value.get().lower() for el in ["video", "audio"]) else False,
            "split_by_chapters": self._split_by_chapters.get(),
            "resolution": None if self._resolution.get().lower() == "best" else self._resolution.get(),
            "max_file_size": None if self._size_limit.get().lower() == "best" else self._frame_size_limit.size_limit.get(),
            "subtitle": self._subtitle.get(),
            "thumbnail": self._thumbnail.get(),
            "output_path": self._output_path.get(),
            "editable": True if self._preset is None else self._preset["editable"]
        }

    def display(self, preset):
        elements_state = "normal" if preset["editable"] is True else "disabled"
        self.set_elements_state(elements_state)

        # Temporarily set combobox values back to "normal" since we are displaying preset info (therefore modifying combobox values)
        for element in self._combobox_elements:
            element.configure(state="normal")

        self._var_preset_name.set(preset["name"])
        if preset["include_video"] and preset["include_audio"]:
            self._combobox_download_option.set("Video + audio")
            self._checkbox_split_video_audio.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
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
            self._frame_size_limit.grid(row=6, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)
            self._frame_size_limit.size_limit.set(preset["max_file_size"])

        self._subtitle.set(preset["subtitle"])
        self._thumbnail.set(preset["thumbnail"])
        self._output_path.set(preset["output_path"])
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()
        self.set_visibility_button_cancel_and_ok(False)
        self._button_cancel_delete.grid_forget()
        self._button_confirm_delete.grid_forget()

        # Set comboboxes state back to "readonly"/"normal" after modifying them
        combobox_state = "readonly" if elements_state == "normal" else "disabled"
        for element in self._combobox_elements:
            element.configure(state=combobox_state)

    def set_elements_state(self, state):
        for element in [self._entry_preset_name, self._checkbox_split_video_audio, self._checkbox_chapter, self._frame_size_limit._input_size_limit, self._checkbox_subtitle, self._checkbox_thumbnail]:
            element.configure(state=state)

        combobox_state = "readonly" if state == "normal" else "disabled"
        for element in self._combobox_elements:
            element.configure(state=combobox_state)

    def set_visibility_button_cancel_and_ok(self, visibility):
        if visibility is True:
            self._button_cancel.grid(row=11, column=2, pady=(0, 10), sticky="e")
            self._button_ok.grid(row=11, column=3, padx=(5, 0), pady=(0, 10), sticky="we")
        else:
            self._button_cancel.grid_forget()
            self._button_ok.grid_forget()

    def clear_all_input(self):
        self._var_preset_name.set("")
        self._combobox_download_option.set("Video + audio")
        self._checkbox_split_video_audio.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._split_video_audio.set(False)
        self._split_by_chapters.set(False)
        self._resolution.set("Best")
        self._size_limit.set("Best")
        self._frame_size_limit.grid_forget()
        self._subtitle.set(False)
        self._thumbnail.set(False)
        self._output_path.set("")
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()

    def _on_download_option_change(self, value):
        if value == "Video + audio":
            self._checkbox_split_video_audio.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        else:
            self._checkbox_split_video_audio.grid_forget()

    def _on_size_limit_option_change(self, value):
        if value == "Best":
            self._frame_size_limit.grid_forget()
        else:
            self._frame_size_limit.grid(row=6, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)
        
    def _on_browse_dir_clicked(self):
        dir_path = tk.filedialog.askdirectory(parent=self._parent, title="Change output folder to...", initialdir=get_download_folder())
        if dir_path == "" or dir_path == self._output_path:
            return
        self._output_path.set(dir_path)

    def _on_new_preset_submit(self):
        self._textbox_message.grid_forget()
        validation = self.validate_form_data()
        
        if validation["valid"] is True:
            preset = self.get_form_data()
            self._parent.create_new_preset(preset)
        else:
            set_textbox_value(self._textbox_message, validation["error_message"])
            self._textbox_message.grid(row=10, column=0, pady=(0, 10), sticky="ew", columnspan=4)

    def show_confirm_delete_message(self, preset):
        set_textbox_value(self._textbox_message, f"Preset \"{preset['name']}\" will be deleted.")
        self._textbox_message.grid(row=10, column=0, pady=(0, 10), sticky="ew", columnspan=4)
        self._button_cancel_delete.grid(row=12, column=2, pady=(0, 10), sticky="e")
        self._button_confirm_delete.grid(row=12, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

    def _on_cancel_delete_clicked(self):
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()
        self._button_cancel_delete.grid_forget()
        self._button_confirm_delete.grid_forget()

    def _handle_size_limit_change(self, _, __, ___):
        set_textbox_value(self._textbox_message, "")
        self._textbox_message.grid_forget()
        value = self._frame_size_limit.size_limit.get()

        try:
            value = float(value)
        except:
            set_textbox_value(self._textbox_message, "File size limit must be a float number.")
            self._textbox_message.grid(row=10, column=0, pady=(0, 10), sticky="ew", columnspan=4)

    def validate_form_data(self):
        valid = True
        error_message = ""
        output_path = self._output_path.get()
        path = Path(output_path)
        if self._var_preset_name.get().strip() == "":
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

    def _on_update_preset_clicked(self):
        self._textbox_message.grid_forget()
        validation = self.validate_form_data()
        
        if validation["valid"] is True:
            preset = self.get_form_data()
            preset["id"] = self.preset["id"]
            self._parent.update_preset(preset)
        else:
            set_textbox_value(self._textbox_message, validation["error_message"])
            self._textbox_message.grid(row=10, column=0, pady=(0, 10), sticky="ew", columnspan=4)


