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

    def open_udp_socket(self):
        # Open a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to the server
        # self.socket.bind(self.server_address)

    def send_message(self, data):
        """Gets encoded data to send"""
        self.socket.sendto(data, self.server_address)

    def send_screenshot(self):
        """Function to send the screenshot"""
        # Take a screenshot using ImageGrab and send it to the server
        bio = io.BytesIO()
        image_quality = 10
        cursor = Image.open("cursor.png").resize((30, 25))
        my_cursor = Controller()
        while True:
            screenshot = ImageGrab.grab()
            screenshot = screenshot.convert("RGBA")
            screenshot.alpha_composite(cursor, dest=my_cursor.position)
            screenshot = screenshot.convert("RGB")
            screenshot.thumbnail((1280, 720))
            screenshot.save(bio, "JPEG", quality=image_quality)
            bio.seek(0)
            screenshot = bio.getvalue()
            length = len(screenshot)
            if length < 65000:
                # send the screenshot
                self.send_message(str(len(screenshot)).zfill(10).encode())
                self.send_message(screenshot)
                if image_quality < 90 and length < 50000:
                    image_quality += 10
            else:
                image_quality -= 10
            bio.truncate(0)

    def receive_screenshot(self):
        """Function to receive and display the screenshot"""
        # Receive the screenshot from the server
        while True:
            length, server_address = self.socket.recvfrom(65000)
            screenshot_bytes, server_address = self.socket.recvfrom(int(length.decode()))
            # Create a PhotoImage object from the received data
            screenshot = Image.open(BytesIO(screenshot_bytes))
            screenshot = customtkinter.CTkImage(light_image=screenshot,
                                                dark_image=screenshot,
                                                size=(1280, 720))
            # Update the label with the new screenshot
            self.label.configure(image=screenshot)
            #self.label.update()

    def start(self):
        # Create a Tkinter window to display the screenshot
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Itay's Zoom Application")

        self.app_image = tkinter.PhotoImage(file="zoom.png")
        self.root.iconphoto(False, self.app_image)

        # Send screenshots to the server
        t1 = threading.Thread(target=self.send_screenshot)
        t1.start()

        time.sleep(1 / 3)

        self.label = customtkinter.CTkLabel(master=self.root, text=" ")
        self.label.pack()

        t2 = threading.Thread(target=self.receive_screenshot)
        t2.start()

        self.root.mainloop()

        # Close the socket
        # self.socket.close()

    def __init__(self):
        self.STREAM_ON = True
        # Host And Port
        self.host = socket.gethostname()
        self.port = 12345
        self.server_address = (self.host, self.port)
        # Create a socket object
        self.open_udp_socket()
        # self.socket.setblocking(False)
        self.root = None
        self.app_image = None
        self.label = None


def main():
    c = Client()
    c.start()


if __name__ == '__main__':
    main()
