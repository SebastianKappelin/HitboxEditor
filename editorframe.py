import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from imageframe import ImageFrame

"""
Tool for creating and showing boxes/position for individual animation frames
"""


class EditorFrame(ImageFrame):

    stipple = "gray50"
    alpha = 128

    def __init__(self, mainframe):
        ImageFrame.__init__(self, mainframe)

    def initialize(self):
        self.animation_frame = None
        self.images = []
        self.update_canvas()

    def create_position(self, event):
        self.master.create_position(
            (
                int(self.canvas.canvasx(event.x) / self.zoom_factor),
                int(self.canvas.canvasy(event.y) / self.zoom_factor),
            )
        )

    def create_box(self, event):
        if self.crop_rectangle == None:
            return
        self.canvas.delete(self.crop_rectangle)
        box = {}
        if self.x0 < self.x1:
            box["x0"] = self.x0
            box["x1"] = self.x1
        else:
            box["x0"] = self.x1
            box["x1"] = self.x0
        if self.y0 < self.y1:
            box["y0"] = self.y0
            box["y1"] = self.y1
        else:
            box["y0"] = self.y1
            box["y1"] = self.y0
        self.master.create_box(box)

    # Uses animation_frame to only draw a crop of the full image
    def show_image(self, event=None):
        if self.animation_frame == None or ImageFrame.image == None:
            return
        else:
            self.canvas.delete("all")
            imagetk = ImageTk.PhotoImage(
                ImageFrame.image.crop(
                    (
                        self.animation_frame.crop["x0"],
                        self.animation_frame.crop["y0"],
                        self.animation_frame.crop["x1"],
                        self.animation_frame.crop["y1"],
                    )
                ).resize(
                    (
                        self.animation_frame.get_crop_width() * self.zoom_factor,
                        self.animation_frame.get_crop_height() * self.zoom_factor,
                    )
                )
            )
        imageid = self.canvas.create_image(
            self.margin[0] * self.zoom_factor,
            self.margin[1] * self.zoom_factor,
            anchor="nw",
            image=imagetk,
        )
        self.canvas.lower(imageid)  # Setting image as background
        self.canvas.imagetk = imagetk  # Avoiding garbage collection
        self.draw_shapes()

    # Draws all boxes and position in animation_frame that's set to visible
    def draw_shapes(self):
        boxes = self.animation_frame.get_boxes()
        self.images = []
        for i in range(len(boxes)):
            transparent_color = self.master.winfo_rgb(boxes[i]["color"]) + (
                EditorFrame.alpha,
            )
            image = Image.new(
                "RGBA",
                (
                    (boxes[i]["box"]["x1"] - boxes[i]["box"]["x0"]) * self.zoom_factor,
                    (boxes[i]["box"]["y1"] - boxes[i]["box"]["y0"]) * self.zoom_factor,
                ),
                transparent_color,
            )
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(
                boxes[i]["box"]["x0"] + self.margin[0] * self.zoom_factor,
                boxes[i]["box"]["y0"] + self.margin[1] * self.zoom_factor,
                image=self.images[i],
                anchor="nw",
            )
            self.canvas.create_rectangle(
                boxes[i]["box"]["x0"] + self.margin[0],
                boxes[i]["box"]["y0"] + self.margin[1],
                boxes[i]["box"]["x1"] + self.margin[0],
                boxes[i]["box"]["y1"] + self.margin[1],
                outline=boxes[i]["color"],
            )
        position = self.animation_frame.get_position()
        if position:
            self.canvas.create_polygon(
                [
                    position["x"] + self.margin[0] - 5,
                    position["y"] + self.margin[1],
                    position["x"] + self.margin[0],
                    position["y"] + self.margin[1] - 5,
                    position["x"] + self.margin[0] + 5,
                    position["y"] + self.margin[1],
                    position["x"] + self.margin[0],
                    position["y"] + self.margin[1] + 5,
                ],
                fill=position["color"],
                stipple=EditorFrame.stipple,
            )
            self.canvas.create_line(
                position["x"] - 2, position["y"], position["x"] + 2, position["y"]
            )
            self.canvas.create_line(
                position["x"], position["y"] - 2, position["x"], position["y"] + 2
            )
        self.canvas.scale("all", 0, 0, self.zoom_factor, self.zoom_factor)

    # Not implemented yet
    def set_margin(self, margin):
        self.margin = margin
        self.update_canvas()
        self.show_image()

    # Not implemented yet
    def create_corner_markers(self):
        self.canvas.create_line(
            self.margin[0] - 2,
            self.margin[1] + self.height,
            self.margin[0] + 2,
            self.margin[1] + self.height,
        )
        self.canvas.create_line(
            self.margin[0],
            self.margin[1] + self.height - 2,
            self.margin[0],
            self.margin[1] + self.height + 2,
        )

    def set_image_dimensions(self, dimensions):
        self.image_size = dimensions
        self.update_canvas()
        self.show_image()

    def set_animation_frame(self, animation_frame):
        self.animation_frame = animation_frame
        self.show_image()

    def position_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.create_position)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def box_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.crop_from)
        self.canvas.bind("<B1-Motion>", self.crop_to)
        self.canvas.bind("<ButtonRelease-1>", self.create_box)
