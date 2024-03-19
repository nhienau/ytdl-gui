import customtkinter as ctk
import platform

class LoadCookiesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(tuple([val for val in range(0, 10)]), weight=1)
        
        self._supported_browsers = ["Brave", "Chrome", "Chromium", "Edge", "Firefox", "Opera", "Vivaldi"]
        self._check_platform()
        
        self.default_message = "It appears that this content does not exist or is only accessible to registered users. Please double-check the URL and ensure its correctness. If the content is private, this URL can be retrieved by allowing the use of browser cookies to obtain your account credentials."

        self.textbox_message = ctk.CTkTextbox(self)
        self.textbox_message.grid(row=0, column=0, pady=(0, 5), sticky="ew", columnspan=10)
        self.textbox_message.insert("0.0", text=self.default_message)
        self.textbox_message.configure(height=40, state="disabled", border_width=0, border_spacing=0, corner_radius=0, fg_color="transparent")

        self._allow_cookies = ctk.BooleanVar(value=False)
        self._checkbox_cookies = ctk.CTkCheckBox(self, text="Accept browser cookies", onvalue=True, offvalue=False, variable=self._allow_cookies, command=self._on_checkbox_click)
        self._checkbox_cookies.grid(row=1, column=0, pady=(0, 10), sticky="we")

        self._browser_value = ctk.StringVar(value="Select your browser")
        self._combobox_browser_name = ctk.CTkComboBox(self, values=self._supported_browsers, state="disabled", variable=self._browser_value)
        self._combobox_browser_name.grid(row=2, column=0, pady=(0, 10), sticky="we", columnspan=2)

        self._button_submit = ctk.CTkButton(self, text="OK", width=24, state="disabled", command=master.on_cookies_submit)
        self._button_submit.grid(row=2, column=2, pady=(0, 10))

    def get_browser_value(self):
        return self._browser_value.get()

    def _on_checkbox_click(self):
        checked = self._allow_cookies.get()
        if checked:
            self._combobox_browser_name.configure(state="readonly")
            self._button_submit.configure(state="normal")
        else:
            self._combobox_browser_name.configure(state="disabled")
            self._button_submit.configure(state="disabled")

    def _check_platform(self):
        if platform.system().lower() == "darwin":
            self._supported_browsers.append("Safari")
            self._supported_browsers.sort()


