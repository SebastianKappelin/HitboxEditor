import tkinter as tk
import copy
from imageframe import ImageFrame
from editorframe import EditorFrame
from cropwindow import CropWindow
from animationframe import AnimationFrame
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk


class HitboxEditor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Hitbox Editor')

        self.current_frame = -1
        self.animation_frames = []

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

        self.open_image_button = tk.Button(
            self.file_frame, text="new project", command=self.new_project
        )
        self.open_image_button.grid(row=1, column=0, sticky="ew")

        self.open_metadata_button = tk.Button(
            self.file_frame, text="open project", command=self.open_project
        )
        self.open_metadata_button.grid(row=2, column=0, sticky="ew")

        self.save_metadata_button = tk.Button(
            self.file_frame, text="save project", command=self.save_project
        )
        self.save_metadata_button.grid(row=3, column=0, sticky="ew")

        self.add_frame_button = tk.Button(
            self.file_frame, text="new frame", command=self.add_frame
        )
        self.add_frame_button.grid(row=4, column=0, sticky="ew")

        self.delete_frame_button = tk.Button(
            self.file_frame, text="delete frame", command=self.delete_frame
        )
        self.delete_frame_button.grid(row=5, column=0, sticky="ew")

        self.copy_frame_button = tk.Button(
            self.file_frame, text="copy frame", command=self.copy_frame
        )
        self.copy_frame_button.grid(row=6, column=0, sticky="ew")

        self.paste_frame_button = tk.Button(
            self.file_frame, text="paste frame", command=self.paste_frame
        )
        self.paste_frame_button.grid(row=7, column=0, sticky="ew")

        self.hitbox_mode_button = tk.Button(
            self.tool_frame, text="hitbox", command=self.hitbox_mode
        )
        self.hitbox_mode_button.grid(row=0, column=0, sticky="ns")

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

        self.initialize()

    def new_project(self):
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
                self.path = filepath
                ImageFrame.image = image
                self.unsaved_changes = True
                self.update_button_states()

    def open_project(self):
        print("open project")

    def save_project(self):
        print("save project")

    def add_frame(self):
        top = Toplevel()
        crop_window = CropWindow(top, self)
        top.mainloop()

    def create_frame(self, crop):
        animation_frame = AnimationFrame(crop=crop)
        self.animation_frames.insert(self.current_frame + 1, animation_frame)
        self.current_frame += 1
        self.update_frame_counters()
        self.editor_frame.set_animation_frame(animation_frame)
        self.editor_frame.set_image_dimensions(self.find_largest_dimensions())
        self.update_button_states()

    def delete_frame(self):
        if self.current_frame == 0:
            return
        self.animation_frames.pop(self.current_frame)
        if self.current_frame == len(self.animation_frames):
            self.current_frame -= 1
        self.editor_frame.set_animation_frame(self.animation_frames[self.current_frame])
        self.update_frame_counters()
        self.update_button_states()

    def copy_frame(self):
        self.copy = copy.deepcopy(self.animation_frames[self.current_frame])
        self.update_button_states()

    def paste_frame(self):
        self.animation_frames.insert(self.current_frame + 1, self.copy)
        self.current_frame += 1
        self.update_frame_counters()
        self.editor_frame.set_animation_frame(self.copy)
        self.copy = copy.deepcopy(self.copy)

    def create_position(self, position):
        if self.position_mode_button["relief"] == tk.SUNKEN:
            self.animation_frames[self.current_frame].position = position

    def create_rectangle(self, box):
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
        if self.path:
            self.add_frame_button.config(state=tk.ACTIVE)
        else:
            self.add_frame_button.config(state=tk.DISABLED)
        if self.copy:
            self.paste_frame_button.config(state=tk.ACTIVE)
        else:
            self.paste_frame_button.config(state=tk.DISABLED)

    def initialize(self):
        self.unsaved_changes = False
        self.copy = None
        self.animation_frames = []
        self.current_frame = -1
        self.path = None
        self.create_frame({"x0": 0, "x1": 0, "y0": 0, "y1": 0})
        self.raise_all_mode_buttons()
        self.update_button_states()
        self.update_frame_counters()