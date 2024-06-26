import customtkinter as ctk

from helper.gui import set_textbox_value
from helper.datetime import to_duration_string, to_date_string

class VideoInfoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._parent = master
        self._root_data = master._root_data
        self.grid_columnconfigure((1), weight=1)
        self._data = {}

        self._label_title = ctk.CTkLabel(self, text="Title")
        self._label_title.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="nw")

        self._textbox_title = ctk.CTkTextbox(self)
        self._textbox_title.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew", columnspan=2)
        self._textbox_title.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_uploader = ctk.CTkLabel(self, text="Owner")
        self._label_uploader.grid(row=1, column=0, padx=(10, 0), pady=(0, 5), sticky="nsw")

        self._textbox_uploader = ctk.CTkTextbox(self)
        self._textbox_uploader.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="ew", columnspan=2)
        self._textbox_uploader.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_upload_date = ctk.CTkLabel(self, text="Upload date")
        self._label_upload_date.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky="nsw")

        self._textbox_upload_date_value = ctk.CTkTextbox(self)
        self._textbox_upload_date_value.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w", columnspan=2)
        self._textbox_upload_date_value.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_duration = ctk.CTkLabel(self, text="Duration")
        self._label_duration.grid(row=3, column=0, padx=(10, 0), pady=(0, 5), sticky="nsw")

        self._textbox_duration_string = ctk.CTkTextbox(self)
        self._textbox_duration_string.grid(row=3, column=1, padx=10, pady=(0, 5), sticky="w", columnspan=2)
        self._textbox_duration_string.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_url = ctk.CTkLabel(self, text="URL")
        self._label_url.grid(row=4, column=0, padx=(10, 0), pady=(0, 5), sticky="nsw")

        self._textbox_url = ctk.CTkTextbox(self)
        self._textbox_url.grid(row=4, column=1, padx=10, pady=(0, 5), sticky="ew", columnspan=2)
        self._textbox_url.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_resolution = ctk.CTkLabel(self, text="Resolution")
        self._label_resolution.grid(row=5, column=0, padx=(10, 0), pady=(0, 5), sticky="nsw")

        self._textbox_resolution = ctk.CTkTextbox(self)
        self._textbox_resolution.grid(row=5, column=1, padx=10, pady=(0, 5), sticky="ew", columnspan=2)
        self._textbox_resolution.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_add = ctk.CTkButton(self, text="Add", command=self._on_add_url)
        self._button_add.grid(row=6, column=2, padx=10, pady=(0, 10), sticky="w")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
    
    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    def display(self, data):
        set_textbox_value(self._textbox_title, data.get("title") or "")
        set_textbox_value(self._textbox_uploader, data.get("uploader") or "")
        set_textbox_value(self._textbox_upload_date_value, to_date_string(data.get("upload_date")) or "")
        set_textbox_value(self._textbox_duration_string, to_duration_string(int(data.get("duration"))) or "")
        set_textbox_value(self._textbox_url, data.get("original_url") or "")
        set_textbox_value(self._textbox_resolution, data.get("resolution") or "")

    def clear_video_info(self):
        set_textbox_value(self._textbox_title, "")
        set_textbox_value(self._textbox_uploader, "")
        set_textbox_value(self._textbox_upload_date_value, "")
        set_textbox_value(self._textbox_duration_string, "")
        set_textbox_value(self._textbox_url, "")
        set_textbox_value(self._textbox_resolution, "")

    def _on_add_url(self):
        data = {
            "title": self._data.get("title") or "",
            "uploader": self._data.get("uploader") or "",
            "upload_date": self._data.get("upload_date") or "",
            "duration": self._data.get("duration") or "",
            "duration_string": to_duration_string(int(self._data["duration"])),
            "webpage_url": self._data.get("webpage_url") or "",
            "original_url": self._data.get("original_url") or "",
            "resolution": self._data.get("resolution") or "",
            "cookies": self._data["cookies"],
            "selected": True,
            "status": "ready"
        }
        result = self.root_data.on_add_urls([data])

        if result["added"] == 1:
            message = f"Successfully added \"{data['title']}\"."
        else:
            message = f"\"{data['title']}\" has already been added."
        
        set_textbox_value(self._parent._textbox_message, message)
        self._parent._show_message()
        self.clear_video_info()
        self.grid_forget()
        

