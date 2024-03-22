import customtkinter as ctk

from helper.gui import set_textbox_value

class PlaylistDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((1), weight=1)
        self._data = {}
        self.add_option = ""

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

        self._textbox_additional_information = ctk.CTkTextbox(self)
        self._textbox_additional_information.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_add_selected = ctk.CTkButton(self, text="Add selected", width=24, command=lambda: master.on_add_entries_click(add_all=False))
        self._button_add_selected.grid(row=5, column=2, pady=(0, 5), sticky="e")

        self._button_add_all = ctk.CTkButton(self, text="Add all", width=24, command=master.on_add_entries_click)
        self._button_add_all.grid(row=5, column=3, pady=(0, 5), sticky="e")

        self._textbox_confirm_add = ctk.CTkTextbox(self)
        self._textbox_confirm_add.configure(height=20, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._button_confirm_add = ctk.CTkButton(self, text="OK", width=24, command=master.add_entries)

        self._button_cancel_add = ctk.CTkButton(self, text="Cancel", width=24, command=self.hide_confirm_message)
    
    def set_data(self, data):
        self._data = data

    def display(self, data):
        self.hide_additional_message()
        self.hide_confirm_message()
        set_textbox_value(self._textbox_playlist_title, data["title"])
        set_textbox_value(self._textbox_playlist_uploader, data["uploader"])
        set_textbox_value(self._textbox_url, data["original_url"])

        if (data["available_count"] < data["playlist_count"]):
            total_str = f"{data['playlist_count']} (available: {data['available_count']})"
            set_textbox_value(self._textbox_playlist_count_value, total_str)
        else:
            set_textbox_value(self._textbox_playlist_count_value, data["playlist_count"])
        
        state = "normal" if len(data["entries"]) > 0 else "disabled"
        self._button_add_selected.configure(state=state)
        self._button_add_all.configure(state=state)

    def show_confirm_message(self, message, show_button = True):
        set_textbox_value(self._textbox_confirm_add, message)
        self._textbox_confirm_add.grid(row=6, column=0, pady=(0, 5), sticky="ew", columnspan=4)
        if show_button is True:
            self._button_confirm_add.grid(row=7, column=2, pady=(0, 5), sticky="we")
            self._button_cancel_add.grid(row=7, column=3, pady=(0, 5), sticky="we")
    
    def hide_confirm_message(self):
        self.add_option = ""
        set_textbox_value(self._textbox_confirm_add, "")
        self._textbox_confirm_add.grid_forget()
        self._button_confirm_add.grid_forget()
        self._button_cancel_add.grid_forget()

    def show_additional_message(self, message):
        set_textbox_value(self._textbox_additional_information, message)
        self._textbox_additional_information.grid(row=4, column=0, pady=(0, 5), sticky="ew", columnspan=4)
    
    def hide_additional_message(self):
        set_textbox_value(self._textbox_additional_information, "")
        self._textbox_additional_information.grid_forget()


