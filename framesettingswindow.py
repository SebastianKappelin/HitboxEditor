import tkinter as tk
from tkinter import *
from editorframe import CoordinatesStyle

"""
Only used for adjusting the EditorFrame's settings.
"""


class FrameSettingsWindow(tk.Toplevel):
    def __init__(self, settings, show_image):
        tk.Toplevel.__init__(self)
        self.title("Frame Settings")

        def only_numbers(input):
            for i in range(len(input)):
                if not input.isdigit():
                    return False
            return True

        numbers = self.register(only_numbers)

        x_label = tk.Label(self, text="x margin")
        x_label.grid(row=0, column=0, sticky="w")

        self.x = tk.Entry(self)
        self.x.config(validate="key", validatecommand=(numbers, "%P"))
        self.x.delete(0, END)
        self.x.insert(0, settings["margin x"])
        self.x.grid(row=0, column=1, sticky="w")

        y_label = tk.Label(self, text="y margin")
        y_label.grid(row=1, column=0, sticky="w")

        self.y = tk.Entry(self)
        self.y.config(validate="key", validatecommand=(numbers, "%P"))
        self.y.delete(0, END)
        self.y.insert(0, settings["margin y"])
        self.y.grid(row=1, column=1, sticky="w")

        coord_label = tk.Label(self, text="coordinates style")
        coord_label.grid(row=3, column=0, sticky="w")

        self.coordinates = IntVar()
        self.coordinates.set(settings["coordinates style"].value)

        current_row = 2

        for e in CoordinatesStyle:
            b = tk.Radiobutton(
                self, text=e.name, variable=self.coordinates, value=e.value
            )
            b.grid(row=current_row, column=1, sticky="w")
            current_row += 1

        self.position = BooleanVar()
        self.position.set(settings["position focus"])

        position_label = tk.Label(self, text="focus on position")
        position_label.grid(row=5, column=0, sticky="w")

        b = tk.Radiobutton(self, text="True", variable=self.position, value=True)
        b.grid(row=current_row, column=1, sticky="w")
        current_row += 1

        b = tk.Radiobutton(self, text="False", variable=self.position, value=False)
        b.grid(row=current_row, column=1, sticky="w")
        current_row += 1

        b = tk.Button(
            self, text="apply", command=lambda: self.apply(settings, show_image)
        )
        b.grid(row=current_row)

        self.mainloop()

    def apply(self, settings, show_image):
        settings["margin x"] = int(self.x.get())
        settings["margin y"] = int(self.y.get())
        settings["coordinates style"] = CoordinatesStyle(self.coordinates.get())
        settings["position focus"] = self.position.get()
        show_image()
        self.destroy()
