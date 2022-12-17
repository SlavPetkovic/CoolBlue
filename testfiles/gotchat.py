import cv2
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter

# Setting up theme of GUI
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Create a canvas to display the webcam feed
        self.canvas = customtkinter.CTkCanvas(self, width=640, height=480)
        self.canvas.pack()
        # Start the webcam feed update loop
        self.capture = cv2.VideoCapture(0)
        self.update_frame()


    def update_frame(self):
        # Open the webcam

        # Get the current frame from the webcam
        _, frame = self.capture.read()
        # Convert the frame to a PhotoImage object
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        # Update the canvas with the new frame
        self.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        self.canvas.image = frame
        # Schedule the next update
        self.canvas.after(30, self.update_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
