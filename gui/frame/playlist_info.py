import customtkinter as ctk

from .playlist_detail import PlaylistDetailFrame
from .playlist_entries import PlaylistEntriesFrame

from helper.datetime import to_duration_string

class PlaylistInfoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._root_data = master._root_data
        self._data = {}

        self._detail_frame = PlaylistDetailFrame(self)
        self._detail_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nswe", columnspan=4)

        self._entries_table = PlaylistEntriesFrame(self, data=[])
        self._entries_table.grid(row=0, column=4, padx=(5, 10), pady=10, sticky="nswe", columnspan=16)

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        # Check if entries are from a channel
        if len(data["entries"]) > 0 and "entries" in data["entries"][0]:
            # Combine all videos, lives, etc. from a channel
            uploader = data["uploader"]
            data["entries"] = [entry for category in data["entries"] for entry in category["entries"]]
            for entry in data["entries"]:
                entry["uploader"] = data["uploader"]
            data["playlist_count"] = len(data["entries"])
                
        if data.get("uploader") is None:
            uploaders = list(set(map(lambda entry: entry.get("uploader"), data["entries"])))
            if len(uploaders) == 1:
                data["uploader"] = uploaders[0]

        for entry in data["entries"]:
            entry["selected"] = True

        if "youtube" in data.get("extractor").lower():
            data["entries"] = list(filter(lambda entry: (entry.get("view_count") or entry.get("concurrent_view_count")) is not None, data["entries"]))
            data["available_count"] = len(data["entries"])
        
        if not data.get("playlist_count"):
            data["playlist_count"] = len(data.get("entries"))

        self._data = data
        self._detail_frame.data = data
        self._entries_table.data = data["entries"]

    def display(self, data):
        self._detail_frame.display(data)
        self._entries_table.display(self._entries_table.data)

    def on_add_entries_click(self, add_all=True):
        self._detail_frame.hide_confirm_message()
        self._detail_frame.add_option = "all" if add_all is True else "selected"
        self._detail_frame.hide_additional_message()
        data = self._entries_table.data
        if not add_all:
            data = list(filter(lambda entry: entry["selected"] is True, data))
            if len(data) == 0:
                self._detail_frame.show_confirm_message("No videos selected", show_button=False)
                return
        
        self._detail_frame.show_confirm_message(f"{len(data)} video{'' if len(data) == 1 else 's'} will be added.")

    def add_entries(self):
        data = self._data["entries"]
        if self._detail_frame.add_option == "selected":
            data = filter(lambda entry: entry["selected"] is True, data)
        data = list(map(lambda entry: {
            "title": entry.get("title") or "",
            "uploader": entry.get("uploader") or "",
            "duration": entry.get("duration") or "",
            "duration_string": to_duration_string(entry.get("duration")),
            "url": entry.get("url"),
            "cookies": self._data["cookies"],
            "selected": True,
            "status": "ready"
        }, data))
        result = self.root_data.on_add_urls(data)
        message = f"Successfully added {result['added']} video{'' if result['added'] == 1 else 's'}."
        self._detail_frame.show_additional_message(message)
        self._detail_frame.hide_confirm_message()

    def clear_frame(self):
        self._detail_frame.clear_detail()
        self._entries_table.clear_entries()


