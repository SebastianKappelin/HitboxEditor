import tkinter as tk
from tkinter import *
from imageframe import CoordinatesStyle


class FrameSettingsWindow:
    def __init__(self, settings, show_image):

        top = Toplevel()

        def only_numbers(input):
            for i in range(len(input)):
                if not input.isdigit():
                    return False
            return True

        numbers = top.register(only_numbers)

        x_label = tk.Label(top, text="x margin")
        x_label.grid(row=0, column=0, sticky="w")

        self.x = tk.Entry(top)
        self.x.config(validate="key", validatecommand=(numbers, "%P"))
        self.x.delete(0, END)
        self.x.insert(0, settings["margin"]["x"])
        self.x.grid(row=0, column=1, sticky="w")

        y_label = tk.Label(top, text="y margin")
        y_label.grid(row=1, column=0, sticky="w")

        self.y = tk.Entry(top)
        self.y.config(validate="key", validatecommand=(numbers, "%P"))
        self.y.delete(0, END)
        self.y.insert(0, settings["margin"]["y"])
        self.y.grid(row=1, column=1, sticky="w")

        coord_label = tk.Label(top, text="coordinates style")
        coord_label.grid(row=3, column=0, sticky="w")

        self.coordinates = IntVar()
        self.coordinates.set(settings["coordinates style"].value)

        current_row = 2

        for e in CoordinatesStyle:
            b = tk.Radiobutton(
                top, text=e.name, variable=self.coordinates, value=e.value
            )
            b.grid(row=current_row, column=1, sticky="w")
            current_row += 1

        self.position = BooleanVar()
        self.position.set(settings["position focus"])

        position_label = tk.Label(top, text="focus on position")
        position_label.grid(row=5, column=0, sticky="w")

        b = tk.Radiobutton(top, text="True", variable=self.position, value=True)
        b.grid(row=current_row, column=1, sticky="w")
        current_row += 1

        b = tk.Radiobutton(top, text="False", variable=self.position, value=False)
        b.grid(row=current_row, column=1, sticky="w")
        current_row += 1

        b = tk.Button(
            top, text="apply", command=lambda: self.apply(settings, show_image, top)
        )
        b.grid(row=current_row)

        top.mainloop()

    def apply(self, settings, show_image, window):
        settings["margin"]["x"] = int(self.x.get())
        settings["margin"]["y"] = int(self.y.get())
        settings["coordinates style"] = CoordinatesStyle(self.coordinates.get())
        settings["position focus"] = self.position.get()
        show_image()
        window.destroy()
        # print(self.x.get())
        # print(self.y.get())
        # print(CoordinatesStyle(self.coordinates.get()))
        # print(self.position.get())
