import customtkinter as ctk
from tksheet import Sheet

from helper.datetime import to_duration_string

class PlaylistEntriesFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._data = []

        self._sheet = Sheet(self, data = data)
        self._sheet.headers([" ", "Title", "Uploader", "Duration", "URL"])
        self._sheet.row_index([])
        self._sheet.checkbox("A")
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(1, width=180)
        for x in range(2, 5):
            self._sheet.column_width(x, width=110)

        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "rc_select", "arrowkeys")
        self._sheet.grid(row = 0, column = 0, sticky = "nswe")

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def display(self, data):
        list_to_display = list(map(lambda entry: [True, entry["title"], entry["uploader"], to_duration_string(entry["duration"]), entry["url"]], data))
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False, reset_highlights=True)


