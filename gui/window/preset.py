import customtkinter as ctk
from tksheet import Sheet

from gui.frame.preset_detail import PresetDetailFrame
from gui.frame.preset_table import PresetTableFrame
from helper.get_download_folder import get_download_folder
import preset.preset as preset

class PresetWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ytdl-gui")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._root_data = list(args)[0]._parent
        self._selected_preset = self._root_data.current_preset

        self._button_new_preset = ctk.CTkButton(self, text="New", width=24, command=self._on_new_preset_clicked)
        self._button_new_preset.grid(row = 0, column = 5, padx=(10, 5), pady = (10, 0))

        self._button_save_preset = ctk.CTkButton(self, text="Save", width=24, state="disabled")
        self._button_save_preset.grid(row = 0, column = 6, padx=5, pady = (10, 0))

        self._button_delete_preset = ctk.CTkButton(self, text="Delete", width=24, command=self._on_delete_preset_clicked)
        self._button_delete_preset.grid(row = 0, column = 7, padx = (5, 0), pady = (10, 0))

        self._preset_table_frame = PresetTableFrame(self)
        self._preset_table_frame.grid(row = 1, column = 0, sticky = "nswe", columnspan = 5, padx = 10, pady = 10)

        self._preset_detail_frame = PresetDetailFrame(self)
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)

        self._button_confirm_choose_preset = ctk.CTkButton(self, text="OK")
        self._button_confirm_choose_preset.grid(row = 2, column=19, sticky="e", padx = (0, 10), pady = (0, 10))

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    def on_table_cell_selected(self, e):
        self._button_new_preset.configure(state="normal")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="normal")
        currently_selected = self._preset_table_frame._sheet.get_currently_selected()
        row = currently_selected.row
        self._selected_preset = self.root_data.preset[row]
        self._preset_detail_frame.preset = self.root_data.preset[row]
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)
        self._preset_detail_frame.set_appearance_button_cancel_and_ok(False)

    def _on_new_preset_clicked(self):
        self._selected_preset = None
        self._button_new_preset.configure(state="disabled")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="disabled")
        self._preset_table_frame.deselect()
        self._preset_detail_frame.set_elements_state("normal")
        self._preset_detail_frame._var_preset_name.set("")
        self._preset_detail_frame._output_path.set(get_download_folder())
        self._preset_detail_frame.set_appearance_button_cancel_and_ok(True)
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)
        
    def on_new_preset_cancel_clicked(self):
        self._button_new_preset.configure(state="normal")
        self._preset_detail_frame.clear_all_input()
        self._preset_detail_frame.set_appearance_button_cancel_and_ok(False)
        self._preset_detail_frame.grid_forget()

    def create_new_preset(self, new_preset):
        preset.insert(new_preset)
        self.root_data.preset = preset.get_all()
        self._selected_preset = self.root_data.preset[len(self.root_data.preset) - 1]
        self._button_new_preset.configure(state="normal")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="normal")
        self._preset_table_frame.display(self.root_data.preset)
        self._preset_table_frame._sheet.add_row_selection(row=len(self.root_data.preset) - 1, redraw=True, run_binding_func=False)
        self._preset_detail_frame.preset = self._selected_preset

    def _on_delete_preset_clicked(self):
        self._preset_detail_frame.show_confirm_delete_message(self._selected_preset)

    def on_preset_confirm_delete_clicked(self, preset_info):
        preset_id = preset_info["id"]
        preset.delete(preset_id)
        self.root_data.preset = preset.get_all()
        self.root_data.current_preset = self.root_data.preset[0]
        self._selected_preset = self.root_data.current_preset
        self._button_new_preset.configure(state="normal")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="disabled")
        self._preset_table_frame.display(self.root_data.preset)
        self._preset_table_frame._sheet.add_row_selection(row=0, redraw=True, run_binding_func=False)
        self._preset_detail_frame.preset = self._selected_preset


