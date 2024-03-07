import customtkinter as ctk

from .input_size_limit import InputSizeLimitFrame

class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)

        self.label_preset = ctk.CTkLabel(self, text="Preset")
        self.label_preset.grid(row=0, column=0, pady=(0, 10), sticky="nsw")

        self.preset_value = ctk.StringVar(value="Best")
        self.preset_value.trace('w', self.on_preset_change)
        self.combobox_preset = ctk.CTkComboBox(self, values=["Best", "Best (1080p)", "Best (720p)"], state="readonly", variable=self.preset_value)
        self.combobox_preset.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self.combobox_preset.set("Best")

        self.label_title = ctk.CTkLabel(self, text="Title")
        self.label_title.grid(row=1, column=0, pady=(0, 10), sticky="nw")

        self.textbox_title = ctk.CTkTextbox(self)
        self.textbox_title.grid(row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="ew", columnspan=3)
        self.textbox_title.insert("0.0", text="lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao lmao")
        self.textbox_title.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self.label_download_option = ctk.CTkLabel(self, text="Include")
        self.label_download_option.grid(row=2, column=0, pady=(0, 10), sticky="nsw")

        self.download_option_value = ctk.StringVar(value="Video + audio")
        self.combobox_download_option = ctk.CTkComboBox(self, values=["Video + audio", "Video only", "Audio only"], state="readonly", variable=self.download_option_value) # "Custom"
        self.combobox_download_option.grid(row=2, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self.combobox_download_option.set("Video + audio")

        self.split_video_audio = ctk.StringVar(value=True)
        self.checkbox_split_video_audio = ctk.CTkCheckBox(self, text="Split into separate files", onvalue=True, offvalue=False, variable=self.split_video_audio) # command
        self.checkbox_split_video_audio.grid(row=3, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self.label_chapter = ctk.CTkLabel(self, text="Chapter")
        self.label_chapter.grid(row=4, column=0, pady=(0, 10), sticky="nw")

        self.split_by_chapters = ctk.StringVar(value=True)
        self.checkbox_chapter = ctk.CTkCheckBox(self, text="Split video by chapters", onvalue=True, offvalue=False, variable=self.split_by_chapters) # command
        self.checkbox_chapter.grid(row=4, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        
        self.label_resolution = ctk.CTkLabel(self, text="Resolution")
        self.label_resolution.grid(row=5, column=0, pady=(0, 10), sticky="nw")

        self.resolution = ctk.StringVar(value="Best")
        self.combobox_resolution = ctk.CTkComboBox(self, values=["Best", "2160p (4K)", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"], state="readonly", variable=self.resolution)
        self.combobox_resolution.grid(row=5, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self.combobox_resolution.set("Best")

        self.label_size_limit = ctk.CTkLabel(self, text="File size")
        self.label_size_limit.grid(row=6, column=0, pady=(0, 10), sticky="nw")

        self.size_limit = ctk.StringVar(value="Best")
        self.combobox_size_limit = ctk.CTkComboBox(self, values=["Best", "Custom"], state="readonly", variable=self.size_limit)
        self.combobox_size_limit.grid(row=6, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)
        self.combobox_size_limit.set("Best")

        self.frame_size_limit = InputSizeLimitFrame(self)
        self.frame_size_limit.grid(row=7, column=1, padx=(10, 0), pady=(0, 10), sticky="w", columnspan=3)

        self.label_subtitle = ctk.CTkLabel(self, text="Subtitle")
        self.label_subtitle.grid(row=8, column=0, pady=(0, 10), sticky="nw")

        self.subtitle = ctk.StringVar(value=False)
        self.checkbox_subtitle = ctk.CTkCheckBox(self, text="Download subtitle (if available)", onvalue=True, offvalue=False, variable=self.subtitle) # command, variable
        self.checkbox_subtitle.grid(row=8, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self.label_thumbnail = ctk.CTkLabel(self, text="Thumbnail")
        self.label_thumbnail.grid(row=9, column=0, pady=(0, 10), sticky="nw")

        self.thumbnail = ctk.StringVar(value=True)
        self.checkbox_thumbnail = ctk.CTkCheckBox(self, text="Save thumbnail (if available)", onvalue=True, offvalue=False, variable=self.thumbnail) # command, variable
        self.checkbox_thumbnail.grid(row=9, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self.label_sponsorblock = ctk.CTkLabel(self, text="Sponsorblock")
        self.label_sponsorblock.grid(row=10, column=0, pady=(0, 10), sticky="nw")

        self.sponsorblock = ctk.StringVar(value=True)
        self.checkbox_sponsorblock = ctk.CTkCheckBox(self, text="Remove sponsor sections", onvalue=True, offvalue=False, variable=self.sponsorblock) # command, variable
        self.checkbox_sponsorblock.grid(row=10, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=3)

        self.label_output_folder = ctk.CTkLabel(self, text="Output folder")
        self.label_output_folder.grid(row=11, column=0, pady=(0, 10), sticky="nw")

        self.output_path = ctk.StringVar(value="")
        self.input_output_folder = ctk.CTkEntry(self, state="disabled", textvariable=self.output_path)
        self.input_output_folder.grid(row=11, column=1, padx=(10, 0), pady=(0, 10), sticky="we", columnspan=2)

        self.button_browse = ctk.CTkButton(self, text="Browse", width=24)
        self.button_browse.grid(row=11, column=3, padx=(5, 0), pady=(0, 10), sticky="we")

        self.button_apply_to_all = ctk.CTkButton(self, text="Apply to all", width=24)
        self.button_apply_to_all.grid(row=12, column=2, pady=(0, 10), sticky="e")

        self.button_apply_single = ctk.CTkButton(self, text="Apply", width=24, command=self.get_form_data)
        self.button_apply_single.grid(row=12, column=3, pady=(0, 10), sticky="e")

    def get_form_data(self):
        data = {
            "preset": self.preset_value.get(),

        }
        print(data)

    def on_preset_change(self, _, __, ___):
        print(self.preset_value.get())

