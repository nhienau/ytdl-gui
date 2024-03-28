import customtkinter as ctk

from helper.gui import set_textbox_value
from helper.datetime import to_duration_string, to_date_string

class VideoInfoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._parent = master
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

    def display(self, data):
        set_textbox_value(self._textbox_title, data["title"])
        set_textbox_value(self._textbox_uploader, data["uploader"])
        set_textbox_value(self._textbox_upload_date_value, to_date_string(data["upload_date"]))
        set_textbox_value(self._textbox_duration_string, to_duration_string(int(data["duration"])))
        set_textbox_value(self._textbox_url, data["original_url"])
        set_textbox_value(self._textbox_resolution, data["resolution"])

    def clear_text(self):
        set_textbox_value(self._textbox_title, "")
        set_textbox_value(self._textbox_uploader, "")
        set_textbox_value(self._textbox_upload_date_value, "")
        set_textbox_value(self._textbox_duration_string, "")
        set_textbox_value(self._textbox_url, "")
        set_textbox_value(self._textbox_resolution, "")

    def _on_add_url(self):
        data = {
            "title": self._data["title"],
            "uploader": self._data["uploader"],
            "upload_date": self._data["upload_date"],
            "duration": self._data["duration"],
            "duration_string": to_duration_string(int(self._data["duration"])),
            "webpage_url": self._data["webpage_url"],
            "original_url": self._data["original_url"],
            "resolution": self._data["resolution"],
            "cookies": self._data["cookies"],
            "selected": True,
        }
        on_add_urls = self._parent.callbacks["on_add_urls"]
        result = on_add_urls([data])

        if result["added"] == 1:
            message = f"Successfully added \"{data['title']}\"."
        else:
            message = f"\"{data['title']}\" has already been added."
        
        self._parent.on_add_urls_callback(message)
        self.clear_text()
        self.grid_forget()
        

