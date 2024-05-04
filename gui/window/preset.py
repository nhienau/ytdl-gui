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
        self._parent = list(args)[0]
        self._root_data = list(args)[0]._parent
        self._selected_preset = self._root_data.current_preset
        self._new_preset_creating = False
        self._choose = False # check if this window is opened for changing curent preset or not

        self._button_new_preset = ctk.CTkButton(self, text="New", width=24, command=self._on_new_preset_clicked)
        self._button_new_preset.grid(row = 0, column = 5, padx=(10, 5), pady = (10, 0))

        self._button_save_preset = ctk.CTkButton(self, text="Save", width=24, state="disabled", command=self._on_save_preset_clicked)
        self._button_save_preset.grid(row = 0, column = 6, padx=5, pady = (10, 0))

        self._button_delete_preset = ctk.CTkButton(self, text="Delete", width=24, state="normal" if self._selected_preset["editable"] is True else "disabled", command=self._on_delete_preset_clicked)
        self._button_delete_preset.grid(row = 0, column = 7, padx = (5, 0), pady = (10, 0))

        self._preset_table_frame = PresetTableFrame(self)
        self._preset_table_frame.grid(row = 1, column = 0, sticky = "nswe", columnspan = 5, padx = 10, pady = 10)

        self._preset_detail_frame = PresetDetailFrame(self)
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)

        self._button_confirm_choose_preset = ctk.CTkButton(self, text="OK", command=self._on_preset_chosen)

        self._button_close = ctk.CTkButton(self, text="Close", command=lambda: self.destroy())

        if self._choose is True:
            self._button_confirm_choose_preset.grid(row = 2, column=18, sticky="e", padx = (0, 10), pady = (0, 10))
            self._button_close.grid_forget()
        else:
            self._button_close.grid(row = 2, column=19, sticky="e", padx = (0, 10), pady = (0, 10))
            self._button_confirm_choose_preset.grid_forget()

    @property
    def root_data(self):
        return self._root_data

    @root_data.setter
    def root_data(self, root_data):
        self._root_data = root_data

    @property
    def choose(self):
        return self._choose

    @choose.setter
    def choose(self, choose):
        self._choose = choose
        if self._choose is True:
            self._button_confirm_choose_preset.grid(row = 2, column=18, sticky="e", padx = (0, 10), pady = (0, 10))
            self._button_close.grid_forget()
        else:
            self._button_close.grid(row = 2, column=19, sticky="e", padx = (0, 10), pady = (0, 10))
            self._button_confirm_choose_preset.grid_forget()

    def on_table_cell_selected(self, e):
        self._new_preset_creating = False
        currently_selected = self._preset_table_frame._sheet.get_currently_selected()
        row = currently_selected.row
        self._selected_preset = self.root_data.preset[row]
        self._preset_detail_frame.preset = self.root_data.preset[row]
        self._button_new_preset.configure(state="normal")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="normal" if self.root_data.preset[row]["editable"] is True else "disabled")
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)
        self._button_confirm_choose_preset.configure(state="normal")

    def _on_new_preset_clicked(self):
        self._new_preset_creating = True
        self._selected_preset = None
        self._preset_detail_frame.preset = self._selected_preset
        self._button_new_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="disabled")
        self._preset_table_frame.deselect()
        self._preset_detail_frame.set_elements_state("normal")
        self._preset_detail_frame._var_preset_name.set("")
        self._preset_detail_frame._output_path.set(get_download_folder())
        self._button_save_preset.configure(state="disabled")
        self._preset_detail_frame.set_visibility_button_cancel_and_ok(True)
        self._preset_detail_frame.grid(row = 1, column = 5, sticky = "nswe", columnspan = 15, padx = 10, pady = 10)
        self._button_confirm_choose_preset.configure(state="disabled")
        
    def on_new_preset_cancel_clicked(self):
        self._new_preset_creating = False
        self._button_new_preset.configure(state="normal")
        self._preset_detail_frame.clear_all_input()
        self._preset_detail_frame.set_visibility_button_cancel_and_ok(False)
        self._preset_detail_frame.grid_forget()
        self._button_confirm_choose_preset.configure(state="disabled")

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
        self._new_preset_creating = False
        self._button_confirm_choose_preset.configure(state="normal")

    def _on_delete_preset_clicked(self):
        self._preset_detail_frame.show_confirm_delete_message(self._selected_preset)

    def on_preset_confirm_delete_clicked(self, preset_info):
        preset_id = preset_info["id"]
        prev_current_preset_id = self.root_data.current_preset["id"]
        preset.delete(preset_id)
        self.root_data.preset = preset.get_all()
        if preset_id == prev_current_preset_id:
            self.root_data.current_preset = self.root_data.preset[0]
            self.root_data._settings_frame.display(self.root_data.current_preset)
        self._selected_preset = self.root_data.preset[0]
        self._preset_detail_frame.preset = self._selected_preset
        self._preset_table_frame.display(self.root_data.preset)
        self._preset_table_frame._sheet.add_row_selection(row=0, redraw=True, run_binding_func=True)
        self._button_confirm_choose_preset.configure(state="normal")

    def enable_button_save(self, _, __, ___):
        if self._new_preset_creating is False:
            self._button_save_preset.configure(state="normal")

    def update_preset(self, preset_data):
        preset.update(preset_data)
        if preset_data["id"] == self.root_data.current_preset["id"]:
            self.root_data.current_preset.update(preset_data)
            if self.root_data._table_frame._sheet.get_currently_selected():
                self._parent.set_visibility_buttons_frame(False)
            else:
                self.root_data._settings_frame.display(self.root_data.current_preset)
        currently_selected = self._preset_table_frame._sheet.get_currently_selected()
        row = currently_selected.row
        self.root_data.preset = preset.get_all()
        self.root_data.current_preset = self.root_data.preset[row]
        self._preset_table_frame.display(self.root_data.preset)
        self._preset_table_frame._sheet.add_row_selection(row=row, redraw=True, run_binding_func=True)
        self._button_confirm_choose_preset.configure(state="normal")

    def _on_save_preset_clicked(self):
        self._preset_detail_frame._on_update_preset_clicked()

    def on_table_deselected(self, e):
        self._selected_preset = None
        self._preset_detail_frame.preset = self._selected_preset
        self._button_new_preset.configure(state="normal")
        self._button_save_preset.configure(state="disabled")
        self._button_delete_preset.configure(state="disabled")
        self._preset_detail_frame.grid_forget()
        self._button_confirm_choose_preset.configure(state="disabled")

    def _on_preset_chosen(self):
        self.root_data.current_preset = self._selected_preset
        self.root_data._settings_frame.display(self.root_data.current_preset)
        self.root_data.displaying_video_settings = False
        self._parent.set_visibility_buttons_frame(True)
        self.destroy()

    def on_main_window_preset_updated(self):
        currently_selected = self._preset_table_frame._sheet.get_currently_selected()
        self._preset_table_frame.display(self.root_data.preset)
        if currently_selected:
            row = currently_selected.row
            self._preset_table_frame._sheet.add_row_selection(row=row, redraw=True, run_binding_func=True)
            self._button_confirm_choose_preset.configure(state="normal")


