import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from imageframe import ImageFrame, CoordinatesStyle

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
        # (width, height), used for centering frames on position
        self.most_extreme_positions = (0, 0)
        self.update_canvas()

    def create_position(self, event):
        self.master.create_position(
            (
                int(
                    self.canvas.canvasx(event.x) / self.zoom_factor
                    - self.settings["margin"]["x"]
                ),
                int(
                    self.canvas.canvasy(event.y) / self.zoom_factor
                    - self.settings["margin"]["x"]
                ),
            )
        )

    def create_box(self, event):
        if self.crop_rectangle == None:
            return
        self.canvas.delete(self.crop_rectangle)
        box = {}
        if self.x0 < self.x1:
            box["x0"] = self.x0 - self.settings["margin"]["x"]
            box["x1"] = self.x1 - self.settings["margin"]["x"]
        else:
            box["x0"] = self.x1 - self.settings["margin"]["x"]
            box["x1"] = self.x0 - self.settings["margin"]["x"]
        if self.y0 < self.y1:
            box["y0"] = self.y0 - self.settings["margin"]["y"]
            box["y1"] = self.y1 - self.settings["margin"]["y"]
        else:
            box["y0"] = self.y1 - self.settings["margin"]["y"]
            box["y1"] = self.y0 - self.settings["margin"]["y"]
        self.master.create_box(box)

    def show_coordinates(self, event):
        if self.settings["coordinates style"] == CoordinatesStyle.Top_left:
            self.x_var.set(
                "x: {}".format(
                    int(
                        self.canvas.canvasx(event.x) / self.zoom_factor
                        - self.settings["margin"]["x"]
                    )
                )
            )
            self.y_var.set(
                "y: {}".format(
                    int(
                        self.canvas.canvasy(event.y) / self.zoom_factor
                        - self.settings["margin"]["y"]
                    )
                )
            )
        elif self.settings["coordinates style"] == CoordinatesStyle.Bottom_left:
            self.x_var.set(
                "x: {}".format(
                    int(
                        self.canvas.canvasx(event.x) / self.zoom_factor
                        - self.settings["margin"]["x"]
                    )
                )
            )
            self.y_var.set(
                "y: {}".format(
                    int(
                        self.settings["margin"]["y"]
                        + self.animation_frame.get_crop_height()
                        - self.canvas.canvasy(event.y) / self.zoom_factor
                    )
                )
            )
        elif self.settings["coordinates style"] == CoordinatesStyle.Position:
            pos = self.animation_frame.get_position()
            if not pos:
                self.x_var.set("no position")
                self.y_var.set(" set")
            else:
                self.x_var.set(
                    "x: {}".format(
                        int(
                            self.canvas.canvasx(event.x) / self.zoom_factor
                            - pos["x"]
                            - self.settings["margin"]["x"]
                        )
                    )
                )
                self.y_var.set(
                    "y: {}".format(
                        int(
                            self.settings["margin"]["y"]
                            + pos["y"]
                            - self.canvas.canvasy(event.y) / self.zoom_factor
                        )
                    )
                )

    # Uses animation_frame to only draw a crop of the full image
    def show_image(self, event=None):
        if self.animation_frame == None or ImageFrame.image == None:
            return
        else:
            self.canvas.delete("all")
            imagetk = ImageTk.PhotoImage(
                ImageFrame.image.crop(self.animation_frame.get_crop_tuple()).resize(
                    (
                        self.animation_frame.get_crop_width() * self.zoom_factor,
                        self.animation_frame.get_crop_height() * self.zoom_factor,
                    )
                )
            )
        imageid = self.canvas.create_image(
            self.settings["margin"]["x"] * self.zoom_factor,
            self.settings["margin"]["y"] * self.zoom_factor,
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
                (boxes[i]["box"]["x0"] + self.settings["margin"]["x"])
                * self.zoom_factor,
                (boxes[i]["box"]["y0"] + self.settings["margin"]["y"])
                * self.zoom_factor,
                image=self.images[i],
                anchor="nw",
            )
            self.canvas.create_rectangle(
                (boxes[i]["box"]["x0"] + self.settings["margin"]["x"])
                * self.zoom_factor,
                (boxes[i]["box"]["y0"] + self.settings["margin"]["y"])
                * self.zoom_factor,
                (boxes[i]["box"]["x1"] + self.settings["margin"]["x"])
                * self.zoom_factor,
                (boxes[i]["box"]["y1"] + self.settings["margin"]["y"])
                * self.zoom_factor,
                outline=boxes[i]["color"],
            )
        position = self.animation_frame.get_position()
        if position:
            self.canvas.create_polygon(
                [
                    (position["x"] + self.settings["margin"]["x"] - 5)
                    * self.zoom_factor,
                    (position["y"] + self.settings["margin"]["y"]) * self.zoom_factor,
                    (position["x"] + self.settings["margin"]["x"]) * self.zoom_factor,
                    (position["y"] + self.settings["margin"]["y"] - 5)
                    * self.zoom_factor,
                    (position["x"] + self.settings["margin"]["x"] + 5)
                    * self.zoom_factor,
                    (position["y"] + self.settings["margin"]["y"]) * self.zoom_factor,
                    (position["x"] + self.settings["margin"]["x"]) * self.zoom_factor,
                    (position["y"] + self.settings["margin"]["y"] + 5)
                    * self.zoom_factor,
                ],
                fill=position["color"],
                stipple=EditorFrame.stipple,
            )
            self.canvas.create_line(
                (position["x"] - 2 + self.settings["margin"]["x"]) * self.zoom_factor,
                (position["y"] + self.settings["margin"]["y"]) * self.zoom_factor,
                (position["x"] + 2 + self.settings["margin"]["x"]) * self.zoom_factor,
                (position["y"] + self.settings["margin"]["y"]) * self.zoom_factor,
            )
            self.canvas.create_line(
                (position["x"] + self.settings["margin"]["x"]) * self.zoom_factor,
                (position["y"] - 2 + self.settings["margin"]["y"]) * self.zoom_factor,
                (position["x"] + self.settings["margin"]["x"]) * self.zoom_factor,
                (position["y"] + 2 + self.settings["margin"]["y"]) * self.zoom_factor,
            )
        self.focus_on_position()

    def focus_on_position(self):
        if self.settings["position focus"] and self.animation_frame.position:
            self.canvas.move(
                "all",
                (self.most_extreme_positions[0] - self.animation_frame.position[0])
                * self.zoom_factor,
                (self.most_extreme_positions[1] - self.animation_frame.position[1])
                * self.zoom_factor,
            )

    # Not implemented yet
    def create_corner_markers(self):
        self.canvas.create_line(
            self.settings["margin"]["x"] - 2,
            self.settings["margin"]["y"] + self.height,
            self.settings["margin"]["x"] + 2,
            self.settings["margin"]["y"] + self.height,
        )
        self.canvas.create_line(
            self.settings["margin"]["x"],
            self.settings["margin"]["y"] + self.height - 2,
            self.settings["margin"]["x"],
            self.settings["margin"]["y"] + self.height + 2,
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
