import time
import tkinter
import customtkinter
import time
import board
from busio import I2C
import adafruit_bme680
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# Setting up theme of GUI
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.is_on = True
        self.title("Cool Blue")
        self.geometry(f"{220}x{160}")
        self.temperature = tkinter.IntVar()
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        # create frame for environmental variable
        self.temperature_frame = customtkinter.CTkFrame(self)
        self.temperature_frame.grid(row=0, column=1, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="n")
        self.temperature_frame.grid_rowconfigure(2, weight=1)

        self.label_temperature = customtkinter.CTkLabel(master=self.temperature_frame, text="Temperature")
        self.label_temperature.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="")

        self.label_temperature_value = customtkinter.CTkLabel(
            master=self.temperature_frame, textvariable=self.temperature,
            font=customtkinter.CTkFont(size=50, weight="bold"))
        self.label_temperature_value.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky="e")

        self.label_temperature_value = customtkinter.CTkLabel(
            master=self.temperature_frame, text = f'\N{DEGREE CELSIUS}',
            font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label_temperature_value.grid(row=1, column=3, columnspan=1, padx=(10, 10), pady=10, sticky="sw")

        self.temp()  # call the temp function just once

    def temp(self):
        self.temperature.set(Temp.current())
        self.after(1000, self.temp)  # 2000 milliseconds = 2 seconds

import random
class Temp:
    temp = 0

    def current():
        while True:
            TEMPERATURE = round(bme680.temperature, 2)
            time.sleep(1)

if __name__ == "__main__":
    app = App()
    app.mainloop()





