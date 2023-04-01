import socket
import threading
from PIL import ImageGrab
import io
import time

class Server:

    def handle_data(self, s):
        """Function to handle the data from client connection and send it back"""
        while True:
            # Recieve the data from the client
            self.length, self.client_address = s.recvfrom(65000)
            self.data, self.client_address = s.recvfrom(int(self.length.decode()))

            # Send back the screenshot
            self.s.sendto(self.length, self.client_address)
            self.s.sendto(self.data, self.client_address)

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind(self.server)

        t = threading.Thread(target=self.handle_data, args=(self.s,))
        t.start()

        # Close the socket
        #self.s.close()

    def __init__(self):
        # Create a socket object
        self.s = 0

        # Bind the socket to a specific host and port
        self.host = socket.gethostname()
        self.port = 12345
        self.server = (self.host, self.port)



        # Start a new thread to send the data



def main():
    s = Server()
    s.start()


if __name__ == '__main__':
    main()