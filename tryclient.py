import socket
import threading
import tkinter
import tkinter as tk
from io import BytesIO
from PIL import ImageGrab, Image, ImageTk
import io
import time
import customtkinter
from pynput.mouse import Controller


class Client:

    def connect_udp_socket(self):
        # Open a socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to the server
        # self.socket.bind(self.server_address)

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
            # Take a screenshot using ImageGrab
            screenshot = ImageGrab.grab()
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
        # Receive the screenshot from the server
        while True:
            length, server_address = self.server_socket.recvfrom(65000)
            screenshot_bytes, server_address = self.server_socket.recvfrom(int(length.decode()))
            # Create a PhotoImage object from the received data
            screenshot = Image.open(BytesIO(screenshot_bytes))
            img = ImageTk.PhotoImage(screenshot)
            # Update the label with the new screenshot
            if not previous_img == img:
                self.label.configure(image=img)
                self.label.update()
            previous_img = img


    def start(self):
        # Create a Tkinter window to display the screenshot
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Itay's Zoom Application")

        # App photo
        self.app_image = tkinter.PhotoImage(file="zoom.png")
        self.root.iconphoto(False, self.app_image)

        # Open a label
        default_img = Image.open("black_screen.png")
        self.label = tk.Label(self.root, image=ImageTk.PhotoImage(default_img))
        self.label.pack()
        self.label.update()

        # Connect to udp server
        self.connect_udp_socket()

        # Send screenshots to the server
        t1 = threading.Thread(target=self.send_screenshot)
        t1.start()

        time.sleep(1 / 3)

        t2 = threading.Thread(target=self.receive_screenshot)
        t2.start()

        self.root.mainloop()

        # Close the socket
        # self.socket.close()

    def __init__(self):
        self.STREAM_ON = True
        self.root = None
        self.app_image = None
        self.label = None
        self.server_socket = None

        self.host = socket.gethostname()
        self.port = 12345
        self.server_address = (self.host, self.port)



def main():
    c = Client()
    c.start()


if __name__ == '__main__':
    main()
