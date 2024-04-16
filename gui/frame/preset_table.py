import customtkinter as ctk
from tksheet import Sheet

class PresetTableFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._parent = master
        self._data = data

        self._sheet = Sheet(self, data=self._data)
        self._sheet.headers(["ID", "Preset"])
        self._sheet.row_index([])
        self._sheet.display_columns([1], all_displayed = False)
        self._sheet.column_width(0, width=300)
        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "up", "down")
        self._sheet.extra_bindings(["cell_select", "row_select", "up", "down"], func=lambda e: self._on_cell_selected(e))
        self._sheet.grid(row = 0, column = 0, sticky = "nswe", columnspan=20)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.display(self._data)

    def display(self, data):
        list_to_display = [[entry["id"], entry["name"]] for entry in data]
        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            column = currently_selected.column
            self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False)

    def _on_cell_selected(self, e):
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        self._parent.current_preset = self._data[row]

        
