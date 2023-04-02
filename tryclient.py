import socket
import threading
import tkinter
import tkinter as tk
from io import BytesIO

import cv2
from PIL import ImageGrab, Image, ImageTk
import io
import time
import customtkinter
from pynput.mouse import Controller
from Window import Window
from abc import ABC, abstractmethod
import vidstream


class Client(ABC):

    def __init__(self):
        self.STREAM_ON = True
        self.root = None
        self.app_image = None
        self.label = None
        self.server_socket = None
        self.window = None
        self.func = None

        self.host = socket.gethostname()
        self.port = 12345
        self.server_address = (self.host, self.port)

    def connect_udp_socket(self):
        # Open a socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, data):
        """Gets encoded data to send"""
        self.server_socket.sendto(data, self.server_address)

    def send_screenshot(self):
        """Function to send the screenshot"""

        previous_screenshot = None
        bio = io.BytesIO()
        image_quality = 10
        cursor = Image.open("cursor.png").resize((28, 28))
        my_cursor = Controller()

        while True:
            # Take a screenshot of the monitor or the camera
            screenshot = self.get_frame()
            if previous_screenshot == screenshot:
                continue

            # Drawing a mouse on the screen
            screenshot = screenshot.convert("RGBA")
            screenshot.alpha_composite(cursor, dest=my_cursor.position)
            screenshot = screenshot.convert("RGB")

            # Resizing the photo
            screenshot = screenshot.resize((1280, 720))

            # Saving the photo to the digital storage
            screenshot.save(bio, "JPEG", quality=image_quality)
            bio.seek(0)

            # Getting the bytes of the photo
            screenshot = bio.getvalue()

            # Restarting the storage
            bio.truncate(0)

            length = len(screenshot)
            if length < 65000:
                # Sending the screenshot
                self.send_message(str(len(screenshot)).zfill(10).encode())
                self.send_message(screenshot)
                if image_quality < 90 and length < 65000:
                    image_quality += 5
            else:
                image_quality -= 10
            previous_screenshot = screenshot

    def receive_screenshot(self):
        """Function to receive and display the screenshot"""
        previous_img = None

        while True:
            # Receive the screenshot from the server
            length, server_address = self.server_socket.recvfrom(65000)
            screenshot_bytes, server_address = self.server_socket.recvfrom(int(length.decode()))

            # Create a PhotoImage object from the received data
            screenshot = Image.open(BytesIO(screenshot_bytes))
            img = ImageTk.PhotoImage(screenshot)

            # Update the label with the new screenshot
            if not previous_img == img:
                self.window.update_label(self.label, img)
            previous_img = img

    def start(self):

        # Create a window object
        self.window = Window()

        # Create a Tkinter window to display the screenshot
        self.root = self.window.create_tk_window()

        # Open a label from the window object
        self.label = self.window.create_label()

        # Connect to udp server
        self.connect_udp_socket()

        # Send screenshots to the server
        t1 = threading.Thread(target=self.send_screenshot)
        t1.start()

        time.sleep(1 / 3)

        t2 = threading.Thread(target=self.receive_screenshot)
        t2.start()

        self.window.mainloop()

        # Close the socket
        # self.socket.close()

    def get_frame(self):
        pass


class ScreenShareClient(Client):

    def __init__(self):
        super(ScreenShareClient, self).__init__()

    def get_frame(self):
        return ImageGrab.grab()

class CameraClient(Client):

    def __init__(self, x_res=1280, y_res=720):
        super(CameraClient, self).__init__()
        self.x_res = x_res
        self.y_res = y_res
        self.camera = cv2.VideoCapture(0)

    def configure(self):
        self.camera.set(3, self.x_res)
        self.camera.set(4, self.y_res)

    def get_frame(self):
        ret, frame = self.camera.read()
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return frame





def main():
    c = ScreenShareClient()
    c.start()


if __name__ == '__main__':
    main()
