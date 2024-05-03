import customtkinter as ctk

class DownloadInfoFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self._textbox = ctk.CTkTextbox(self)
        self._textbox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self._textbox.configure(height=140, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent", wrap="word")

    def display(self, download_info):
        self._textbox.configure(state="normal")
        self._textbox.delete("0.0", "end")
        self._textbox.insert("1.0", text=f"Pending: {download_info['pending']}\n")
        self._textbox.insert("2.0", text=f"Finished: {download_info['finished']}\n")
        self._textbox.insert("3.0", text=f"Error: {download_info['error']}\n")
        if download_info["downloading_title"] != "":
            stopped = " (Stopped)" if download_info["stopped"] else ""
            self._textbox.insert("4.0", text=f"Downloading \"{download_info['downloading_title']}\"{stopped}")
        self._textbox.configure(state="disabled")


