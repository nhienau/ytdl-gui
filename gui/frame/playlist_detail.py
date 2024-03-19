import customtkinter as ctk

from helper.gui import set_textbox_value

class PlaylistDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)
        self._data = {}

        self._label_playlist_title = ctk.CTkLabel(self, text="Title")
        self._label_playlist_title.grid(row=0, column=0, pady=(0, 5), sticky="nsw")

        self._textbox_playlist_title = ctk.CTkTextbox(self)
        self._textbox_playlist_title.grid(row=0, column=1, padx=(10, 0), pady=(0, 5), sticky="ew", columnspan=3)
        self._textbox_playlist_title.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_playlist_uploader = ctk.CTkLabel(self, text="Owner")
        self._label_playlist_uploader.grid(row=1, column=0, pady=(0, 5), sticky="nsw", columnspan=3)

        self._textbox_playlist_uploader = ctk.CTkTextbox(self)
        self._textbox_playlist_uploader.grid(row=1, column=1, padx=(10, 0), pady=(0, 5), sticky="ew", columnspan=3)
        self._textbox_playlist_uploader.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_playlist_count = ctk.CTkLabel(self, text="Total")
        self._label_playlist_count.grid(row=2, column=0, pady=(0, 5), sticky="nsw")

        self._textbox_playlist_count_value = ctk.CTkTextbox(self)
        self._textbox_playlist_count_value.grid(row=2, column=1, padx=(10, 0), pady=(0, 5), sticky="w", columnspan=3)
        self._textbox_playlist_count_value.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._label_playlist_url = ctk.CTkLabel(self, text="URL")
        self._label_playlist_url.grid(row=3, column=0, pady=(0, 5), sticky="nsw")

        self._textbox_url = ctk.CTkTextbox(self)
        self._textbox_url.grid(row=3, column=1, padx=(10, 0), pady=(0, 5), sticky="ew", columnspan=3)
        self._textbox_url.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_add_selected = ctk.CTkButton(self, text="Add selected", width=24)
        self._button_add_selected.grid(row=4, column=2, pady=(0, 5), sticky="e")

        self._button_add_all = ctk.CTkButton(self, text="Add all", width=24)
        self._button_add_all.grid(row=4, column=3, pady=(0, 5), sticky="e")
    
    def set_data(self, data):
        self._data = data

    def display(self, data):
        set_textbox_value(self._textbox_playlist_title, data["title"])
        set_textbox_value(self._textbox_playlist_uploader, data["uploader"])
        set_textbox_value(self._textbox_playlist_count_value, data["playlist_count"])
        set_textbox_value(self._textbox_url, data["original_url"])
        
        state = "normal" if len(data["entries"]) > 0 else "disabled"
        self._button_add_selected.configure(state=state)
        self._button_add_all.configure(state=state)


