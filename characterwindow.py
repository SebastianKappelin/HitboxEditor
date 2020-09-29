import tkinter as tk

# import tkinter.ttk as ttk
from tkinter import *

# from tkinter.ttk import *
from character import Character
from PIL import Image


class CharacterWindow:
    def __init__(self, character, update_image):
        top = Toplevel()

        self.entries = {}
        self.labels = {}

        def only_numbers(input):
            for i in range(len(input)):
                if not input.isdigit():
                    return False
            return True

        numbers = top.register(only_numbers)

        current_row = 0

        for k, v in Character.template.items():
            if v == int:
                self.entries[k] = tk.Entry(
                    top, validate="key", validatecommand=(numbers, "%P")
                )
                self.entries[k].delete(0, END)
                self.entries[k].insert(0, character.attributes[k])
                self.entries[k].grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(top, text=k)
            elif v == str:
                self.entries[k] = tk.Entry(top)
                self.entries[k].delete(0, END)
                self.entries[k].insert(0, character.attributes[k])
                self.entries[k].grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(top, text=k)
            elif v == "image":
                self.labels[k] = tk.Label(top, text=character.attributes[k])
                self.labels[k].grid(row=current_row, column=1, sticky="ew")
                key = k  # Save value so it doesn't get overwritten later
                description = tk.Button(
                    top,
                    text="spritesheet",
                    command=lambda: self.select_spritesheet(key),
                )
            else:
                continue
            description.grid(row=current_row, column=0)
            current_row += 1

        b = tk.Button(
            top, text="apply", command=lambda: self.apply(character, top, update_image)
        )
        b.grid(row=current_row)

        top.mainloop()

    def apply(self, character, window, update_image):
        for key, value in self.entries.items():
            character.attributes[key] = value.get()
        for key, value in self.labels.items():
            character.attributes[key] = value.cget("text")
        update_image()
        window.destroy()

    def select_spritesheet(self, key):
        try:
            filepath = tk.filedialog.askopenfilename(
                title="Select spritesheet", filetypes=[("Image File", ".*")]
            )
            if not filepath:
                return
            image = Image.open(filepath)
        except:
            top = tk.Toplevel()
            message = tk.Label(
                master=top,
                text="Need to select an image",
                foreground="white",
                background="black",
            )
            message.pack()
            top.mainloop()
        else:
            if not filepath:
                return
            self.labels[key].config(text=filepath)