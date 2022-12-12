import tkinter
import tkinter.messagebox
import customtkinter
import board
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from picamera import PiCamera

from time import sleep
import pygame
import os

kit1 = MotorKit()
kit2 = MotorKit(address=0x61)

kit1.motor1.throttle = 0
kit2.motor1.throttle = 0

# Setting up theme
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Cool Blue")
        self.geometry(f"{1200}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.bind("<KeyPress>", self.key_pressed)
        self.bind("<KeyRelease>", self.key_released)

        # create sidebar frame for controls
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Controls",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.button_up = customtkinter.CTkButton(self.sidebar_frame, text="W", height=10, width=10)
        self.button_up.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_up.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'W'))
        self.button_up.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'W'))

        self.button_down = customtkinter.CTkButton(self.sidebar_frame, text="S", height=10, width=10)
        self.button_down.grid(row=3, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_down.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'S'))
        self.button_down.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'S'))

        self.button_left = customtkinter.CTkButton(self.sidebar_frame, text="A", height=10, width=10)
        self.button_left.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_left.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'A'))
        self.button_left.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'A'))

        self.button_right = customtkinter.CTkButton(self.sidebar_frame, text="D", height=10, width=10)
        self.button_right.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_right.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'D'))
        self.button_right.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x,'D'))

        self.button_stop = customtkinter.CTkButton(self.sidebar_frame, text="Stop", height=10, width=10)
        self.button_stop.grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # create Video Canvas
        self.picam = customtkinter.CTkCanvas(self, width=800, background="gray")
        self.picam.grid(row=0, column=1, rowspan=2, padx=(5, 5), pady=(20, 20), sticky="nsew")
        self.picam_label = customtkinter.CTkLabel(master=self.picam, text="Live Video", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.picam_label.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        # create sidebar frame for Environmental Variable
        self.measurements = customtkinter.CTkFrame(self, width=200)
        self.measurements.grid(row=0, column=3, rowspan=4, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.measurements.grid_rowconfigure(4, weight=1)
        self.label_measurements = customtkinter.CTkLabel(master=self.measurements, text="Environment:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_measurements.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

    def key_pressed(self, event):
        if event.char in 'wads':
            self.motion_event_start(event, event.char.upper())

    def key_released(self, event):
        if event.char in 'wads':
            self.motion_event_stop(event, event.char.upper())

    def motion_event_start(self, event, button):
        if button == "W":
            kit1.motor1.throttle = 1
            kit2.motor1.throttle = 1
            print("yes it is")

        print(f"{button} Pressed")

    def motion_event_stop(self, event, button):
        if button == "W":
            kit1.motor1.throttle = 0
            kit2.motor1.throttle = 0


        print(f"{button} Released")


if __name__ == "__main__":
    app = App()
    app.mainloop()