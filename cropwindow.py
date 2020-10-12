import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from imageframe import ImageFrame

"""
The CropWindow along with the CropImageFrame serves one purpose.
To crop the image used for the project.
"""


class CropWindow:
    def __init__(self, create_animation_frame, update):

        top = Toplevel()
        top.grab_set()

        crop_tool_frame = tk.Frame(master=top, width=200, height=50, bg="red")
        crop_frame = CropImageFrame(top)

        zoom_in_button = tk.Button(
            crop_tool_frame, text="+", command=crop_frame.zoom_in
        )
        zoom_in_button.grid(row=0, column=0, sticky="ns")

        zoom_out_button = tk.Button(
            crop_tool_frame, text="-", command=crop_frame.zoom_out
        )
        zoom_out_button.grid(row=0, column=1, sticky="ns")

        save_button = tk.Button(
            crop_tool_frame,
            text="crop image",
            command=lambda: crop_frame.close_and_create_animation_frame(
                create_animation_frame, update
            ),
        )
        save_button.grid(row=0, column=2, sticky="ns")

        x_label = tk.Label(
            crop_tool_frame,
            textvariable=crop_frame.x_var,
            foreground="white",
            background="black",
        )
        x_label.grid(row=0, column=3, sticky="ns")

        y_label = tk.Label(
            crop_tool_frame,
            textvariable=crop_frame.y_var,
            foreground="white",
            background="black",
        )
        y_label.grid(row=0, column=4, sticky="ns")

        crop_tool_frame.pack(fill=tk.X, side=tk.TOP)
        crop_frame.pack(fill=tk.BOTH, expand=True)

        top.mainloop()


class CropImageFrame(ImageFrame):
    def __init__(self, mainframe):
        ImageFrame.__init__(self, mainframe)

    def initialize(self):
        if ImageFrame.image:
            self.image_size = ImageFrame.image.size
        else:
            self.image_size = (0, 0)
        self.update_scrollregion()

    def show_image(self, event=None):
        if ImageFrame.image == None:
            return
        else:
            imagetk = ImageTk.PhotoImage(
                ImageFrame.image.resize(
                    (
                        self.image_size[0] * self.zoom_factor,
                        self.image_size[1] * self.zoom_factor,
                    )
                )
            )
        imageid = self.canvas.create_image(0, 0, anchor="nw", image=imagetk)
        self.canvas.lower(imageid)
        self.canvas.imagetk = imagetk
        self.canvas.scale("all", 0, 0, self.zoom_factor, self.zoom_factor)

    def set_crop_rectangle_in_bounds(self):
        if self.x0 < 0:
            self.x0 = 0
        elif self.x0 > self.image_size[0]:
            self.x0 = self.image_size[0]
        if self.x1 < 0:
            self.x1 = 0
        elif self.x1 > self.image_size[0]:
            self.x1 = self.image_size[0]
        if self.y0 < 0:
            self.y0 = 0
        elif self.y0 > self.image_size[1]:
            self.y0 = self.image_size[1]
        if self.y1 < 0:
            self.y1 = 0
        elif self.y1 > self.image_size[1]:
            self.y01 = self.image_size[1]

    def close_and_create_animation_frame(self, create_frame, update):
        if self.crop_rectangle == None:
            return
        self.set_crop_rectangle_in_bounds()
        coordinates = {}
        if self.x0 < self.x1:
            coordinates["x0"] = self.x0
            coordinates["x1"] = self.x1
        else:
            coordinates["x0"] = self.x1
            coordinates["x1"] = self.x0
        if self.y0 < self.y1:
            coordinates["y0"] = self.y0
            coordinates["y1"] = self.y1
        else:
            coordinates["y0"] = self.y1
            coordinates["y1"] = self.y0
        create_frame(coordinates)
        update()
        self.master.destroy()