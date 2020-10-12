import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


"""
Superclass for EditorFrame and CropImageFrame
"""


class ImageFrame(tk.Frame):
    image = None

    def __init__(self, mainframe):
        tk.Frame.__init__(self, master=mainframe)

        self.canvas = tk.Canvas(self)

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.crop_rectangle = None
        self.x_var = StringVar()
        self.y_var = StringVar()

        self.zoom_factor = 1
        # image_size = (width, height)
        if ImageFrame.image:
            self.image_size = ImageFrame.image.size
        else:
            self.image_size = (0, 0)

        hbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.canvas.xview)
        vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.bind("<Configure>", self.show_image)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<ButtonPress-1>", self.crop_from)
        self.canvas.bind("<B1-Motion>", self.crop_to)

        self.initialize()
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def initialize(self):
        pass

    def zoom_in(self):
        # self.zoom_factor = int(self.zoom_factor * 2)
        self.zoom_factor += 1
        self.update_scrollregion()
        self.show_image()

    def zoom_out(self):
        if self.zoom_factor == 1:
            return
        # self.zoom_factor = int(self.zoom_factor / 2)
        self.zoom_factor -= 1
        self.update_scrollregion()
        self.show_image()

    def motion(self, event):
        self.show_coordinates(event)

    def crop_from(self, event):
        self.x0 = int(self.canvas.canvasx(event.x) / self.zoom_factor)
        self.y0 = int(self.canvas.canvasy(event.y) / self.zoom_factor)

    def crop_to(self, event):
        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)
        self.x1 = int(self.canvas.canvasx(event.x) / self.zoom_factor)
        self.y1 = int(self.canvas.canvasy(event.y) / self.zoom_factor)
        self.crop_rectangle = self.canvas.create_rectangle(
            self.x0 * self.zoom_factor,
            self.y0 * self.zoom_factor,
            self.x1 * self.zoom_factor,
            self.y1 * self.zoom_factor,
        )
        self.show_coordinates(event)

    def show_image(self, event=None):
        pass

    def update_scrollregion(self):
        self.canvas.config(
            scrollregion=(
                0,
                0,
                self.image_size[0] * self.zoom_factor,
                self.image_size[1] * self.zoom_factor,
            )
        )

    def get_settings(self):
        return self.settings

    # def set_margin(self, margin):
    #     self.margin = margin
    #     self.update_canvas()
    #     self.show_image()

    def show_coordinates(self, event):
        self.x_var.set(
            "x: {}".format(int(self.canvas.canvasx(event.x) / self.zoom_factor))
        )
        self.y_var.set(
            "y: {}".format(int(self.canvas.canvasy(event.y) / self.zoom_factor))
        )
