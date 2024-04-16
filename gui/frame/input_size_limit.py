import customtkinter as ctk

class InputSizeLimitFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self._label_smaller = ctk.CTkLabel(self, text="(<")
        self._label_smaller.grid(row=0, column=0, sticky="w")

        self.size_limit = ctk.DoubleVar(value="")
        self._input_size_limit = ctk.CTkEntry(self, width=48, textvariable=self.size_limit)
        self._input_size_limit.grid(row=0, column=1, padx=(5, 5), sticky="w")

        self._label_megabyte = ctk.CTkLabel(self, text="MB)")
        self._label_megabyte.grid(row=0, column=2, sticky="w")

    
