import socket
import threading
from multiprocessing import pool

from PIL import ImageGrab
import io
import time
import pyaudio
import concurrent.futures


class StreamingServer:

    def __init__(self):
        # Create a socket object
        self.server_socket = None

        # Bind the socket to a specific host and port
        self.host = socket.gethostname()
        self.port = 12345
        self.server_address = (self.host, self.port)

    def open_udp_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)

    def handle_data(self, s):
        """Function to handle the data from client connection and send it back"""
        while True:
            # Receive the data from the client
            length, client_address = s.recvfrom(65000)
            data, client_address = s.recvfrom(int(length.decode()))

            # Send back the screenshot
            self.server_socket.sendto(length, client_address)
            self.server_socket.sendto(data, client_address)

    def start(self):
        t = threading.Thread(target=self.handle_data, args=(self.server_socket,))
        t.start()


class AudioServer:

    def __init__(self):
        self.__chunk = 1024
        self.__format = pyaudio.paInt16
        self.__channels = 1
        self.__rate = 44100

        # Create a socket object
        self.server_socket = None

        # Bind the socket to a specific host and port
        self.host = socket.gethostname()
        self.port = 12345
        self.server_address = (self.host, self.port)

        # Open to udp server
        self.open_udp_server()

        # Create a thread pool with a limited number of workers
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    def open_udp_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)



    def handle_data(self):
        while True:
            # Receive a chunk of audio data from a client
            data, address = self.server_socket.recvfrom(4096)

            # Send the data back to Clients
            self.server_socket.sendto(data, address)

def main():
    s = StreamingServer()
    s.open_udp_server()
    s.start()


if __name__ == '__main__':
    main()
