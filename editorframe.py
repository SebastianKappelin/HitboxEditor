import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from imageframe import ImageFrame
from enum import Enum

"""
Basically a canvas that can draw the characters current animation frame
and create new boxes/position
"""


class EditorFrame(ImageFrame):

    stipple = "gray50"
    alpha = 128

    def __init__(self, mainframe):
        ImageFrame.__init__(self, mainframe)

    def initialize(self):
        self.most_extreme_positions = {
            "x": 0,
            "y": 0,
        }  # Represents the highest x and y position values from all frames in the current action.
        # Used to center frames on position
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.settings = {
            "margin x": 0,
            "margin y": 0,
            "coordinates style": CoordinatesStyle.Top_left,
            "position focus": False,
        }
        self.update_scrollregion()

    def set_position(self, event):
        offset = self.get_offset()
        self.master.set_position(
            {
                "x": int(self.canvas.canvasx(event.x) / self.zoom_factor - offset["x"]),
                "y": int(self.canvas.canvasy(event.y) / self.zoom_factor - offset["y"]),
            }
        )

    def create_box(self, event):
        if self.crop_rectangle == None:
            return
        self.canvas.delete(self.crop_rectangle)
        box = {}
        offset = self.get_offset()
        if self.x0 < self.x1:
            box["x0"] = self.x0 - offset["x"]
            box["x1"] = self.x1 - offset["x"]
        else:
            box["x0"] = self.x1 - offset["x"]
            box["x1"] = self.x0 - offset["x"]
        if self.y0 < self.y1:
            box["y0"] = self.y0 - offset["y"]
            box["y1"] = self.y1 - offset["y"]
        else:
            box["y0"] = self.y1 - offset["y"]
            box["y1"] = self.y0 - offset["y"]
        self.master.create_box(box)

    def show_coordinates(self, event):
        offset = self.get_offset()
        if self.settings["coordinates style"] == CoordinatesStyle.Top_left:
            self.x_var.set(
                "x: {}".format(
                    int(self.canvas.canvasx(event.x) / self.zoom_factor - offset["x"])
                )
            )
            self.y_var.set(
                "y: {}".format(
                    int(self.canvas.canvasy(event.y) / self.zoom_factor - offset["y"])
                )
            )
        elif self.settings["coordinates style"] == CoordinatesStyle.Bottom_left:
            self.x_var.set(
                "x: {}".format(
                    int(self.canvas.canvasx(event.x) / self.zoom_factor - offset["x"])
                )
            )
            self.y_var.set(
                "y: {}".format(
                    int(
                        offset["y"]
                        + self.character.get_crop_height()
                        - self.canvas.canvasy(event.y) / self.zoom_factor
                    )
                )
            )
        elif self.settings["coordinates style"] == CoordinatesStyle.Position:
            pos = self.character.get_position()
            if not pos:
                self.x_var.set("no position")
                self.y_var.set("set")
            else:
                self.x_var.set(
                    "x: {}".format(
                        int(
                            self.canvas.canvasx(event.x) / self.zoom_factor
                            - pos["x"]
                            - offset["x"]
                        )
                    )
                )
                self.y_var.set(
                    "y: {}".format(
                        int(
                            offset["y"]
                            + pos["y"]
                            - self.canvas.canvasy(event.y) / self.zoom_factor
                        )
                    )
                )

    def show_image(self, event=None):
        if self.character == None or ImageFrame.image == None:
            return
        self.canvas.delete("all")
        imagetk = ImageTk.PhotoImage(
            ImageFrame.image.crop(self.character.get_crop_tuple()).resize(
                (
                    self.character.get_crop_width() * self.zoom_factor,
                    self.character.get_crop_height() * self.zoom_factor,
                )
            )
        )
        imageid = self.canvas.create_image(
            self.settings["margin x"] * self.zoom_factor,
            self.settings["margin y"] * self.zoom_factor,
            anchor="nw",
            image=imagetk,
        )
        self.canvas.lower(imageid)  # Setting image as background
        self.canvas.imagetk = imagetk  # Avoiding garbage collection
        self.draw_shapes()

    # Draws all boxes and position in animation_frame that's set to visible
    def draw_shapes(self):
        boxes = self.character.get_boxes()
        self.images = []
        for i in range(len(boxes)):
            image = Image.new(
                "RGBA",
                (
                    (boxes[i]["box"]["x1"] - boxes[i]["box"]["x0"]) * self.zoom_factor,
                    (boxes[i]["box"]["y1"] - boxes[i]["box"]["y0"]) * self.zoom_factor,
                ),
                (
                    boxes[i]["color"]["r"],
                    boxes[i]["color"]["g"],
                    boxes[i]["color"]["b"],
                    EditorFrame.alpha,
                ),
            )
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(
                (boxes[i]["box"]["x0"] + self.settings["margin x"]) * self.zoom_factor,
                (boxes[i]["box"]["y0"] + self.settings["margin y"]) * self.zoom_factor,
                image=self.images[i],
                anchor="nw",
            )
            self.canvas.create_rectangle(
                (boxes[i]["box"]["x0"] + self.settings["margin x"]) * self.zoom_factor,
                (boxes[i]["box"]["y0"] + self.settings["margin y"]) * self.zoom_factor,
                (boxes[i]["box"]["x1"] + self.settings["margin x"]) * self.zoom_factor,
                (boxes[i]["box"]["y1"] + self.settings["margin y"]) * self.zoom_factor,
                outline="#{:06x}".format(
                    (
                        (boxes[i]["color"]["r"] << 16)
                        + (boxes[i]["color"]["g"] << 8)
                        + (boxes[i]["color"]["b"])
                    )
                    & 0xFFFFFF
                ),
            )

        if self.character.frame_has_position() and self.character.is_position_visible():
            position = self.character.get_position_and_color()
            self.canvas.create_polygon(
                [
                    (position["position"]["x"] + self.settings["margin x"] - 5)
                    * self.zoom_factor,
                    (position["position"]["y"] + self.settings["margin y"])
                    * self.zoom_factor,
                    (position["position"]["x"] + self.settings["margin x"])
                    * self.zoom_factor,
                    (position["position"]["y"] + self.settings["margin y"] - 5)
                    * self.zoom_factor,
                    (position["position"]["x"] + self.settings["margin x"] + 5)
                    * self.zoom_factor,
                    (position["position"]["y"] + self.settings["margin y"])
                    * self.zoom_factor,
                    (position["position"]["x"] + self.settings["margin x"])
                    * self.zoom_factor,
                    (position["position"]["y"] + self.settings["margin y"] + 5)
                    * self.zoom_factor,
                ],
                fill="#{:06x}".format(
                    (
                        (position["color"]["r"] << 16)
                        + (position["color"]["g"] << 8)
                        + (position["color"]["b"])
                    )
                    & 0xFFFFFF
                ),
                stipple=EditorFrame.stipple,
            )
            self.canvas.create_line(
                (position["position"]["x"] - 2 + self.settings["margin x"])
                * self.zoom_factor,
                (position["position"]["y"] + self.settings["margin y"])
                * self.zoom_factor,
                (position["position"]["x"] + 2 + self.settings["margin x"])
                * self.zoom_factor,
                (position["position"]["y"] + self.settings["margin y"])
                * self.zoom_factor,
            )
            self.canvas.create_line(
                (position["position"]["x"] + self.settings["margin x"])
                * self.zoom_factor,
                (position["position"]["y"] - 2 + self.settings["margin y"])
                * self.zoom_factor,
                (position["position"]["x"] + self.settings["margin x"])
                * self.zoom_factor,
                (position["position"]["y"] + 2 + self.settings["margin y"])
                * self.zoom_factor,
            )
            if self.settings["position focus"]:
                self.canvas.move(
                    "all",
                    (self.most_extreme_positions["x"] - position["position"]["x"])
                    * self.zoom_factor,
                    (self.most_extreme_positions["y"] - position["position"]["y"])
                    * self.zoom_factor,
                )

    # Gets the distance from the drawn picture and the upper left corner.
    def get_offset(self):
        if self.settings["position focus"] and self.character.frame_has_position():
            return {
                "x": self.most_extreme_positions["x"]
                - self.character.frame_position_x()
                + self.settings["margin x"],
                "y": self.most_extreme_positions["y"]
                - self.character.frame_position_y()
                + self.settings["margin y"],
            }
        else:
            return {
                "x": self.settings["margin x"],
                "y": self.settings["margin y"],
            }

    def update_most_extreme_positions(self):
        self.most_extreme_positions = self.character.find_most_extreme_positions()
        self.show_image()

    # Not implemented yet/never
    def create_corner_markers(self):
        self.canvas.create_line(
            self.settings["margin x"] - 2,
            self.settings["margin y"] + self.height,
            self.settings["margin x"] + 2,
            self.settings["margin y"] + self.height,
        )
        self.canvas.create_line(
            self.settings["margin x"],
            self.settings["margin y"] + self.height - 2,
            self.settings["margin x"],
            self.settings["margin y"] + self.height + 2,
        )

    # Used to get correct size on scrollbars
    def set_image_dimensions(self, dimensions):
        self.image_size = dimensions
        self.update_scrollregion()
        self.show_image()

    def update_scrollregion(self):
        self.canvas.config(
            scrollregion=(
                0,
                0,
                (self.image_size[0] + self.settings["margin x"] * 2) * self.zoom_factor,
                (self.image_size[1] + self.settings["margin y"] * 2) * self.zoom_factor,
            )
        )

    def get_settings(self):
        return self.settings

    def set_character(self, character):
        self.character = character
        self.show_image()

    def position_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.set_position)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def box_mode(self):
        self.canvas.bind("<ButtonPress-1>", self.crop_from)
        self.canvas.bind("<B1-Motion>", self.crop_to)
        self.canvas.bind("<ButtonRelease-1>", self.create_box)


# For showing coordinates differently.
# Top_left x-positive = right, y-positive = down
# Bottom_left x-positive = right, y-positive = up(same as pyglet)
# Position x-positive = right, y-positive = up
class CoordinatesStyle(Enum):
    Top_left = 1
    Bottom_left = 2
    Position = 3