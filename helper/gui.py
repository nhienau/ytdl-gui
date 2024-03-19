def set_textbox_value(textbox, message):
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text=message)
    textbox.configure(state="disabled")
