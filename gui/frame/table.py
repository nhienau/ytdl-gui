import customtkinter as ctk
from PIL import Image
from tksheet import Sheet

from .table_buttons import TableButtonsFrame
from helper.convert_byte import convert_byte
from helper.custom_exception import DownloadStoppedException
from helper.datetime import to_duration_string
from helper.file_extension import SUPPORTED_EXTENSIONS
from helper.gui import move_rows_up, move_rows_down, move_rows_to_top, move_rows_to_bottom

class TableFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._parent = master

        self._table_buttons_frame = TableButtonsFrame(self)

        self._button_select_all = ctk.CTkButton(self, text="Select all", width=24, command=lambda: self._toggle_all_checkboxes(True), state="disabled")
        self._button_select_all.grid(row=0, column=18, pady=10, sticky="ew")

        self._button_deselect_all = ctk.CTkButton(self, text="Deselect all", width=24, command=lambda: self._toggle_all_checkboxes(False), state="disabled")
        self._button_deselect_all.grid(row=0, column=19, padx=(5, 10), pady=10, sticky="ew")

        self._sheet = Sheet(self, data = [])
        self._sheet.headers([" ", "Title", "URL", "Length", "Cookies", "Status", "Progress", "Downloaded bytes", "Total bytes", "Speed", "ETA", "Elapsed", "Video", "Audio", "Split v+a", "Split by chapters", "Resolution", "Size", "Subtitle", "Thumbnail", "Output folder"])
        self._sheet.row_index([])
        self._sheet.checkbox("A", check_function=self._on_entry_checked)
        self._sheet.column_width(0, width=30)
        for x in range(1, 15):
            self._sheet.column_width(x, width=110)
        self._sheet.column_width(1, width=240)
        self._sheet.column_width(2, width=240)
        self._sheet.column_width(20, width=240)

        self._selecting = False
        self._last_selected_row = None
        self._selected_rows = []
        self.set_table_functionality_and_bindings(True)
        self._sheet.grid(row = 1, column = 0, sticky = "nswe", columnspan=20, padx=10, pady=(0, 10))

        self.display(self.parent.download_list)
    
    def display(self, data, deselect = True, redraw = True):
        list_to_display = [
            [
                entry["selected"],
                entry.get("title") or "",
                entry.get("original_url") or entry.get("url"),
                entry.get("duration_string") or "",
                entry.get("cookies").title(),
                entry["status"].title(),
                "",
                "",
                "",
                "",
                "",
                "",
                "Yes" if entry["preset"]["include_video"] is True else "No",
                "Yes" if entry["preset"]["include_audio"] is True else "No",
                "Yes" if entry["preset"]["split_video_and_audio"] is True else "No",
                "Yes" if entry["preset"]["split_by_chapters"] is True else "No",
                "Best" if entry["preset"]["resolution"] is None else entry["preset"]["resolution"],
                "Best" if entry["preset"]["max_file_size"] is None else f"<={entry['preset']['max_file_size']}MB",
                "Yes" if entry["preset"]["subtitle"] is True else "No",
                "Yes" if entry["preset"]["thumbnail"] is True else "No",
                entry["preset"]["output_path"]]
             for entry in data]
        if deselect is True:
            currently_selected = self._sheet.get_currently_selected()
            if currently_selected:
                row = currently_selected.row
                column = currently_selected.column
                self._sheet.deselect(row, column)
        self._sheet.set_sheet_data(data=list_to_display, reset_col_positions=False, redraw=redraw)
        self._button_select_all.configure(state="disabled" if len(self.parent.download_list) == 0 else "normal")
        self._button_deselect_all.configure(state="disabled" if len(self.parent.download_list) == 0 else "normal")
        if len(self.parent.download_list) == 0:
            self._table_buttons_frame.set_buttons_state("disabled")
            self._table_buttons_frame.grid_forget()
            self.set_buttons_state("disabled")
        else:
            self._table_buttons_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def _on_entry_checked(self, e):
        index = e["selected"][0]
        self.parent.download_list[index]["selected"] = e["value"]
        currently_selected = self._sheet.get_currently_selected()
        row = currently_selected.row
        self._sheet.add_row_selection(row=row, redraw=False, run_binding_func=False)
        self._last_selected_row = row
        self._selected_rows.append(row)
        self._table_buttons_frame.set_buttons_state("normal")

    def _toggle_all_checkboxes(self, value):
        for entry in self.parent.download_list:
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
            self.parent.on_table_rows_clicked(self._selected_rows)
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
        self.parent.on_table_rows_clicked(self._selected_rows)
        self.parent.set_visibility_download_info_frame(False)
            
    def _on_cell_deselected(self, e):
        if e["selection_boxes"] == {}:
            self._selected_rows.clear()
            self._table_buttons_frame.set_buttons_state("disabled")
            self.parent.on_table_rows_clicked(self._selected_rows)
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
        self.parent.on_table_rows_clicked(self._selected_rows)

    def _toggle_marked_rows(self, value):
        for row in self._selected_rows:
            self.parent.download_list[row]["selected"] = value
            self._sheet.click_checkbox(f"A{row + 1}", checked=value)

    def _on_row_selected(self, e):
        for row in self._sheet.get_selected_rows():
            self._selected_rows.append(row)
        currently_selected = self._sheet.get_currently_selected()
        self._table_buttons_frame.set_buttons_state("disabled" if len(currently_selected) == 0 else "normal")
        self.parent.on_table_rows_clicked(self._selected_rows)

    def move_rows_up(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self.parent.download_list) == 1:
            return

        new_list, new_selected_rows = move_rows_up(self.parent.download_list.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
            if i == 0:
                self._sheet.add_row_selection(row=len(self.parent.download_list) - 1, redraw=False, run_binding_func=False)
            else:
                self._sheet.add_row_selection(row=i - 1, redraw=False, run_binding_func=False)

        self.parent.download_list = new_list
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")
        self.parent.on_table_rows_clicked(self._selected_rows)

    def move_rows_down(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self.parent.download_list) == 1:
            return

        new_list, new_selected_rows = move_rows_down(self.parent.download_list.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows, reverse=True):
            self._sheet.deselect(row=i, redraw=False)
            if i == len(self.parent.download_list) - 1:
                self._sheet.add_row_selection(row=0, redraw=False, run_binding_func=False)
            else:
                self._sheet.add_row_selection(row=i + 1, redraw=False, run_binding_func=False)

        self.parent.download_list = new_list
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")
        self.parent.on_table_rows_clicked(self._selected_rows)

    def move_rows_to_top(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self.parent.download_list) == 1:
            return

        new_list, new_selected_rows = move_rows_to_top(self.parent.download_list.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
        for i in sorted(new_selected_rows):
            self._sheet.add_row_selection(row=i, redraw=False, run_binding_func=False)
        self.parent.download_list = new_list
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")
        self.parent.on_table_rows_clicked(self._selected_rows)
        
    def move_rows_to_bottom(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected or len(self.parent.download_list) == 1:
            return

        new_list, new_selected_rows = move_rows_to_bottom(self.parent.download_list.copy(), self._selected_rows.copy())
        for i in sorted(self._selected_rows):
            self._sheet.deselect(row=i, redraw=False)
        for i in sorted(new_selected_rows):
            self._sheet.add_row_selection(row=i, redraw=False, run_binding_func=False)
        self.parent.download_list = new_list
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._selected_rows = new_selected_rows
        self._last_selected_row = self._selected_rows[-1]
        self._sheet.set_currently_selected(row=self._last_selected_row)
        self._table_buttons_frame.set_buttons_state("normal")
        self.parent.on_table_rows_clicked(self._selected_rows)

    def delete_marked_rows(self):
        currently_selected = self._sheet.get_currently_selected()
        if not currently_selected:
            return
        new_list = [el for i, el in enumerate(self.parent.download_list) if i not in self._selected_rows]
        for i in self._selected_rows:
            self._sheet.deselect(row=i, redraw=False)
        self.parent.download_list = new_list
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._last_selected_row = None

        currently_selected = self._sheet.get_currently_selected()
        if currently_selected:
            row = currently_selected.row
            self._sheet.deselect(cell=(row, 0), redraw=True)

        if len(self.parent.download_list) == 0:
            self._table_buttons_frame.set_buttons_state("disabled")
            self._table_buttons_frame.grid_forget()
            self.set_buttons_state("disabled")
        else:
            self._table_buttons_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")
        self.parent.on_table_rows_clicked(self._selected_rows)
        
    def clear_list(self):
        for i in self._selected_rows:
            self._sheet.deselect(row=i, redraw=False)
        self.parent.download_list.clear()
        self.display(data=self.parent.download_list, deselect=False, redraw=True)
        self._last_selected_row = None
        
        self._table_buttons_frame.set_buttons_state("disabled")
        self._table_buttons_frame.grid_forget()
        self.set_buttons_state("disabled")
        self.parent.on_table_rows_clicked(self._selected_rows)

    def set_buttons_state(self, state):
        self._button_select_all.configure(state=state)
        self._button_deselect_all.configure(state=state)

    def set_table_functionality_and_bindings(self, value):
        default_bindings = ["single_select", "row_select", "drag_select", "ctrl_select", "column_width_resize", "double_click_column_resize", "right_click_popup_menu", "arrowkeys"]
        if value is True:
            self._sheet.enable_bindings(*default_bindings)
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
        else:
            self._sheet.disable_bindings(*default_bindings)
            self._sheet.popup_menu_del_command()

    def set_download_status(self, entry, index, status, clear_progress_info = True):
        entry["status"] = status
        self._sheet.span(f"F{index + 1}").data = entry["status"].title()
        if clear_progress_info:
            self._sheet.span(f"G{index + 1}").data = ["" for i in range(0, 6)]

    def display_progress(self, progress, stop_event, entry, index):
        if stop_event.is_set():
            raise DownloadStoppedException("Download stopped by user")

        file_extension = progress["filename"].split(".")[-1]
        if file_extension not in SUPPORTED_EXTENSIONS:
            return
        extension_info = self._parent.download_extension_info
        if extension_info["extension"] is None:
            extension_info["extension"] = file_extension
        elif not extension_info["initial"] or extension_info["extension"] != file_extension:
            extension_info["initial"] = False
            extension_info["extension"] = file_extension
            return

        if progress["downloaded_bytes"] is None:
            downloaded_bytes_str = ""
        else:
            downloaded_bytes = convert_byte(progress["downloaded_bytes"])
            downloaded_bytes_str = f"{(downloaded_bytes['result']):.1f} {downloaded_bytes['unit']}"

        if "total_bytes" not in progress and "total_bytes_estimate" not in progress:
            total_bytes_str = ""
        else:
            total_bytes = convert_byte(progress.get("total_bytes") or progress.get("total_bytes_estimate"))
            total_bytes_str = f"{(total_bytes['result']):.1f} {total_bytes['unit']}"
        
        if progress["speed"] is None:
            speed_str = ""
        else:
            speed = convert_byte(progress["speed"])
            speed_str = f"{(speed['result']):.1f} {speed['unit']}/s"

        status = progress["status"]
        entry["status"] = progress["status"]
        progress_str = f"{(progress['downloaded_bytes'] / (progress.get('total_bytes') or progress.get('total_bytes_estimate')) * 100):.1f}%"

        eta_str = to_duration_string(progress['eta']) if "eta" in progress else ""
        elapsed_str = to_duration_string(progress["elapsed"]) if "elapsed" in progress else ""
        
        if progress["status"] == "error":
            self.set_download_status(entry, index, progress["status"], False)
            return

        if progress["status"] == "finished":
            status = "postprocessing"
            entry["status"] = status

        self._sheet.span(f"F{index + 1}").data = [status.title(), progress_str, downloaded_bytes_str, total_bytes_str, speed_str, eta_str, elapsed_str]

    def on_url_postprocessing(self, process_info, stop_event, entry, index):
        if stop_event.is_set():
            raise DownloadStoppedException("Download stopped by user")

        status = "finished" if process_info["status"] == "finished" else "postprocessing"
        self.set_download_status(entry, index, status, False)
        if process_info["status"] == "finished":
            self._parent.on_entry_finish_downloading()

    def on_download_stopped(self, entry, index):
        self.set_download_status(entry, index, "stopped", False)
        self._parent.download_extension_info = {}

        pending_entries = [(index, entry) for index, entry in enumerate(self._parent.download_list) if entry["status"] == "pending"]
        for pending_index, pending_entry in pending_entries:
            self.set_download_status(pending_entry, pending_index, "ready")


