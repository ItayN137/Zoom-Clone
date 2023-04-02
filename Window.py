import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, JpegImagePlugin


class Window:

    def __init__(self, width=1280, height=720):
        self.root = None
        self.width = width
        self.height = height
        self.title = "Itay's Zoom Application"

    def create_tk_window(self):
        """Creates tkinter window"""
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title(self.title)

        # Application logo
        app_image = tk.PhotoImage(file="zoom.png")
        self.root.iconphoto(False, app_image)
        return self.root

    def create_label(self, img="black_screen.png", text="", font="", x=0, y=0):
        """creates label to display image using tk"""
        if type(img) == str:
            img = Image.open(img)
        label = tk.Label(self.root, image=ImageTk.PhotoImage(img), text=text, font=font)
        label.pack(padx=x, pady=y)
        label.update()
        return label

    def update_label(self, label, img):
        """updating label with given image"""
        if type(img) == JpegImagePlugin.JpegImageFile:
            img = ImageTk.PhotoImage(img)

        label.configure(image=img)
        label.update()
        return

    def mainloop(self):
        self.root.mainloop()



