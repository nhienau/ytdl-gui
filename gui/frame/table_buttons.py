import customtkinter as ctk
from PIL import Image

class TableButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.callbacks = {
            "move_rows_up": master.move_rows_up,
            "move_rows_down": master.move_rows_down,
            "move_rows_to_top": master.move_rows_to_top,
            "move_rows_to_bottom": master.move_rows_to_bottom,
            "delete_marked_rows": master.delete_marked_rows,
            "clear_list": master.clear_list,
        }

        self._icon_arrow_top = ctk.CTkImage(light_image=Image.open("gui/icons/arrow_top.png"), dark_image=Image.open("gui/icons/arrow_top.png"), size=(24, 24))

        self._button_move_to_top = ctk.CTkButton(self, image=self._icon_arrow_top, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["move_rows_to_top"], state="disabled")
        self._button_move_to_top.grid(row=0, column=0)

        self._icon_arrow_up = ctk.CTkImage(light_image=Image.open("gui/icons/arrow_up.png"), dark_image=Image.open("gui/icons/arrow_up.png"), size=(24, 24))

        self._button_move_up = ctk.CTkButton(self, image=self._icon_arrow_up, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["move_rows_up"], state="disabled")
        self._button_move_up.grid(row=0, column=1)

        self._icon_arrow_down = ctk.CTkImage(light_image=Image.open("gui/icons/arrow_down.png"), dark_image=Image.open("gui/icons/arrow_down.png"), size=(24, 24))

        self._button_move_down = ctk.CTkButton(self, image=self._icon_arrow_down, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["move_rows_down"], state="disabled")
        self._button_move_down.grid(row=0, column=2)

        self._icon_arrow_bottom = ctk.CTkImage(light_image=Image.open("gui/icons/arrow_bottom.png"), dark_image=Image.open("gui/icons/arrow_bottom.png"), size=(24, 24))

        self._button_move_to_bottom = ctk.CTkButton(self, image=self._icon_arrow_bottom, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["move_rows_to_bottom"], state="disabled")
        self._button_move_to_bottom.grid(row=0, column=3)

        self._icon_delete = ctk.CTkImage(light_image=Image.open("gui/icons/delete.png"), dark_image=Image.open("gui/icons/delete.png"), size=(24, 24))

        self._button_delete = ctk.CTkButton(self, image=self._icon_delete, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["delete_marked_rows"], state="disabled")
        self._button_delete.grid(row=0, column=4)

        self._icon_delete_all = ctk.CTkImage(light_image=Image.open("gui/icons/delete_all.png"), dark_image=Image.open("gui/icons/delete_all.png"), size=(24, 24))

        self._button_delete_all = ctk.CTkButton(self, image=self._icon_delete_all, text="", width=32, fg_color="transparent", hover_color="#EBEBEB", anchor="center", command=self.callbacks["clear_list"], state="disabled")
        self._button_delete_all.grid(row=0, column=5)

    def set_buttons_state(self, state):
        self._button_move_to_top.configure(state=state)
        self._button_move_up.configure(state=state)
        self._button_move_down.configure(state=state)
        self._button_move_to_bottom.configure(state=state)
        self._button_delete.configure(state=state)
        self._button_delete_all.configure(state=state)


