from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from character import Character
from charactersettingswindow import CharacterSettingsWindow


class ActionsWindow(tk.Toplevel):
    def __init__(self, character, on_destroy):
        tk.Toplevel.__init__(self)
        # self.window = Toplevel()
        # self.window.grab_set()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window(on_destroy))

        self.character = character
        self.tree = ttk.Treeview(self, selectmode="browse")

        self.tree["columns"] = ("1", "2")

        self.tree.heading("#0", text="Name")
        self.tree.heading("1", text="Input")
        self.tree.heading("2", text="No. Frames")
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side=tk.LEFT)

        add_action_button = ttk.Button(
            buttons_frame, text="add action", command=self.add_action
        )
        add_action_button.pack(side=tk.TOP)

        delete_action_button = ttk.Button(
            buttons_frame, text="delete action", command=self.delete_action
        )
        delete_action_button.pack(side=tk.TOP)

        edit_action_button = ttk.Button(
            buttons_frame, text="edit action", command=self.edit_action
        )
        edit_action_button.pack(side=tk.TOP)

        Select_action_button = ttk.Button(
            buttons_frame, text="Set current action", command=self.set_current_action
        )
        Select_action_button.pack(side=tk.BOTTOM)

        vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vscrollbar.pack(side="right", fill="y")

        self.tree.config(yscrollcommand=vscrollbar.set)
        self.tree.pack()

        self.categories = {}

        for k in Character.action_categories:
            self.categories[k] = self.tree.insert("", "end", text=k, values=("", ""))

        actions = character.get_all_actions()
        for i in range(len(actions)):
            self.tree.insert(
                self.categories[character.get_action_category(actions[i])],
                "end",
                text=character.get_action_name(actions[i]),
                values=(
                    character.get_action_input(actions[i]),
                    character.get_action_total_frames(actions[i]),
                ),
            )

        self.mainloop()

    def add_action(self):
        def add(not_used, attributes):
            action = self.character.create_action(
                attributes.pop("name"), attributes.pop("category"), **attributes
            )
            if action:
                self.tree.insert(
                    self.categories[self.character.get_action_category(action)],
                    "end",
                    text=self.character.get_action_name(action),
                    values=(
                        self.character.get_action_input(action),
                        self.character.get_action_total_frames(action),
                    ),
                )
                self.character.set_current_action(action)
            else:
                self.error_popup(
                    "Couldn't add action.\nName category pair already taken"
                )

        CharacterSettingsWindow(
            "Add Action",
            self.character.create_empty_object(self.character.get_action_template()),
            self.character.get_action_template(),
            add,
        )

    def delete_action(self):
        if not self.tree.parent(self.tree.focus()):
            return
        if self.character.delete_action(
            self.tree.item(self.tree.focus())["text"],  # name
            self.tree.item(self.tree.parent(self.tree.focus()))["text"],  # category
        ):
            self.tree.delete(self.tree.focus())

    def edit_action(self):
        def edit(old_attributes, new_attributes):
            action = self.character.try_apply_action_changes(
                old_attributes, new_attributes
            )
            if not action:
                self.error_popup(
                    "Couldn't edit action.\nName category pair already taken"
                )
            else:
                self.tree.delete(self.tree.focus())
                self.tree.insert(
                    self.categories[self.character.get_action_category(action)],
                    "end",
                    text=self.character.get_action_name(action),
                    values=(
                        self.character.get_action_input(action),
                        self.character.get_action_total_frames(action),
                    ),
                )

        if not self.tree.parent(self.tree.focus()):
            return
        action = self.character.get_action(
            self.tree.item(self.tree.focus())["text"],  # name
            self.tree.item(self.tree.parent(self.tree.focus()))["text"],  # category
        )
        # if action:
        CharacterSettingsWindow(
            "Edit Action", action, self.character.get_action_template(), edit
        )

    def set_current_action(self):
        if not self.tree.parent(self.tree.focus()):
            return
        self.character.set_current_action(
            self.character.get_action(
                self.tree.item(self.tree.focus())["text"],  # name
                self.tree.item(self.tree.parent(self.tree.focus()))["text"],  # category
            )
        )

    def error_popup(self, message):
        top = tk.Toplevel()
        top.grab_set()
        lbl = tk.Label(top, text=message)
        lbl.pack()
        top.mainloop()

    def close_window(self, on_destroy):
        on_destroy()
        self.destroy()