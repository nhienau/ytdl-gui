import customtkinter as ctk

from .playlist_detail import PlaylistDetailFrame
from .playlist_entries import PlaylistEntriesFrame

from helper.datetime import to_duration_string

class PlaylistInfoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._parent = master
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._data = {}

        self._detail_frame = PlaylistDetailFrame(self)
        self._detail_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nswe", columnspan=4)

        self._entries_table = PlaylistEntriesFrame(self, data=[])
        self._entries_table.grid(row=0, column=4, padx=(5, 10), pady=10, sticky="nswe", columnspan=16)

    def set_data(self, data):
        # Check if entries are from a channel
        if len(data["entries"]) > 0 and "entries" in data["entries"][0]:
            # Combine all videos, lives, etc. from a channel
            uploader = data["uploader"]
            data["entries"] = [entry for category in data["entries"] for entry in category["entries"]]
            for entry in data["entries"]:
                entry["uploader"] = data["uploader"]
            data["playlist_count"] = len(data["entries"])
                
        if data["uploader"] is None:
            uploaders = list(set(map(lambda entry: entry["uploader"], data["entries"])))
            if len(uploaders) == 1:
                data["uploader"] = uploaders[0]

        for entry in data["entries"]:
            entry["selected"] = True

        data["entries"] = list(filter(lambda entry: entry["uploader"] is not None, data["entries"]))
        data["available_count"] = len(data["entries"])

        self._data = data
        self._detail_frame.set_data(data)
        self._entries_table.set_data(data["entries"])

    def display(self, data):
        self._detail_frame.display(data)
        self._entries_table.display(self._entries_table.get_data())

    def on_add_entries_click(self, add_all=True):
        self._detail_frame.hide_confirm_message()
        self._detail_frame.add_option = "all" if add_all is True else "selected"
        self._detail_frame.hide_additional_message()
        data = self._entries_table.get_data()
        if not add_all:
            data = list(filter(lambda entry: entry["selected"] is True, data))
            if len(data) == 0:
                self._detail_frame.show_confirm_message("No videos selected", show_button=False)
                return
        
        self._detail_frame.show_confirm_message(f"{len(data)} video{'' if len(data) == 1 else 's'} will be added.")

    def add_entries(self):
        data = self._entries_table.get_data()
        if self._detail_frame.add_option == "selected":
            data = filter(lambda entry: entry["selected"] is True, data)
        data = list(map(lambda entry: {
            "title": entry["title"],
            "uploader": entry["uploader"],
            "duration": entry["duration"],
            "duration_string": to_duration_string(entry["duration"]),
            "url": entry["url"],
            "cookies": self._data["cookies"],
            "selected": True,
        }, data))
        on_add_urls = self._parent.callbacks["on_add_urls"]
        result = on_add_urls(data)
        message = f"Successfully added {result['added']} video{'' if result['added'] == 1 else 's'}."
        self._detail_frame.show_additional_message(message)
        self._detail_frame.hide_confirm_message()


