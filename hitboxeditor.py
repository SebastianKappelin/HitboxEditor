import tkinter as tk
import json
from imageframe import ImageFrame
from editorframe import EditorFrame
from cropwindow import CropWindow
from framesettingswindow import FrameSettingsWindow
from checkboxwindow import CheckboxWindow
from character import Character
from characterwindow import CharacterWindow
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk

"""
Main window for the program.
There are currently many planned features yet to be implemented here.
"""


class HitboxEditor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.character = None
        self.unsaved_changes = False

        # Setting up all widgets
        self.title("Hitbox Editor")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.list_frame = tk.Frame(master=self, width=200, height=50, bg="green")
        self.list_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.file_frame = tk.Frame(master=self, width=50, height=200, bg="blue")
        self.file_frame.pack(fill=tk.Y, side=tk.LEFT)

        self.tool_frame = tk.Frame(master=self, width=200, height=50, bg="red")
        self.tool_frame.pack(fill=tk.X, side=tk.TOP)

        self.data_frame = tk.Frame(master=self, width=50, height=200, bg="yellow")
        self.data_frame.pack(fill=tk.Y, side=tk.RIGHT)

        self.editor_frame = EditorFrame(self)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.new_character_button = tk.Button(
            self.file_frame, text="new character", command=self.new_character
        )
        self.new_character_button.grid(row=1, column=0, sticky="ew")

        self.open_chraracter_button = tk.Button(
            self.file_frame, text="open character", command=self.open_character
        )
        self.open_chraracter_button.grid(row=2, column=0, sticky="ew")

        self.save_character_button = tk.Button(
            self.file_frame, text="save character", command=self.save_character
        )
        self.save_character_button.grid(row=3, column=0, sticky="ew")

        self.add_frame_button = tk.Button(
            self.file_frame, text="new frame", command=self.add_frame
        )
        self.add_frame_button.grid(row=4, column=0, sticky="ew")

        self.delete_frame_button = tk.Button(
            self.file_frame, text="delete frame", command=self.delete_animation_frame
        )
        self.delete_frame_button.grid(row=5, column=0, sticky="ew")

        self.copy_frame_button = tk.Button(
            self.file_frame, text="copy frame", command=self.copy_animation_frame
        )
        self.copy_frame_button.grid(row=6, column=0, sticky="ew")

        self.paste_frame_button = tk.Button(
            self.file_frame, text="paste frame", command=self.paste_animation_frame
        )
        self.paste_frame_button.grid(row=7, column=0, sticky="ew")

        self.frame_settings_button = tk.Button(
            self.file_frame, text="frame settings", command=self.frame_settings
        )
        self.frame_settings_button.grid(row=8, column=0, sticky="ew")

        self.character_attributes_button = tk.Button(
            self.file_frame,
            text="character attributes",
            command=self.character_attributes,
        )
        self.character_attributes_button.grid(row=9, column=0, sticky="ew")

        self.select_action_button = tk.Button(
            self.file_frame, text="select action", command=self.select_action
        )
        self.select_action_button.grid(row=10, column=0, sticky="ew")

        self.box_mode_button = tk.Button(
            self.tool_frame, text="box mode", command=self.box_mode
        )
        self.box_mode_button.grid(row=0, column=1)

        self.box_types_button = tk.Button(
            self.tool_frame, text="box types", command=self.box_types
        )
        self.box_types_button.grid(row=0, column=2)

        self.position_mode_button = tk.Button(
            self.tool_frame, text="position", command=self.position_mode
        )
        self.position_mode_button.grid(row=0, column=3, sticky="ns")

        self.zoom_in_button = tk.Button(
            self.tool_frame, text="+", command=self.editor_frame.zoom_in
        )
        self.zoom_in_button.grid(row=0, column=4, sticky="ns")

        self.zoom_out_button = tk.Button(
            self.tool_frame, text="-", command=self.editor_frame.zoom_out
        )
        self.zoom_out_button.grid(row=0, column=5, sticky="ns")

        self.left_button = tk.Button(
            self.tool_frame, text="<-", command=self.previous_frame
        )
        self.left_button.grid(row=0, column=6, sticky="ns")

        self.right_button = tk.Button(
            self.tool_frame, text="->", command=self.next_frame
        )
        self.right_button.grid(row=0, column=7, sticky="ns")

        self.x_label = tk.Label(
            self.tool_frame,
            textvariable=self.editor_frame.x_var,
            foreground="white",
            background="black",
        )
        self.x_label.grid(row=0, column=9, sticky="ns")

        self.y_label = tk.Label(
            self.tool_frame,
            textvariable=self.editor_frame.y_var,
            foreground="white",
            background="black",
        )
        self.y_label.grid(row=0, column=10, sticky="ns")

        data_label1 = tk.Label(
            master=self.data_frame,
            text="placeholder move data",
            foreground="white",
            background="black",
        )
        data_label1.pack()

        self.current_frame_var = StringVar()
        self.total_frames_var = StringVar()

        self.current_frame_label = tk.Label(
            master=self.list_frame,
            textvariable=self.current_frame_var,
            foreground="black",
            background="white",
        )
        self.current_frame_label.pack(side=tk.LEFT)

        self.total_frames_label = tk.Label(
            master=self.list_frame,
            textvariable=self.total_frames_var,
            foreground="black",
            background="white",
        )
        self.total_frames_label.pack(side=tk.LEFT)

        self.initialize()

    # Used to setup the program on startup and new/open project
    def initialize(self):
        self.editor_frame.set_character(self.character)
        self.raise_all_mode_buttons()
        self.update()

    def new_character(self):
        question = "yes"
        if self.unsaved_changes:
            question = tk.messagebox.askquestion(
                "Unsaved changes",
                "Are you sure you want to continue? Unsaved changes will be lost",
                icon="warning",
            )
        if question == "yes":
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
                self.image_path = filepath
                ImageFrame.image = image
                self.character = Character(image=filepath)
                self.unsaved_changes = True
                self.initialize()

    # Files are in JSON format
    def open_character(self):
        filepath = tk.filedialog.askopenfilename(
            title="Select Project", filetypes=[("Character Project File", "*.char")]
        )
        if not filepath:
            return
        self.initialize()
        f = open(filepath, "r")
        self.character = Character(character=json.load(f))
        f.close()
        self.initialize()
        self.update_image()
        self.unsaved_changes = False

    def save_character(self):
        filepath = asksaveasfilename(
            defaultextension="char", filetypes=[("Project file", "*.char")]
        )
        if not filepath:
            return
        # f = open("/home/chrx/Kod/Hitbox/shredder.char", "w+")
        # json.dump(self.collect_project_as_json(), f, indent=4)
        f = open(filepath, "w+")
        json.dump(self.character.attributes, f, indent=6)
        f.close()
        self.unsaved_changes = False

    def update_image(self):
        ImageFrame.image = Image.open(self.character.attributes["image path"])
        self.editor_frame.show_image()

    def add_frame(self):
        CropWindow(self.character.create_animation_frame, self.update)

    def delete_animation_frame(self):
        self.character.delete_animation_frame()
        self.update()
        self.unsaved_changes = True

    # Creates a copy of the current frame along with all its data
    def copy_animation_frame(self):
        self.character.copy_animation_frame()
        self.update_button_states()

    def paste_animation_frame(self):
        self.character.paste_animation_frame()
        self.update()

    def frame_settings(self):
        FrameSettingsWindow(self.editor_frame.settings, self.editor_frame.show_image)

    def character_attributes(self):
        CharacterWindow(self.character, self.update_image)

    def select_action(self):
        pass

    def set_position(self, position):
        self.character.set_position(position)
        self.editor_frame.update_most_extreme_positions()
        self.unsaved_changes = True

    def create_box(self, box):
        self.character.create_box(box)
        self.update()
        self.unsaved_changes = True

    def box_mode(self):
        self.raise_all_mode_buttons()
        self.box_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.box_mode()

    def box_types(self):
        CheckboxWindow(Character.box_types)

    def position_mode(self):
        self.raise_all_mode_buttons()
        self.position_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.position_mode()

    def previous_frame(self):
        self.character.previous_frame()
        self.update()

    def next_frame(self):
        self.character.next_frame()
        self.update()

    def raise_all_mode_buttons(self):
        self.box_mode_button.config(relief=tk.RAISED)
        self.position_mode_button.config(relief=tk.RAISED)

    def disable_all_tool_buttons(self):
        self.box_mode_button.config(state=tk.DISABLED)
        self.box_types_button.config(state=tk.DISABLED)
        self.position_mode_button.config(state=tk.DISABLED)
        self.zoom_in_button.config(state=tk.DISABLED)
        self.zoom_out_button.config(state=tk.DISABLED)
        self.left_button.config(state=tk.DISABLED)
        self.right_button.config(state=tk.DISABLED)

    def activate_all_tool_buttons(self):
        self.box_mode_button.config(state=tk.ACTIVE)
        self.box_types_button.config(state=tk.ACTIVE)
        self.position_mode_button.config(state=tk.ACTIVE)
        self.zoom_in_button.config(state=tk.ACTIVE)
        self.zoom_out_button.config(state=tk.ACTIVE)
        self.left_button.config(state=tk.ACTIVE)
        self.right_button.config(state=tk.ACTIVE)

    def update(self):
        self.update_button_states()
        self.update_frame_counters()
        self.editor_frame.show_image()

    def update_frame_counters(self):
        if self.character:
            self.current_frame_var.set(
                "current frame: {}".format(self.character.current_frame + 1)
            )
            self.total_frames_var.set(
                "total frames: {}".format(self.character.get_total_frames())
            )

    def update_button_states(self):
        if self.character:
            self.activate_all_tool_buttons()
            self.character_attributes_button.config(state=tk.ACTIVE)
            self.frame_settings_button.config(state=tk.ACTIVE)
            self.select_action_button.config(state=tk.ACTIVE)
            if self.character.current_frame >= 0:
                self.delete_frame_button.config(state=tk.ACTIVE)
                self.copy_frame_button.config(state=tk.ACTIVE)
            else:
                self.delete_frame_button.config(state=tk.DISABLED)
                self.copy_frame_button.config(state=tk.DISABLED)
            if self.character.image_chosen():
                self.add_frame_button.config(state=tk.ACTIVE)
                self.save_character_button.config(state=tk.ACTIVE)
            else:
                self.add_frame_button.config(state=tk.DISABLED)
                self.save_character_button.config(state=tk.DISABLED)
            if self.character.copied_frame:
                self.paste_frame_button.config(state=tk.ACTIVE)
            else:
                self.paste_frame_button.config(state=tk.DISABLED)
        else:
            self.disable_all_tool_buttons()
            self.save_character_button.config(state=tk.DISABLED)
            self.add_frame_button.config(state=tk.DISABLED)
            self.delete_frame_button.config(state=tk.DISABLED)
            self.copy_frame_button.config(state=tk.DISABLED)
            self.paste_frame_button.config(state=tk.DISABLED)
            self.character_attributes_button.config(state=tk.DISABLED)
            self.frame_settings_button.config(state=tk.DISABLED)
            self.select_action_button.config(state=tk.DISABLED)

    def close_window(self):
        if self.unsaved_changes:
            question = tk.messagebox.askquestion(
                "Unsaved changes",
                "Are you sure you want to exit? Unsaved changes will be lost",
                icon="warning",
            )
            if question == "yes":
                self.destroy()
            else:
                return
        else:
            self.destroy()
