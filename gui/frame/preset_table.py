import customtkinter as ctk
from tksheet import Sheet

class PresetTableFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._root_data = master.root_data

        self._sheet = Sheet(self, data=[])
        self._sheet.headers(["ID", "Preset"])
        self._sheet.row_index([])
        self._sheet.display_columns([1], all_displayed = False)
        self._sheet.column_width(0, width=300)
        self._sheet.enable_bindings("single_select", "row_select", "column_width_resize", "double_click_column_resize", "up", "down")
        self._sheet.extra_bindings(["cell_select", "row_select", "up", "down"], func=lambda e: master.on_table_cell_selected(e))
        self._sheet.grid(row = 0, column = 0, sticky = "nswe", columnspan=20)

        self.display(self.root_data.preset)

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    def display(self, data):
        list_to_display = [[entry["id"], entry["name"]] for entry in data]
        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            column = currently_selected.column
            self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False)


