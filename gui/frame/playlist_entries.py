import customtkinter as ctk
from PIL import Image
from tksheet import Sheet

from helper.datetime import to_duration_string

class PlaylistEntriesFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._data = []
        self._query = ""

        self._search_entry_var = ctk.StringVar(value="")
        self._entry_search = ctk.CTkEntry(self, textvariable=self._search_entry_var)
        self._entry_search.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew", columnspan=5)
        self._entry_search.bind("<Return>", lambda e: self._handle_search())

        self._icon_clear = ctk.CTkImage(light_image=Image.open("gui/icons/close.png"), dark_image=Image.open("gui/icons/close.png"), size=(24, 24))

        self._button_clear_input = ctk.CTkButton(self, image=self._icon_clear, text="", width=24, fg_color="#FFFFFF", hover_color="#EBEBEB", anchor="center", command=self._clear_query)

        self._icon_search = ctk.CTkImage(light_image=Image.open("gui/icons/search.png"), dark_image=Image.open("gui/icons/search.png"), size=(24, 24))

        self._button_search = ctk.CTkButton(self, image=self._icon_search, text="", width=24, fg_color="#FFFFFF", hover_color="#EBEBEB", anchor="center", command=self._handle_search)
        self._button_search.grid(row=0, column=6, pady=10, sticky="we")

        self._button_select_all = ctk.CTkButton(self, text="Select all", width=24)
        self._button_select_all.grid(row=0, column=18, pady=10, sticky="ew")

        self._button_unselect_all = ctk.CTkButton(self, text="Unselect all", width=24)
        self._button_unselect_all.grid(row=0, column=19, padx=(5, 10), pady=10, sticky="ew")

        self._sheet = Sheet(self, data = data)
        self._sheet.headers([" ", "Title", "Uploader", "Duration", "URL"])
        self._sheet.row_index([])
        self._sheet.checkbox("A")
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(1, width=180)
        for x in range(2, 5):
            self._sheet.column_width(x, width=110)

        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "rc_select", "arrowkeys")
        self._sheet.grid(row = 1, column = 0, sticky = "nswe", columnspan=20, padx=10, pady=(0, 10))

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def display(self, data):
        list_to_display = list(map(lambda entry: [entry["selected"], entry["title"], entry["uploader"], to_duration_string(entry["duration"]), entry["url"]], data))
        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            column = currently_selected.column
            self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False)

    def _handle_search(self):
        query = self._search_entry_var.get().strip()
        if query == self._query:
            return
        
        self._query = query
        if query == "":
            self.display(self._data)
            self._button_clear_input.grid_forget()
            return
        
        filtered = list(filter(lambda entry: query in entry["title"].lower(), self._data))
        self.display(filtered)
        self._button_clear_input.grid(row=0, column=5, padx=(0, 5), pady=10, sticky="we")

    def _clear_query(self):
        self._query = ""
        self._search_entry_var.set("")
        self._button_clear_input.grid_forget()
        self.display(self._data)


