import customtkinter as ctk
import tkinter as tk

from downloader.extractor import extract

class AddUrlWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ytdl-gui")
        self.geometry("1152x648")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)

        self.label_url = ctk.CTkLabel(self, text="URL")
        self.label_url.grid(row=0, column=4, pady=(10, 10))

        self.entry_var = tk.StringVar(value="")
        self.entry_url = ctk.CTkEntry(self, textvariable=self.entry_var)
        self.entry_url.grid(row=0, column=5, pady=(10, 10), sticky="we", columnspan=10)

        self.button_get_info = ctk.CTkButton(self, text="Get info", width=24, command=self.on_extract_url)
        self.button_get_info.grid(row=0, column=15, pady=(10, 10))

        self.label_error_message = ctk.CTkLabel(self)

    def show_error_message(self, message):
        self.label_error_message.grid(row=1, column=5, pady=(0, 10), sticky="w", columnspan=10)
        self.label_error_message.configure(text=message)

    def hide_error_message(self):
        self.label_error_message.grid_forget()

    def on_extract_url(self):
        self.hide_error_message()
        url = self.entry_var.get()
        if url == '':
            self.show_error_message("Please input")
        result = extract(url)
        print(result["_type"])
        result = {
            "url": result["original_url"],
            "title": result["fulltitle"],
            "uploader": result["uploader"],
            "upload_date": result["upload_date"],
            "extractor_key": result["extractor_key"],
            "duration": result["duration"],
            "duration_string": result["duration_string"],
            "width": result["width"],
            "height": result["height"],
            "resolution": result["resolution"],
            "fps": result["fps"],
        }
        print(result)