import customtkinter as ctk
import threading
import tkinter as tk
import traceback

from downloader.extractor import extract
from gui.frame.cookies import LoadCookiesFrame
from gui.frame.video_info import VideoInfoFrame
from gui.frame.playlist_info import PlaylistInfoFrame
from helper.gui import set_textbox_value

class AddUrlWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ytdl-gui")
        self.geometry("1024x576")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(5, weight=1)
        self._root_data = list(args)[0]._parent

        self._thread = None
        self._stop_event = threading.Event()
        self._cookies_from_browser = ""

        self._label_url = ctk.CTkLabel(self, text="URL")
        self._label_url.grid(row=0, column=1, pady=(10, 10), sticky="e")

        self._entry_var = ctk.StringVar(value="")
        self._entry_url = ctk.CTkEntry(self, textvariable=self._entry_var)
        self._entry_url.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="we", columnspan=16)
        self._entry_url.bind("<Return>", lambda e: self._on_get_info())

        self._button_get_info = ctk.CTkButton(self, text="Get info", width=24, command=self._on_get_info)
        self._button_get_info.grid(row=0, column=18, pady=(10, 10), sticky="w")

        self._label_instruction = ctk.CTkLabel(self, text="Let's start by pasting a URL. A valid URL can be a single video, a playlist or a channel.")
        self._label_instruction.grid(row=1, column=1, sticky="we", columnspan=18)

        self._textbox_message = ctk.CTkTextbox(self)
        self._textbox_message.configure(height=48, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._load_cookies_frame = LoadCookiesFrame(self)
        self._video_info_frame = VideoInfoFrame(self)
        self._playlist_info_frame = PlaylistInfoFrame(self)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    def _show_message(self):
        self._textbox_message.grid(row=2, column=2, pady=(0, 10), sticky="we", columnspan=16)

    def _hide_message(self):
        self._textbox_message.configure(state="normal")
        self._textbox_message.delete("0.0", "end")
        self._textbox_message.configure(state="disabled")
        self._textbox_message.grid_forget()

    def _set_controls_state(self, state):
        self._entry_url.configure(state=state)
        self._button_get_info.configure(state=state)

    def _on_get_info(self):
        self._hide_message()
        self._load_cookies_frame.grid_forget()
        url = self._entry_var.get().strip()
        if url == '':
            return
        
        self._label_instruction.grid_forget()
        self._video_info_frame.grid_forget()
        self._playlist_info_frame.grid_forget()
        self._playlist_info_frame.clear_frame()

        loading_message = "Loading"
        if self._cookies_from_browser != "":
            loading_message += f" (cookies: {self._cookies_from_browser})"
        loading_message += "..."

        set_textbox_value(self._textbox_message, loading_message)
        self._show_message()
        self._set_controls_state("disabled")
        
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._extract_url, args=(url, self._cookies_from_browser, self._stop_event), daemon=True)
        self._thread.start()

    def _extract_url(self, url, cookies_from_browser, stop_event):
        try:
            result = extract(url, cookies_from_browser, stop_event)
            if "format" not in result and "formats" not in result and "entries" not in result:
                if "url" in result:
                    result = extract(result.get("url"), cookies_from_browser, stop_event)
                    if "format" not in result and "formats" not in result and "entries" not in result:
                        raise Exception("URL cannot be resolved")
                else:
                    raise Exception("URL cannot be resolved")
            self._handle_result(result, cookies_from_browser)
        except Exception as e:
            if e.__class__.__name__ == "ExtractionStoppedException":
                print(e)
                return
            self._on_result_error(e)

    def _handle_result(self, result, cookies_from_browser = ""):
        self._hide_message()
        self._entry_var.set("")

        result["cookies"] = cookies_from_browser

        if "entries" in result:
            # Result is a playlist, show playlist info frame
            self._playlist_info_frame.grid(row=5, column=0, sticky="nswe", columnspan=20)
            self._playlist_info_frame.data = result
            self._playlist_info_frame.display(result)
        else:
            # Show video info frame
            self._video_info_frame.grid(row=4, column=6, sticky="we", pady=(10, 10), columnspan=10)
            self._video_info_frame.data = result
            self._video_info_frame.display(result)
        
        self._set_controls_state("normal")
        self._cookies_from_browser = ""

    def _on_result_error(self, e):
        self._hide_message()

        error_name = e.__class__.__name__
        message = e.msg if hasattr(e, "msg") else str(e)

        substr = ["Private video", "for registered users", "playlist does not exist", "No video formats found"]
        private = any(str in message for str in substr)
        
        if (error_name == "FileNotFoundError"):
            self._load_cookies_frame.grid(row=3, column=2, pady=(0, 10), sticky="ew", columnspan=16)
            set_textbox_value(self._load_cookies_frame.textbox_message, "Could not find browser cookies. Make sure you provided the appropriate browser name.")
        elif private:
            self._load_cookies_frame.grid(row=3, column=2, pady=(0, 10), sticky="ew", columnspan=16)
            set_textbox_value(self._load_cookies_frame.textbox_message, self._load_cookies_frame.default_message)
        else:
            set_textbox_value(self._textbox_message, "An error occurred when trying to extract URL. Make sure you provided a valid URL and try again.")
            self._show_message()
            self._entry_var.set("")
            print(traceback.format_exc())

        self._set_controls_state("normal")
        self._cookies_from_browser = ""
        print(error_name + ": " + message)

    def on_cookies_submit(self):
        browser = self._load_cookies_frame.get_browser_value().lower()
        if browser == "select your browser":
            return

        self._cookies_from_browser = browser
        self._on_get_info()

    def on_closing(self):
        self._stop_event.set()
        self.destroy()


