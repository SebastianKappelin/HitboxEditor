import tkinter as tk
from tkinter import *
from character import Character


class CheckboxWindow:
    def __init__(self, options):
        top = Toplevel()

        self.checkboxes = {}

        for k, v in options.items():
            self.checkboxes[k] = IntVar()
            self.checkboxes[k].set(v)
            c = tk.Checkbutton(top, text=k, variable=self.checkboxes[k])
            c.pack()

        b = tk.Button(top, text="testing", command=lambda: self.apply(options, top))
        b.pack()
        top.mainloop()

    def apply(self, options, window):
        for k, v in self.checkboxes.items():
            if v.get():
                options[k] = True
            else:
                options[k] = False
        window.destroy()