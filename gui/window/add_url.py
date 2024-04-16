import asyncio
import customtkinter as ctk
import threading
import tkinter as tk

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

        self._async_loop = asyncio.get_event_loop()
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
        self._async_loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._asyncio_thread, args=(self._async_loop, url, self._cookies_from_browser, self._handle_result))
        self._thread.daemon = True
        self._thread.start()

    def _asyncio_thread(self, async_loop, url, cookies_from_browser, callback):
        try:
            result = async_loop.run_until_complete(self._extract_url(url, cookies_from_browser))
            if not self._stop_event.is_set():
                callback(result, cookies_from_browser)
        except Exception as e:
            self._hide_message()

            error_name = e.__class__.__name__
            message = e.msg if hasattr(e, "msg") else str(e)

            substr = ["Private video", "for registered users", "playlist does not exist"]
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

            print(error_name + ": " + message)
        finally:
            self._set_controls_state("normal")
            self._cookies_from_browser = ""
            async_loop.stop()

    async def _extract_url(self, url, cookies_from_browser = ""):
        result = await extract(url, cookies_from_browser)
        if result["webpage_url_domain"] is None or not "release_year" in result:
            url = result["url"] if "url" in result else result["original_url"]
            result = await extract(url, cookies_from_browser)
        if not "thumbnails" in result or len(result.get("thumbnails")) == 0:
            raise Exception("URL cannot be resolved")
        return result

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

    def on_cookies_submit(self):
        browser = self._load_cookies_frame.get_browser_value().lower()
        if browser == "select your browser":
            return

        self._cookies_from_browser = browser
        self._on_get_info()

    def on_closing(self):
        self._stop_event.set()
        self.destroy()


