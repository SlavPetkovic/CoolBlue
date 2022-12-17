import time
import board
import adafruit_dht
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
from adafruit_dht import DHT22
import threading

dht22_temperature = ""
dht22_humidity = ""


def dht22_read():
    global dht22_temperature
    global dht22_humidity
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    while True:
        try:
            # Print the values to the serial port
            dht22_temperature = dhtDevice.temperature
            dht22_humidity = dhtDevice.humidity
            print(
                "Temperatur: {:.1f} C    Luftfeuchtigkeit: {}% ".format(
                    dht22_temperature, dht22_humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)


dht22_thread = threading.Thread(target=dht22_read)
dht22_thread.start()

root = tk.Tk()
root.geometry('800x480')
root.resizable(width=False, height=False)

image = Image.open('Download.jpeg').resize((30, 30))
photo = ImageTk.PhotoImage(image)

temperatur = tk.StringVar()
temperatur.set("")

luftfeuchtigkeit = tk.StringVar()
luftfeuchtigkeit.set("")

temp = tk.StringVar()
temp.set('Temperatur:')

luft = tk.StringVar()
luft.set('Luftfeuchtigkeit:')

label = ttk.Label(root, textvariable=temp)
label.pack()

label1 = ttk.Label(root, textvariable=temperatur)
label1.pack()

label2 = ttk.Label(root, textvariable=luft)
label2.pack()

label3 = ttk.Label(root, textvariable=luftfeuchtigkeit)
label3.pack()

button_an = ttk.Button(root, text='Loggen An')
button_an.pack()

button_aus = ttk.Button(root, text='Loggen Aus')
button_aus.pack()

button_close = ttk.Button(root, image=photo, command=root.destroy)
button_close.pack()


def update_values():
    luftfeuchtigkeit.set(str(dht22_humidity))
    temperatur.set(str(dht22_temperature))
    root.after(1000, update_values)


root.after(1000, update_values)
root.mainloop()