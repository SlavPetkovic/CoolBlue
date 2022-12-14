import tkinter
import tkinter.messagebox
import customtkinter
import board
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
import time
from busio import I2C
import adafruit_bme680
import datetime
import adafruit_veml7700


# Setting up Motors
kit1 = MotorKit()
kit2 = MotorKit(address=0x61)
kit1.motor1.throttle = 0
kit2.motor1.throttle = 0

# Setting up relays to control LED and main lights
rc1 = 23
rc2 = 24
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(rc1, GPIO.OUT)
GPIO.setup(rc2, GPIO.OUT)
GPIO.output(rc1, True)
GPIO.output(rc2, True)


# Sensors
i2c = board.I2C()  # uses board.SCL and board.SDA
veml7700 = adafruit_veml7700.VEML7700(i2c)
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Setting up theme of GUI
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.is_on = True
        self.temperature = tkinter.IntVar()
        self.pressure = tkinter.IntVar()
        self.humidity = tkinter.IntVar()
        self.luminosity = tkinter.IntVar()

        #self.temperature.set(f'{50}\N{DEGREE CELSIUS}')

        self.title("Cool Blue")
        self.geometry(f"{1200}x{560}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.bind("<KeyPress>", self.key_pressed)
        self.bind("<KeyRelease>", self.key_released)


        ###################################################################
        # create sidebar frame for controls
        ###################################################################
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100)
        self.sidebar_frame.grid(row=0, column=0, rowspan=1, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Setting up grid label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Motion",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(10, 10))

        # Setting up W - Forward button
        self.button_up = customtkinter.CTkButton(self.sidebar_frame, text="W", height=10, width=10)
        self.button_up.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_up.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'W'))
        self.button_up.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'W'))

        # Setting up S - Backwards buttons
        self.button_down = customtkinter.CTkButton(self.sidebar_frame, text="S", height=10, width=10)
        self.button_down.grid(row=3, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_down.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'S'))
        self.button_down.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'S'))

        # Setting up A - Left button
        self.button_left = customtkinter.CTkButton(self.sidebar_frame, text="A", height=10, width=10)
        self.button_left.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_left.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'A'))
        self.button_left.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x, 'A'))

        # Setting up D - Right button
        self.button_right = customtkinter.CTkButton(self.sidebar_frame, text="D", height=10, width=10)
        self.button_right.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_right.bind('<ButtonPress-1>', lambda x: self.motion_event_start(x, 'D'))
        self.button_right.bind('<ButtonRelease-1>', lambda x: self.motion_event_stop(x,'D'))


        ###################################################################
        # Create Sidebar for arm control
        ###################################################################
        self.arm_control = customtkinter.CTkFrame(self)
        self.arm_control.grid(row=1, column=0, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.arm_control.grid_rowconfigure(2, weight=1)

        # Setting up grid label
        self.arm_label = customtkinter.CTkLabel(self.arm_control, text="Arm",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.arm_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.grip_label = customtkinter.CTkLabel(self.arm_control, text="Grip",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.grip_label.grid(row=0, column=1, padx=20, pady=(10, 10))

        # Arm Up
        self.button_arm_up = customtkinter.CTkButton(self.arm_control, text="    Up   ", height=10, width=10)
        self.button_arm_up.grid(row=1, column=0, padx=10, pady=10, ipadx=30, ipady=10)
        # Arm Down
        self.button_arm_down = customtkinter.CTkButton(self.arm_control, text=" Down", height=10, width=10)
        self.button_arm_down.grid(row=2, column=0, padx=10, pady=10, ipadx=30, ipady=10)
        # Grip Open
        self.button_grip_open = customtkinter.CTkButton(self.arm_control, text="Open", height=10, width=10)
        self.button_grip_open.grid(row=1, column=1, padx=10, pady=10, ipadx=30, ipady=10, sticky="w")
        # Grip Closed
        self.button_grip_close = customtkinter.CTkButton(self.arm_control, text="Close", height=10, width=10)
        self.button_grip_close.grid(row=2, column=1, padx=10, pady=10, ipadx=30, ipady=10, sticky="w")


        ###################################################################
        # Create Sidebar for LED, LIghts and Camera controls
        ###################################################################
        self.lights_control = customtkinter.CTkFrame(self)
        self.lights_control.grid(row=3, column=0, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.lights_control.grid_rowconfigure(1, weight=1)

        # LED  Lights
        self.led_switch = customtkinter.CTkSwitch(master=self.lights_control, text="LED", command=self.led_switch)
        self.led_switch.grid(row=0, column=1, pady=10, padx=20, sticky="n")

        # Regular Lights
        self.lights_switch = customtkinter.CTkSwitch(master=self.lights_control, text="Lights", command=self.lights_switch)
        self.lights_switch.grid(row=1, column=1, pady=10, padx=20)

        # Camera
        self.camera_switch = customtkinter.CTkSwitch(master=self.lights_control, text="Camera", command=self.camera_switch)
        self.camera_switch.grid(row=2, column=1, pady=10, padx=20, )


        ###################################################################
        # Create canvas for RPCam live stream
        ###################################################################
        self.picam = customtkinter.CTkCanvas(self, width=800, background="gray")
        self.picam.grid(row=0, column=1, rowspan=4, padx=(5, 5), pady=(20, 20), sticky="nsew")
        self.picam.grid_rowconfigure(4, weight=1)

        # picam label
        self.picam_label = customtkinter.CTkLabel(master=self.picam, text="Live Stream", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.picam_label.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")


        ###################################################################
        # Create sidebar grid for Temperature, Pressure, Humidity and Luminosity
        ###################################################################
        # create frame for environmental variable
        self.temperature_frame = customtkinter.CTkFrame(self)
        self.temperature_frame.grid(row=0, column=3, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="n")
        self.temperature_frame.grid_rowconfigure(2, weight=1)

        self.label_temperature = customtkinter.CTkLabel(master=self.temperature_frame, text=f'Temperature (\N{DEGREE CELSIUS})')
        self.label_temperature.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="")
        self.label_temperature_value = customtkinter.CTkLabel(master=self.temperature_frame, textvariable=self.temperature, font=customtkinter.CTkFont(size=50, weight="bold"))
        self.label_temperature_value.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="e")

        # create checkbox and switch frame
        self.pressure_frame = customtkinter.CTkFrame(self)
        self.pressure_frame.grid(row=1, column=3, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="n")
        self.pressure_frame.grid_rowconfigure(1, weight=1)

        self.label_pressure = customtkinter.CTkLabel(master=self.pressure_frame, text="Pressure (in Hg)")
        self.label_pressure.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.label_pressure_value = customtkinter.CTkLabel(master=self.pressure_frame, textvariable=self.pressure, font=customtkinter.CTkFont(size=50, weight="bold"))
        self.label_pressure_value.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="e")


        # create checkbox and switch frame
        self.humidity_frame = customtkinter.CTkFrame(self)
        self.humidity_frame.grid(row=3, column=3, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="")
        self.humidity_frame.grid_rowconfigure(1, weight=1)

        self.label_humidity = customtkinter.CTkLabel(master=self.humidity_frame, text="Humidity (%)")
        self.label_humidity.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.label_humidity_value = customtkinter.CTkLabel(master=self.humidity_frame, textvariable=self.humidity, font=customtkinter.CTkFont(size=50, weight="bold"))
        self.label_humidity_value.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="e")

        # # create checkbox and switch frame
        # self.luminosity = customtkinter.CTkFrame(self)
        # self.luminosity.grid(row=4, column=3, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="")
        # self.luminosity.grid_rowconfigure(1, weight=1)
        # self.label_luminosity = customtkinter.CTkLabel(master=self.luminosity, text="Luminosity")
        # self.label_luminosity.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        self.temp()  # call the temp function just once

    def temp(self):
        current_temp, current_pres, current_hum = self.current()
        self.temperature.set(current_temp)
        self.pressure.set(current_pres)
        self.humidity.set(current_hum)

        self.after(2000, self.temp)  # 2000 milliseconds = 2 seconds

    def current(self):
        while True:
            current_temp = round(bme680.temperature, 2)
            current_pres = round(bme680.pressure * 0.030, 2)
            current_hum =  round(bme680.humidity, 2)
            print(f'{current_temp}')
            return current_temp, current_pres, current_hum


    def key_pressed(self, event):
        if event.char in 'wads':
            self.motion_event_start(event, event.char.upper())
        elif event.keysym == 'Left':
            self.move_left_arm_function()
        elif event.keysym == 'Right':
            self.move_right_arm_function()
        elif event.keysym == 'Up':
            self.move_left_arm_function()
        elif event.keysym == 'Down':
            self.move_right_arm_function()

    def key_released(self, event):
        if event.char in 'wads':
            self.motion_event_stop(event, event.char.upper())

    def motion_event_start(self, event, button):
        if button == "W":
            kit1.motor1.throttle = 1
            kit2.motor1.throttle = 1
            print(f"{button} Pressed")
        elif button == "S":
            kit1.motor1.throttle = -1
            kit2.motor1.throttle = -1

            print(f"{button} Pressed")

    def motion_event_stop(self, event, button):
        print(f"{button} Released")
        kit1.motor1.throttle = 0
        kit2.motor1.throttle = 0

    #########################################################################
    # LED Switch
    #########################################################################

    def led_switch(self, event=None):
        if self.is_on:
            print("LED on")
            GPIO.output(rc1, False)
            self.is_on = False
        else:
            print("LED off")
            GPIO.output(rc1, True)
            self.is_on = True

    #########################################################################
    # Lights Switch
    #########################################################################

    def lights_switch(self, event=None):
        if self.is_on:
            print("Lights on")
            GPIO.output(rc2, False)
            self.is_on = False
        else:
            print("Lights off")
            GPIO.output(rc2, True)
            self.is_on = True

    #########################################################################
    # Camera Switch
    #########################################################################
    def camera_switch(self, event=None):
        #camera = PiCamera()
        if self.is_on:
            #camera.start_preview()
            print("Cam on")

            self.is_on = False
        else:
            print("Cam off")
            # camera.stop_preview()
            # camera.close()

            self.is_on = True


if __name__ == "__main__":
    app = App()
    app.mainloop()