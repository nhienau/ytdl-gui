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
        self._query_results = []

        self._search_entry_var = ctk.StringVar(value="")
        self._entry_search = ctk.CTkEntry(self, textvariable=self._search_entry_var)
        self._entry_search.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ew", columnspan=5)
        self._entry_search.bind("<Return>", lambda e: self._handle_search())

        self._icon_clear = ctk.CTkImage(light_image=Image.open("gui/icons/close.png"), dark_image=Image.open("gui/icons/close.png"), size=(24, 24))

        self._button_clear_input = ctk.CTkButton(self, image=self._icon_clear, text="", width=24, fg_color="#FFFFFF", hover_color="#EBEBEB", anchor="center", command=self._clear_query)

        self._icon_search = ctk.CTkImage(light_image=Image.open("gui/icons/search.png"), dark_image=Image.open("gui/icons/search.png"), size=(24, 24))

        self._button_search = ctk.CTkButton(self, image=self._icon_search, text="", width=24, fg_color="#FFFFFF", hover_color="#EBEBEB", anchor="center", command=self._handle_search)
        self._button_search.grid(row=0, column=6, pady=10, sticky="we")

        self._button_select_all = ctk.CTkButton(self, text="Select all", width=24, command=lambda: self._toggle_all_checkboxes(True))
        self._button_select_all.grid(row=0, column=18, pady=10, sticky="ew")

        self._button_unselect_all = ctk.CTkButton(self, text="Unselect all", width=24, command=lambda: self._toggle_all_checkboxes(False))
        self._button_unselect_all.grid(row=0, column=19, padx=(5, 10), pady=10, sticky="ew")

        self._sheet = Sheet(self, data = data)
        self._sheet.headers([" ", "Title", "Uploader", "Duration", "URL"])
        self._sheet.row_index([])
        self._sheet.checkbox("A", check_function=self._on_entry_checked)
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(1, width=180)
        for x in range(2, 5):
            self._sheet.column_width(x, width=110)

        self._selecting = False
        self._last_selected_row = None
        self._selected_rows = []
        self._sheet.enable_bindings("single_select", "row_select", "drag_select", "ctrl_select", "column_width_resize", "double_click_column_resize", "right_click_popup_menu", "arrowkeys", "up", "down")
        self._sheet.extra_bindings(["cell_select", "drag_select_cells"], func=lambda e: self._on_cell_selected(e))
        self._sheet.extra_bindings("deselect", func=lambda e: self._on_cell_deselected(e))
        self._sheet.extra_bindings("shift_cell_select", func=lambda e: self._on_shift_cell_selected(e))
        self._sheet.grid(row = 1, column = 0, sticky = "nswe", columnspan=20, padx=10, pady=(0, 10))

    def set_data(self, data):
        self._data = data
        self._query_results = self._data

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
        
        self._query_results = list(filter(lambda entry: query in entry["title"].lower(), self._data))
        self.display(self._query_results)
        self._button_clear_input.grid(row=0, column=5, padx=(0, 5), pady=10, sticky="we")

    def _clear_query(self):
        self._query = ""
        self._search_entry_var.set("")
        self._button_clear_input.grid_forget()
        self._query_results = self._data
        self.display(self._data)

    def _on_entry_checked(self, e):
        print("[Checkbox] Selection boxes:", e["selection_boxes"])
        print("[Checkbox] Selected:", e["selected"])
        print("[Checkbox] Being selected: ", e["being_selected"])
        print("[Checkbox] Selected rows: ", self._selected_rows)

        index = e["selected"][0]
        self._query_results[index]["selected"] = e["value"]
        for row in self._selected_rows:
            if row != index:
                self._sheet.click_checkbox(checked=e["value"], redraw=False)
                self._query_results[row]["selected"] = e["value"]

    def _toggle_all_checkboxes(self, value):
        for entry in self._query_results:
            entry["selected"] = value
        self._sheet.click_checkbox("A", checked=value)

    def _on_cell_selected(self, e):
        print("[Cell, before] Selection boxes:", e["selection_boxes"])
        print("[Cell, before] Selected:", e["selected"])
        print("[Cell, before] Being selected: ", e["being_selected"])
        print("[Cell, before] Selected rows: ", self._selected_rows)
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        column = currently_selected.column
        
        # Deselect row if selected
        if self._sheet.row_selected(row):
            self._selecting = True
            self._sheet.deselect(row=row, redraw=False)
            self._sheet.deselect(cell=(row, column), redraw=True)
            self._selecting = False
            self._selected_rows.remove(row)
            # Store last selected row (for shift select)
            currently_selected = self._sheet.get_currently_selected()
            self._last_selected_row = None if len(currently_selected) == 0 else currently_selected.row
            return
        
        # Skip if selected on checkbox cell
        if column == 0:
            return
        
        # Select row
        self._selecting = True
        self._sheet.deselect(cell=(row, column), redraw=False)
        self._selecting = False
        self._sheet.add_row_selection(row=row, redraw=False, run_binding_func=False)
        self._last_selected_row = row
        self._selected_rows.append(row)
        print("[Cell, after] Selection boxes:", e["selection_boxes"])
        print("[Cell, after] Selected:", e["selected"])
        print("[Cell, after] Being selected: ", e["being_selected"])
        print("[Cell, after] Selected rows: ", self._selected_rows)
            
    def _on_cell_deselected(self, e):
        print(e)
        print("[Deselected] Selection boxes:", e["selection_boxes"])
        print("[Deselected] Selected:", e["selected"])
        print("[Deselected] Being selected: ", e["being_selected"])
        print("[Deselected] Selected rows: ", self._selected_rows)
        if e["selection_boxes"] == {}:
            print("[Deselected] Selected_boxes empty")
            self._selected_rows.clear()
            return
        elif self._selecting is True:
            print("[Deselected] Selecting..")
            return

    def _on_shift_cell_selected(self, e):
        print("[Shift, before] Selection boxes:", e["selection_boxes"])
        print("[Shift, before] Selected:", e["selected"])
        print("[Shift, before] Being selected: ", e["being_selected"])
        print("[Shift, before] Selected rows: ", self._selected_rows)
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        column = currently_selected.column
        r1 = min(row, self._last_selected_row)
        r2 = max(row, self._last_selected_row)

        self._selecting = True
        self._sheet.deselect(cell=(row, column), redraw=False)
        self._selecting = False
        for r in range(r1, r2 + 1):
            self._sheet.add_row_selection(row=r, redraw=False, run_binding_func=False)

        self._selected_rows = [row for row in range(r1, r2 + 1)]
        print("[Shift, after] Selected rows: ", self._selected_rows)
        
    def clear_entries(self):
        self._data = []
        self._query = ""
        self._query_results = self._data
        self._search_entry_var.set("")
        self._button_clear_input.grid_forget()
        self.display(self._data)


