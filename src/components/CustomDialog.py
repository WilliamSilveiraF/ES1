import tkinter as tk
from tkinter import ttk

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title=None, message=None, buttons=None):
        super().__init__(parent)

        self.title(title)
        self.resizable(False, False)

        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        self.message = ttk.Label(self.frame, text=message)
        self.message.pack(padx=10, pady=10)

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        if buttons is not None:
            for button in buttons:
                btn = ttk.Button(self.button_frame, text=button['text'], command=button['command'])
                btn.pack(side="left", padx=5)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
