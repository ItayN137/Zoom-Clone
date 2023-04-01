import customtkinter
from PIL import Image, ImageTk
import tkinter


class Zoom_Main_Window:

    def __init__(self):
        self.root = 0
        self.frame = 0
        self. label = 0
        self.entry1 = 0
        self.entry2 = 0
        self.create_button = 0
        self.join_button = 0
        self.handle_zoom_window()


    def handle_zoom_window(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.geometry("300x300")
        self.root.title("Itay's Zoom Application")

        self.app_image = tkinter.PhotoImage(file="zoom.png")
        self.root.iconphoto(False, self.app_image)

        self.label = customtkinter.CTkLabel(master=self.root, text="Itay's Zoom Application", font=("Arial", 25))
        self.label.pack(pady=12, padx=10)

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=12, padx=10)

        self.create_button = customtkinter.CTkButton(master=self.frame, text="Create New Meeting", command=self.handle_new_host_client)
        self.create_button.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Meeting ID")
        self.entry2.pack(pady=12, padx=10)

        self.join_button = customtkinter.CTkButton(master=self.frame, text="Join Meeting", command=self.handle_new_client)
        self.join_button.pack(pady=12, padx=10)


        self.root.mainloop()

    def handle_new_client(self):
        # self.entry1.get()

        self.root.destroy()
        pass

    def handle_new_host_client(self):
        # self.entry1.get()

        self.root.destroy()
        pass



def main():
    zoom1 = Zoom_Main_Window()

if __name__ == '__main__':
    main()
