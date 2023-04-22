import customtkinter
import tkinter
from PIL import Image, ImageTk
import multiprocessing
import socket
import sys
import threading
import time

import tryclient
from tryclient import *


class ZoomClient:

    def __init__(self, username, kick_adminstartion):
        self._USERNAME = username
        self._IS_MUTED = True
        self._IS_CAMERA = False
        self._IS_SCREEN_SHARING = False
        self._CHAT_OPEN = False
        self._PARTICIPANTS_OPEN = False
        self._SETTINGS = False
        self._KICK = kick_adminstartion
        self._WIDTH = 1280
        self._HEIGHT = 920
        self.root = 0
        self.lower_frame = 0
        self.upper_frame = 0
        self.label = 0
        self.app_image = 0
        self.microphone_button = 0
        self.camera_button = 0
        self.share_screen_button = 0
        self.chat_button = 0
        self.participants_button = 0
        self.settings_button = 0
        self.muted_mic_image = customtkinter.CTkImage(light_image=Image.open("mute_microphone.png"),
                                                      dark_image=Image.open("mute_microphone.png"),
                                                      size=(20, 20))

        self.unmuted_mic_image = customtkinter.CTkImage(light_image=Image.open("microphone.png"),
                                                        dark_image=Image.open("microphone.png"),
                                                        size=(20, 20))

        self.camera_on = customtkinter.CTkImage(light_image=Image.open("video_camera.png"),
                                                dark_image=Image.open("video_camera.png"),
                                                size=(20, 20))

        self.camera_off = customtkinter.CTkImage(light_image=Image.open("no_video_camera.png"),
                                                 dark_image=Image.open("no_video_camera.png"),
                                                 size=(20, 20))

        self.share_screen_on_photo = customtkinter.CTkImage(light_image=Image.open("screen_share_on.png"),
                                                            dark_image=Image.open("screen_share_on.png"),
                                                            size=(20, 20))

        self.share_screen_off_photo = customtkinter.CTkImage(light_image=Image.open("screen_share_off.png"),
                                                             dark_image=Image.open("screen_share_off.png"),
                                                             size=(20, 20))

        self.chat_photo = customtkinter.CTkImage(light_image=Image.open("chat.png"),
                                                 dark_image=Image.open("chat.png"),
                                                 size=(20, 20))

        self.participants_photo = customtkinter.CTkImage(light_image=Image.open("group.png"),
                                                         dark_image=Image.open("group.png"),
                                                         size=(20, 20))
        self.settings_photo = customtkinter.CTkImage(light_image=Image.open("settings.png"),
                                                     dark_image=Image.open("settings.png"),
                                                     size=(20, 20))
        self.audio_client = tryclient.MicrophoneAudioClient()
        self.audio_client.start()

        self.handle_new_client()

    def handle_new_client(self):
        self.root = customtkinter.CTk()
        self.root.geometry(f"{self._WIDTH}x{self._HEIGHT}")
        self.root.title("Itay's Zoom Application")

        self.app_image = tkinter.PhotoImage(file="zoom.png")
        self.root.iconphoto(False, self.app_image)

        self.label = customtkinter.CTkLabel(master=self.root, text="Itay's Zoom Application",
                                            font=("Arial", 25))
        self.label.pack(pady=6, padx=5)

        self.upper_frame = customtkinter.CTkFrame(master=self.root, width=400, height=50)
        self.upper_frame.pack(ipadx=400, ipady=220, side="top")

        self.lower_frame = customtkinter.CTkFrame(master=self.root, width=400, height=50)
        self.lower_frame.pack(ipadx=400, ipady=4, side="bottom")

        self.microphone_button = customtkinter.CTkButton(master=self.lower_frame, image=self.muted_mic_image,
                                                         text="Unmute",
                                                         font=("Ariel", 15, "bold"), width=10, height=10,
                                                         command=self.handle_mic)
        self.microphone_button.pack(pady=10, padx=10, side="left", anchor=tkinter.CENTER)

        self.camera_button = customtkinter.CTkButton(master=self.lower_frame, image=self.camera_off,
                                                     text="Turn On",
                                                     font=("Ariel", 15, "bold"), width=10, height=10,
                                                     command=self.handle_camera)
        self.camera_button.pack(pady=10, padx=10, side="left", anchor=tkinter.CENTER)

        self.share_screen_button = customtkinter.CTkButton(master=self.lower_frame, image=self.share_screen_off_photo,
                                                           text="Share Screen",
                                                           font=("Ariel", 15, "bold"), width=10, height=10,
                                                           command=self.handle_share_screen)
        self.share_screen_button.pack(pady=10, padx=10, side="left", anchor=tkinter.CENTER)

        self.chat_button = customtkinter.CTkButton(master=self.lower_frame, image=self.chat_photo,
                                                   text="Chat",
                                                   font=("Ariel", 15, "bold"), width=10, height=10,
                                                   command=self.handle_chat())
        self.chat_button.pack(pady=10, padx=10, side="right", anchor=tkinter.CENTER)

        self.participants_button = customtkinter.CTkButton(master=self.lower_frame, image=self.participants_photo,
                                                           text="Participants",
                                                           font=("Ariel", 15, "bold"), width=10, height=10,
                                                           command=self.handle_participants())
        self.participants_button.pack(pady=10, padx=10, side="right", anchor=tkinter.CENTER)

        self.settings_button = customtkinter.CTkButton(master=self.lower_frame, image=self.settings_photo,
                                                       text="",
                                                       font=("Ariel", 15, "bold"), width=10, height=10,
                                                       command=self.handle_settings())
        self.settings_button.pack(pady=10, padx=10, side="right", anchor=tkinter.CENTER)

        self.root.mainloop()

    def handle_mic(self):
        """
        handle the press of the button. changes the button to mute or un-mute text and image and also provides
        the audio share between clients
        :return:
        """
        if self._IS_MUTED:
            self._IS_MUTED = False
            self.microphone_button.configure(image=self.unmuted_mic_image, text="Mute",
                                             font=("Ariel", 15, "bold"), width=10, height=10)
            self.audio_client.start_mic()

        else:
            self._IS_MUTED = True
            self.microphone_button.configure(image=self.muted_mic_image,
                                             text="Unmute",
                                             font=("Ariel", 15, "bold"), width=10, height=10)
            self.audio_client.stop_mic()
        return

    def handle_camera(self):
        """
        handle the press of the button. changes the button to camera on or off with text and image and also provides
        the camera share between clients
        :return:
        """
        if not self._IS_CAMERA:
            self._IS_CAMERA = True
            self.camera_button.configure(image=self.camera_on,
                                         text="Turn Off",
                                         font=("Ariel", 15, "bold"), width=10, height=10)
            # open the connection
        else:
            self._IS_CAMERA = False
            self.camera_button.configure(image=self.camera_off,
                                         text="Turn On",
                                         font=("Ariel", 15, "bold"), width=10, height=10)
            # close the connection
        return

    def handle_share_screen(self):
        """
        handle the press of the button. changes the button to share screen on or off with text and image and also
        provides the screen share between clients
        :return:
        """
        if not self._IS_SCREEN_SHARING:
            self._IS_SCREEN_SHARING = True
            self.share_screen_button.configure(image=self.share_screen_on_photo,
                                               text="Stop Sharing",
                                               font=("Ariel", 15, "bold"), width=10, height=10)
            # open the connection
        else:
            self._IS_SCREEN_SHARING = False
            self.share_screen_button.configure(image=self.share_screen_off_photo,
                                               text="Share Screen",
                                               font=("Ariel", 15, "bold"), width=10, height=10)
            # close the connection
        return

    def handle_chat(self):
        """
        handle the press of the button. opening and closing the chat window
        :return:
        """
        if not self._CHAT_OPEN:
            self._CHAT_OPEN = True
            # open the chat window
        else:
            self._CHAT_OPEN = False
            # close the chat window
        return

    def handle_participants(self):
        """
        handle the press of the button. opening and closing the participants window
        :return:
        """
        if not self._PARTICIPANTS_OPEN:
            self._PARTICIPANTS_OPEN = True
            # open the participants window
        else:
            self._PARTICIPANTS_OPEN = False
            # close the participants window
        return

    def handle_settings(self):
        """
        handle the press of the button. opening and closing the settings window
        :return:
        """
        if not self._SETTINGS:
            self._SETTINGS = True
            # open the settings window
        else:
            self._SETTINGS = False
            # close the settings window
        return


def main():
    zoom_client = ZoomClient("Itay", False)


if __name__ == '__main__':
    main()
