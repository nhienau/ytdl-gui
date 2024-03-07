import customtkinter as ctk

class DetailTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.grid_columnconfigure((0, 1), weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.add("Info")
        self.add("Settings")

        self.info_frame = InfoFrame(master=self.tab("Info"))
        self.info_frame.grid()

        self.settings_frame = SettingsFrame(master=self.tab("Settings"))
        self.settings_frame.grid(row=0, column=0, sticky="nswe")