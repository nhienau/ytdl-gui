import customtkinter as ctk

from gui.frame.control import ControlFrame
from gui.frame.settings import SettingsFrame
from gui.frame.table import TableFrame

data = [
    # {
    #     "id": "W-U5_m35scM",
    #     "title": "CS2's Smallest Update... yet",
    #     "video": True,
    #     "audio": True,
    #     "progress": 0,
    #     "status": "abc",
    #     "length": 96,
    #     "size": 210731313,
    #     "subtitle": True,
    #     "thumbnail": True,
    #     "sponsorblock": False,
    # }
    [False, "W-U5_m35scM", "CS2's Smallest Update... yet", True, True, 0, "abc", 96, 2107931313, True, True, False],
    [False, "W-U5_m35scM", "CS2's Smallest Update... yet", True, True, 0, "abc", 96, 2107931313, True, True, False]
]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ytdl-gui")
        self.geometry("1152x648")
        self.grid_columnconfigure(tuple([val for val in range(0, 20)]), weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.set_appearance_mode("light")
        
        self._control_frame = ControlFrame(self)
        self._control_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nswe", columnspan=20)
        
        self._settings_frame = SettingsFrame(self)
        self._settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nswe", columnspan=4)

        self._table_frame = TableFrame(self, data=data)
        self._table_frame.grid(row=1, column=4, padx=(5, 10), pady=10, sticky="nswe", columnspan=16)

        
