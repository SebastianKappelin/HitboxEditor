import tkinter as tk

# import tkinter.ttk as ttk
from tkinter import *

# from tkinter.ttk import *
from character import Character
from PIL import Image


class CharacterSettingsWindow(tk.Toplevel):
    def __init__(
        self, title, character_attributes, template, apply_function, do_after=None
    ):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.grab_set()

        self.attributes = {}
        self.numbers = {}

        def only_numbers(input):
            if len(input) == 0:
                return True
            if input[0] == "-":
                for i in range(1, len(input)):
                    if not input[i].isdigit():
                        return False
                return True
            if not input.isdigit():
                return False
            return True

        def only_positive_numbers(input):
            if len(input) == 0:
                return True
            if not input.isdigit():
                return False
            return True

        only_numbers = self.register(only_numbers)
        only_positive_numbers = self.register(only_positive_numbers)
        current_row = 0

        for k, v in template.items():
            if v == int:
                self.numbers[k] = tk.Entry(
                    self,
                    validate="key",
                    validatecommand=(only_numbers, "%P"),
                )
                self.numbers[k].delete(0, END)
                self.numbers[k].insert(0, character_attributes[k])
                self.numbers[k].grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(self, text=k)
                description.bind(
                    "<ButtonPress-1>", lambda e, c=self.numbers[k]: c.focus()
                )
            elif v == "positive":
                self.numbers[k] = tk.Entry(
                    self,
                    validate="key",
                    validatecommand=(only_positive_numbers, "%P"),
                )
                self.numbers[k].delete(0, END)
                self.numbers[k].insert(0, character_attributes[k])
                self.numbers[k].grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(self, text=k)
                description.bind(
                    "<ButtonPress-1>", lambda e, c=self.numbers[k]: c.focus()
                )
            elif v == str:
                self.attributes[k] = tk.Entry(self)
                self.attributes[k].delete(0, END)
                self.attributes[k].insert(0, character_attributes[k])
                self.attributes[k].grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(self, text=k)
                description.bind(
                    "<ButtonPress-1>", lambda e, c=self.attributes[k]: c.focus()
                )
            elif v == bool:
                self.attributes[k] = IntVar()
                self.attributes[k].set(character_attributes[k])
                check_button = tk.Checkbutton(self, variable=self.attributes[k])
                check_button.grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(self, text=k)
                description.bind(
                    "<ButtonPress-1>",
                    lambda e, c=self.attributes[k]: c.set(c.get() == 0),
                )
            elif v == "category":  # Only used for characters.
                self.attributes[k] = StringVar(value=character_attributes[k])
                option = tk.OptionMenu(
                    self, self.attributes[k], *Character.action_categories
                )
                option.grid(row=current_row, column=1, sticky="ew")
                description = tk.Label(self, text=k)
            elif v == "image":  # Only used for characters.
                self.attributes[k] = tk.Entry(self, width=50)
                self.attributes[k].delete(0, END)
                self.attributes[k].insert(0, character_attributes[k])
                self.attributes[k].grid(row=current_row, column=1, sticky="ew")
                key = k  # Save value so it doesn't get overwritten later
                description = tk.Button(
                    self,
                    text="spritesheet",
                    command=lambda: self.select_spritesheet(key),
                )
            else:
                continue
            description.grid(row=current_row, column=0)
            current_row += 1

        b = tk.Button(
            self,
            text="apply",
            command=lambda: self.apply(character_attributes, apply_function, do_after),
        )
        b.grid(row=current_row)
        self.mainloop()

    def apply(self, character_attributes, apply_function, do_after):
        apply_attributes = {}
        for k, v in self.numbers.items():
            if v.get() == "" or v.get() == "-":
                apply_attributes[k] = 0
            else:
                apply_attributes[k] = int(v.get())
        for k, v in self.attributes.items():
            apply_attributes[k] = v.get()
        apply_function(character_attributes, apply_attributes)
        if do_after:
            do_after()
        self.destroy()

    # TODO limit filetypes to what pyglet can handle
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
            self.attributes[key].delete(0, END)
            self.attributes[key].insert(0, filepath)