import tkinter as tk
import copy
import json
from imageframe import ImageFrame
from editorframe import EditorFrame
from cropwindow import CropWindow
from animationframe import AnimationFrame
from framesettingswindow import FrameSettingsWindow
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
        # Setting up all widgets
        self.title("Hitbox Editor")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.list_frame = tk.Frame(master=self, width=200, height=50, bg="green")
        self.list_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.tool_frame = tk.Frame(master=self, width=200, height=50, bg="red")
        self.tool_frame.pack(fill=tk.X, side=tk.TOP)

        self.file_frame = tk.Frame(master=self, width=50, height=200, bg="blue")
        self.file_frame.pack(fill=tk.Y, side=tk.LEFT)

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

        self.hitbox_mode_button = tk.Button(
            self.tool_frame, text="hitbox", command=self.hitbox_mode
        )
        self.hitbox_mode_button.grid(row=0, column=0, sticky="ns")

        # listbox = Listbox(self.tool_frame)
        # listbox.insert(END, "a list entry")

        # for item in ["one", "two", "three", "four"]:
        #     listbox.insert(END, item)

        # listbox.grid(row=0, column=1)

        self.hurtbox_mode_button = tk.Button(
            self.tool_frame, text="hurtbox", command=self.hurtbox_mode
        )
        self.hurtbox_mode_button.grid(row=0, column=1, sticky="ns")

        self.throwbox_mode_button = tk.Button(
            self.tool_frame, text="throwbox", command=self.throwbox_mode
        )
        self.throwbox_mode_button.grid(row=0, column=2, sticky="ns")

        self.pushbox_mode_button = tk.Button(
            self.tool_frame, text="pushbox", command=self.pushbox_mode
        )
        self.pushbox_mode_button.grid(row=0, column=3, sticky="ns")

        self.position_mode_button = tk.Button(
            self.tool_frame, text="position", command=self.position_mode
        )
        self.position_mode_button.grid(row=0, column=4, sticky="ns")

        self.zoom_in_button = tk.Button(
            self.tool_frame, text="+", command=self.editor_frame.zoom_in
        )
        self.zoom_in_button.grid(row=0, column=5, sticky="ns")

        self.zoom_out_button = tk.Button(
            self.tool_frame, text="-", command=self.editor_frame.zoom_out
        )
        self.zoom_out_button.grid(row=0, column=6, sticky="ns")

        self.left_button = tk.Button(
            self.tool_frame, text="<-", command=self.previous_frame
        )
        self.left_button.grid(row=0, column=7, sticky="ns")

        self.right_button = tk.Button(
            self.tool_frame, text="->", command=self.next_frame
        )
        self.right_button.grid(row=0, column=8, sticky="ns")

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

        # Setting up variables
        self.image_path = None
        self.initialize()
        self.unsaved_changes = False

    # Used to setup the program on startup and new/open project
    def initialize(self):
        self.copy = None
        self.animation_frames = []
        self.current_frame = -1
        self.create_animation_frame({"x0": 0, "x1": 0, "y0": 0, "y1": 0})
        self.raise_all_mode_buttons()
        self.update_button_states()
        self.update_frame_counters()

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
        self.create_project_from_json(filepath)
        self.unsaved_changes = False

    def save_character(self):
        filepath = asksaveasfilename(
            defaultextension="char", filetypes=[("Project file", "*.char")]
        )
        if not filepath:
            return
        f = open("/home/chrx/Kod/Hitbox/shredder.char", "w+")
        json.dump(self.collect_project_as_json(), f, indent=4)
        f.close()
        self.unsaved_changes = False

    def create_project_from_json(self, filepath):
        f = open(filepath, "r")
        project = json.load(f)
        self.image_path = project["image path"]
        ImageFrame.image = Image.open(self.image_path)
        for i in range(len(project["action"])):
            animation_frame = AnimationFrame(
                hitboxes=project["action"][i]["hitboxes"],
                hurtboxes=project["action"][i]["hurtboxes"],
                throwboxes=project["action"][i]["throwboxes"],
                pushboxes=project["action"][i]["pushboxes"],
                position=(
                    project["action"][i]["position"]["x"],
                    project["action"][i]["position"]["y"],
                ),
                crop=project["action"][i]["crop"],
            )
            self.insert_animation_frame(animation_frame)
        self.editor_frame.most_extreme_positions = self.find_most_extreme_positions()

    def collect_project_as_json(self):
        project = {}
        if self.image_path:
            project["image path"] = self.image_path
        project["action"] = []
        for i in range(1, len(self.animation_frames)):
            project["action"].append(self.animation_frames[i].to_json())
        return project

    def add_frame(self):
        CropWindow(self.create_animation_frame)

    def create_animation_frame(self, crop):
        animation_frame = AnimationFrame(crop=crop)
        self.insert_animation_frame(animation_frame)

    def delete_animation_frame(self):
        if self.current_frame == 0:
            return
        self.animation_frames.pop(self.current_frame)
        if self.current_frame == len(self.animation_frames):
            self.current_frame -= 1
        self.editor_frame.set_animation_frame(self.animation_frames[self.current_frame])
        self.update_frame_counters()
        self.update_button_states()
        self.unsaved_changes = True

    # Creates a copy of the current frame along with all its data
    def copy_animation_frame(self):
        self.copy = copy.deepcopy(self.animation_frames[self.current_frame])
        self.update_button_states()

    def paste_animation_frame(self):
        self.insert_animation_frame(self.copy)

    def frame_settings(self):
        FrameSettingsWindow(self.editor_frame.settings, self.editor_frame.show_image)

    # New frame is inserted behind the current frame
    def insert_animation_frame(self, animation_frame):
        self.animation_frames.insert(self.current_frame + 1, animation_frame)
        self.current_frame += 1
        self.update_frame_counters()
        self.editor_frame.set_animation_frame(animation_frame)
        self.editor_frame.set_image_dimensions(self.find_largest_dimensions())
        self.update_button_states()
        self.unsaved_changes = True

    def create_position(self, position):
        if self.position_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].position = position
            self.editor_frame.most_extreme_positions = (
                self.find_most_extreme_positions()
            )
            self.editor_frame.show_image()
            self.unsaved_changes = True

    def create_box(self, box):
        if self.current_frame == 0:
            return
        if self.hitbox_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].hitboxes.append(box)
        elif self.hurtbox_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].hurtboxes.append(box)
        elif self.throwbox_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].throwboxes.append(box)
        elif self.pushbox_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].pushboxes.append(box)
        self.editor_frame.show_image()
        self.unsaved_changes = True

    def hitbox_mode(self):
        self.raise_all_mode_buttons()
        self.hitbox_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.box_mode()

    def hurtbox_mode(self):
        self.raise_all_mode_buttons()
        self.hurtbox_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.box_mode()

    def throwbox_mode(self):
        self.raise_all_mode_buttons()
        self.throwbox_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.box_mode()

    def pushbox_mode(self):
        self.raise_all_mode_buttons()
        self.pushbox_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.box_mode()

    def position_mode(self):
        self.raise_all_mode_buttons()
        self.position_mode_button.config(relief=tk.SUNKEN)
        self.editor_frame.position_mode()

    def previous_frame(self):
        if self.current_frame == 0:
            self.current_frame = len(self.animation_frames) - 1
        else:
            self.current_frame -= 1
        self.editor_frame.set_animation_frame(self.animation_frames[self.current_frame])
        self.update_frame_counters()
        self.update_button_states()

    def next_frame(self):
        if self.current_frame + 1 >= len(self.animation_frames):
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.editor_frame.set_animation_frame(self.animation_frames[self.current_frame])
        self.update_frame_counters()
        self.update_button_states()

    def raise_all_mode_buttons(self):
        self.hitbox_mode_button.config(relief=tk.RAISED)
        self.hurtbox_mode_button.config(relief=tk.RAISED)
        self.throwbox_mode_button.config(relief=tk.RAISED)
        self.pushbox_mode_button.config(relief=tk.RAISED)
        self.position_mode_button.config(relief=tk.RAISED)

    def find_largest_dimensions(self):
        largest_width = int(0)
        largest_height = int(0)
        for i in range(len(self.animation_frames)):
            current = self.animation_frames[i]
            if current.crop["x1"] - current.crop["x0"] > largest_width:
                largest_width = current.crop["x1"] - current.crop["x0"]
            if current.crop["y1"] - current.crop["y0"] > largest_height:
                largest_height = current.crop["y1"] - current.crop["y0"]
        return (largest_width, largest_height)

    def find_most_extreme_positions(self):
        largest_width = int(0)
        largest_height = int(0)
        for i in range(len(self.animation_frames)):
            current = self.animation_frames[i]
            if current.position:
                if current.position[0] > largest_width:
                    largest_width = current.position[0]
                if current.position[1] > largest_height:
                    largest_height = current.position[1]
        return (largest_width, largest_height)

    def update_frame_counters(self):
        self.current_frame_var.set("current frame: {}".format(self.current_frame))
        self.total_frames_var.set(
            "total frames: {}".format(len(self.animation_frames) - 1)
        )

    def update_button_states(self):
        if self.current_frame > 0:
            self.delete_frame_button.config(state=tk.ACTIVE)
            self.copy_frame_button.config(state=tk.ACTIVE)
        else:
            self.delete_frame_button.config(state=tk.DISABLED)
            self.copy_frame_button.config(state=tk.DISABLED)
        if self.image_path:
            self.add_frame_button.config(state=tk.ACTIVE)
            self.save_character_button.config(state=tk.ACTIVE)
        else:
            self.add_frame_button.config(state=tk.DISABLED)
            self.save_character_button.config(state=tk.DISABLED)
        if self.copy:
            self.paste_frame_button.config(state=tk.ACTIVE)
        else:
            self.paste_frame_button.config(state=tk.DISABLED)

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
