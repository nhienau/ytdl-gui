import customtkinter as ctk

from .input_size_limit import InputSizeLimitFrame

class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)

        self._label_preset = ctk.CTkLabel(self, text="Preset")
        self._label_preset.grid(row=0, column=0, pady=(0, 10), sticky="nsw")

        self._preset_value = ctk.StringVar(value="Best")
        self._preset_value.trace('w', self._on_preset_change)
        self._combobox_preset = ctk.CTkComboBox(self, values=["Best", "Best (1080p)", "Best (720p)"], state="readonly", variable=self._preset_value)
        self._combobox_preset.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_preset.set("Best")

        self._label_title = ctk.CTkLabel(self, text="Title")
        self._label_title.grid(row=1, column=0, pady=(0, 10), sticky="nw")

        self._textbox_title = ctk.CTkTextbox(self)
        self._textbox_title.grid(row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="ew", columnspan=3)
        self._textbox_title.insert("0.0", "Test")
        self._textbox_title.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_download_option = ctk.CTkLabel(self, text="Include")
        self._label_download_option.grid(row=2, column=0, pady=(0, 10), sticky="nsw")

        self._download_option_value = ctk.StringVar(value="Video + audio")
        self._combobox_download_option = ctk.CTkComboBox(self, values=["Video + audio", "Video only", "Audio only"], state="readonly", variable=self._download_option_value) # "Custom"
        self._combobox_download_option.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_download_option.set("Video + audio")

        self._split_video_audio = ctk.BooleanVar(value=True)
        self._checkbox_split_video_audio = ctk.CTkCheckBox(self, text="Split into separate files", onvalue=True, offvalue=False, variable=self._split_video_audio) # command
        self._checkbox_split_video_audio.grid(row=3, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_chapter = ctk.CTkLabel(self, text="Chapter")
        self._label_chapter.grid(row=4, column=0, pady=(0, 10), sticky="nw")

        self._split_by_chapters = ctk.BooleanVar(value=True)
        self._checkbox_chapter = ctk.CTkCheckBox(self, text="Split video by chapters", onvalue=True, offvalue=False, variable=self._split_by_chapters) # command
        self._checkbox_chapter.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        
        self._label_resolution = ctk.CTkLabel(self, text="Resolution")
        self._label_resolution.grid(row=5, column=0, pady=(0, 10), sticky="nw")

        self._resolution = ctk.StringVar(value="Best")
        self._combobox_resolution = ctk.CTkComboBox(self, values=["Best", "2160p (4K)", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"], state="readonly", variable=self._resolution)
        self._combobox_resolution.grid(row=5, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_resolution.set("Best")

        self._label_size_limit = ctk.CTkLabel(self, text="File size")
        self._label_size_limit.grid(row=6, column=0, pady=(0, 10), sticky="nw")

        self._size_limit = ctk.StringVar(value="Best")
        self._combobox_size_limit = ctk.CTkComboBox(self, values=["Best", "Custom"], state="readonly", variable=self._size_limit)
        self._combobox_size_limit.grid(row=6, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self._combobox_size_limit.set("Best")

        self._frame_size_limit = InputSizeLimitFrame(self)
        self._frame_size_limit.grid(row=7, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)

        self._label_subtitle = ctk.CTkLabel(self, text="Subtitle")
        self._label_subtitle.grid(row=8, column=0, pady=(0, 10), sticky="nw")

        self._subtitle = ctk.BooleanVar(value=False)
        self._checkbox_subtitle = ctk.CTkCheckBox(self, text="Download subtitle (if available)", onvalue=True, offvalue=False, variable=self._subtitle) # command, variable
        self._checkbox_subtitle.grid(row=8, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_thumbnail = ctk.CTkLabel(self, text="Thumbnail")
        self._label_thumbnail.grid(row=9, column=0, pady=(0, 10), sticky="nw")

        self._thumbnail = ctk.BooleanVar(value=True)
        self._checkbox_thumbnail = ctk.CTkCheckBox(self, text="Save thumbnail (if available)", onvalue=True, offvalue=False, variable=self._thumbnail) # command, variable
        self._checkbox_thumbnail.grid(row=9, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_sponsorblock = ctk.CTkLabel(self, text="Sponsorblock")
        self._label_sponsorblock.grid(row=10, column=0, pady=(0, 10), sticky="nw")

        self._sponsorblock = ctk.BooleanVar(value=True)
        self._checkbox_sponsorblock = ctk.CTkCheckBox(self, text="Remove sponsor sections", onvalue=True, offvalue=False, variable=self._sponsorblock) # command, variable
        self._checkbox_sponsorblock.grid(row=10, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self._label_output_folder = ctk.CTkLabel(self, text="Output folder")
        self._label_output_folder.grid(row=11, column=0, pady=(0, 10), sticky="nw")

        self._output_path = ctk.StringVar(value="")
        self._input_output_folder = ctk.CTkEntry(self, state="disabled", textvariable=self._output_path)
        self._input_output_folder.grid(row=11, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=2)

        self._button_browse = ctk.CTkButton(self, text="Browse", width=24)
        self._button_browse.grid(row=11, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

        self._button_apply_to_all = ctk.CTkButton(self, text="Apply to all", width=24)
        self._button_apply_to_all.grid(row=12, column=2, pady=(0, 10), sticky="e")

        self._button_apply_single = ctk.CTkButton(self, text="Apply", width=24, command=self._get_form_data)
        self._button_apply_single.grid(row=12, column=3, pady=(0, 10), sticky="e")

    def _get_form_data(self):
        data = {
            "preset": self._preset_value.get(),

        }
        print(data)

    def _on_preset_change(self, _, __, ___):
        print(self._preset_value.get())


