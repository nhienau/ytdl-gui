import customtkinter as ctk
from tksheet import Sheet

class TableFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sheet = Sheet(self, data = data)
        self._sheet.headers([" ", "ID", "Title", "Video", "Audio", "Progress", "Status", "Length", "Size", "Subtitle", "Thumbnail", "Sponsorblock"])
        self._sheet.row_index([])
        self._sheet.checkbox("A")
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(2, width=180)
        for x in range(3, 12):
            self._sheet.column_width(x, width=110)

        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "rc_select", "arrowkeys")
        # self._sheet.enable_bindings("all")
        self._sheet.grid(row = 0, column = 0, sticky = "nswe")


