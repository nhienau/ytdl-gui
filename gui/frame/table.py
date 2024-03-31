import customtkinter as ctk
from PIL import Image
from tksheet import Sheet

from .table_buttons import TableButtonsFrame
from helper.datetime import to_duration_string
from helper.gui import move_rows_up, move_rows_down, move_rows_to_top, move_rows_to_bottom

class TableFrame(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._data = data

        self._table_buttons_frame = TableButtonsFrame(self)

        self._button_select_all = ctk.CTkButton(self, text="Select all", width=24, command=lambda: self._toggle_all_checkboxes(True), state="disabled")
        self._button_select_all.grid(row=0, column=18, pady=10, sticky="ew")

        self._button_deselect_all = ctk.CTkButton(self, text="Deselect all", width=24, command=lambda: self._toggle_all_checkboxes(False), state="disabled")
        self._button_deselect_all.grid(row=0, column=19, padx=(5, 10), pady=10, sticky="ew")

        self._sheet = Sheet(self, data = [])
        self._sheet.headers([" ", "Title", "URL", "Video", "Audio", "Progress", "Status", "Length", "Size", "Subtitle", "Thumbnail", "Sponsorblock"])
        self._sheet.row_index([])
        self._sheet.checkbox("A", check_function=self._on_entry_checked)
        self._sheet.column_width(0, width=30)
        self._sheet.column_width(2, width=180)
        for x in range(3, 12):
            self._sheet.column_width(x, width=110)

        self._selecting = False
        self._last_selected_row = None
        self._selected_rows = []
        self._sheet.enable_bindings("single_select", "row_select", "drag_select", "ctrl_select", "column_width_resize", "double_click_column_resize", "right_click_popup_menu", "arrowkeys")
        self._sheet.extra_bindings(["cell_select", "drag_select_cells"], func=lambda e: self._on_cell_selected(e))
        self._sheet.extra_bindings("deselect", func=lambda e: self._on_cell_deselected(e))
        self._sheet.extra_bindings("shift_cell_select", func=lambda e: self._on_shift_cell_selected(e))
        self._sheet.extra_bindings(["row_select", "drag_select_rows"], func=lambda e: self._on_row_selected(e))
        self._sheet.popup_menu_add_command("Select marked URLs", lambda: self._toggle_marked_rows(True), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Deselect marked URLs", lambda: self._toggle_marked_rows(False), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Select all URLs", lambda: self._toggle_all_checkboxes(True), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Deselect all URLs", lambda: self._toggle_all_checkboxes(False), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Move up", lambda: self.move_rows_up(), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Move down", lambda: self.move_rows_down(), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Move to top", lambda: self.move_rows_to_top(), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Move to bottom", lambda: self.move_rows_to_bottom(), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Delete marked URLs", lambda: self.delete_marked_rows(), empty_space_menu=False)
        self._sheet.popup_menu_add_command("Delete all URLs", lambda: self.clear_list(), empty_space_menu=False)
        self._sheet.grid(row = 1, column = 0, sticky = "nswe", columnspan=20, padx=10, pady=(0, 10))
    
    def display(self, data, deselect = True, redraw = True):
        list_to_display = [[entry["selected"], entry["title"], entry.get("webpage_url") or entry.get("url"), "", "", "", "", "", "", "", "", ""] for entry in data]
        if deselect is True:
            currently_selected = self._sheet.get_currently_selected()
            if currently_selected:
                row = currently_selected.row
                column = currently_selected.column
                self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False, redraw=redraw)
        self._button_select_all.configure(state="disabled" if len(self._data) == 0 else "normal")
        self._button_deselect_all.configure(state="disabled" if len(self._data) == 0 else "normal")
        if len(self._data) == 0:
            self._table_buttons_frame.set_buttons_state("disabled")
            self._table_buttons_frame.grid_forget()
            self._set_buttons_state("disabled")
        else:
            self._table_buttons_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def _on_entry_checked(self, e):
        index = e["selected"][0]
        self._data[index]["selected"] = e["value"]
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        self._sheet.add_row_selection(row=row, redraw=False, run_binding_func=False)
        self._last_selected_row = row
        self._selected_rows.append(row)
        self._table_buttons_frame.set_buttons_state("normal")

    def _toggle_all_checkboxes(self, value):
        for entry in self._data:
            entry["selected"] = value
        self._sheet.click_checkbox("A", checked=value)

    def _on_cell_selected(self, e):
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        column = currently_selected.column
        
        # Deselect row if selected
        if self._sheet.row_selected(row):
            self._sheet.deselect(row=row, redraw=False)
            self._sheet.deselect(cell=(row, column), redraw=True)
            if row in self._selected_rows:
                self._selected_rows.remove(row)
            # Store last selected row (for shift select)
            currently_selected = self._sheet.get_currently_selected()
            self._last_selected_row = None if len(currently_selected) == 0 else currently_selected.row
            self._table_buttons_frame.set_buttons_state("disabled" if len(currently_selected) == 0 else "normal")
            return
        
        # Skip if selected on checkbox cell
        if column == 0:
            return
        
        # Select row
        self._sheet.deselect(cell=(row, column), redraw=False)
        self._sheet.add_row_selection(row=row, redraw=False, run_binding_func=False)
        self._last_selected_row = row
        self._selected_rows.append(row)
        self._table_buttons_frame.set_buttons_state("disabled" if len(currently_selected) == 0 else "normal")
            
    def _on_cell_deselected(self, e):
        if e["selection_boxes"] == {}:
            self._selected_rows.clear()
            self._table_buttons_frame.set_buttons_state("disabled")
            return

    def _on_shift_cell_selected(self, e):
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        column = currently_selected.column
        r1 = min(row, self._last_selected_row)
        r2 = max(row, self._last_selected_row)
        self._sheet.deselect(cell=(row, column), redraw=False)
        for r in range(r1, r2 + 1):
            self._sheet.add_row_selection(row=r, redraw=False, run_binding_func=False)
        
        self._selected_rows = [row for row in range(r1, r2 + 1)]
        self._table_buttons_frame.set_buttons_state("disabled" if len(currently_selected) == 0 else "normal")

    def _toggle_marked_rows(self, value):
        for row in self._selected_rows:
            self._data[row]["selected"] = value
            self._sheet.click_checkbox(f"A{row + 1}", checked=value)

    def _on_row_selected(self, e):
        for row in self._sheet.get_selected_rows():
            self._selected_rows.append(row)
        currently_selected = self._sheet.get_currently_selected()
        self._table_buttons_frame.set_buttons_state("disabled" if len(currently_selected) == 0 else "normal")

    def move_rows_up(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self._data) == 1:
            return

        new_list, new_selected_rows = move_rows_up(self._data.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
            if i == 0:
                self._sheet.add_row_selection(row=len(self._data) - 1, redraw=False, run_binding_func=False)
            else:
                self._sheet.add_row_selection(row=i - 1, redraw=False, run_binding_func=False)

        self._data = new_list
        self.display(data=self._data, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")

    def move_rows_down(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self._data) == 1:
            return

        new_list, new_selected_rows = move_rows_down(self._data.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows, reverse=True):
            self._sheet.deselect(row=i, redraw=False)
            if i == len(self._data) - 1:
                self._sheet.add_row_selection(row=0, redraw=False, run_binding_func=False)
            else:
                self._sheet.add_row_selection(row=i + 1, redraw=False, run_binding_func=False)

        self._data = new_list
        self.display(data=self._data, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")

    def move_rows_to_top(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self._data) == 1:
            return

        new_list, new_selected_rows = move_rows_to_top(self._data.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
        for i in sorted(new_selected_rows):
            self._sheet.add_row_selection(row=i, redraw=False, run_binding_func=False)
        self._data = new_list
        self.display(data=self._data, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")
        
    def move_rows_to_bottom(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self._data) == 1:
            return

        new_list, new_selected_rows = move_rows_to_bottom(self._data.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
        for i in sorted(new_selected_rows):
            self._sheet.add_row_selection(row=i, redraw=False, run_binding_func=False)
        self._data = new_list
        self.display(data=self._data, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")

    def delete_marked_rows(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected:
            return
        new_list = [el for i, el in enumerate(self._data) if i not in self._selected_rows]
        for i in self._selected_rows:
            self._sheet.deselect(row=i, redraw=False)
        self._data = new_list
        self.display(data=self._data, deselect=False, redraw=True)
        self._last_selected_row = None

        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            self._sheet.deselect(cell=(row, 0), redraw=True)

        if len(self._data) == 0:
            self._table_buttons_frame.set_buttons_state("disabled")
            self._table_buttons_frame.grid_forget()
            self._set_buttons_state("disabled")
        else:
            self._table_buttons_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")
        
    def clear_list(self):
        for i in self._selected_rows:
            self._sheet.deselect(row=i, redraw=False)
        self._data.clear()
        self._data = self._data
        self.display(data=self._data, deselect=False, redraw=True)
        self._last_selected_row = None
        
        self._table_buttons_frame.set_buttons_state("disabled")
        self._table_buttons_frame.grid_forget()
        self._set_buttons_state("disabled")

    def _set_buttons_state(self, state):
        self._button_select_all.configure(state=state)
        self._button_deselect_all.configure(state=state)


