import customtkinter as ctk
from tksheet import Sheet

class TableFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._data = data
        self._sheet = Sheet(self, data = [])
        self._sheet.headers([" ", "Title", "URL", "Video", "Audio", "Progress", "Status", "Length", "Size", "Subtitle", "Thumbnail", "Sponsorblock"])
        self._sheet.row_index([])
        self._sheet.checkbox("A")
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(2, width=180)
        for x in range(3, 12):
            self._sheet.column_width(x, width=110)

        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "rc_select", "arrowkeys")
        # self._sheet.enable_bindings("all")
        self._sheet.grid(row = 0, column = 0, sticky = "nswe")
    
    def display(self, data):
        self._data = data
        list_to_display = list(map(lambda entry: [entry["selected"], entry["title"], entry.get("webpage_url") or entry.get("url"), "", "", "", "", "", "", "", "", ""], data))
        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            column = currently_selected.column
            self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False)


