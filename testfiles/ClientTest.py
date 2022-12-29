import socket as sc
import time
from playsound import playsound
# Create a socket and connect to the Raspberry Pi
socket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
socket.connect(('192.168.2.88', 12345))
print( "Systems Online")
playsound('../data/SysOnline.mp3')


while True:
    # Send a command to turn the LED on
    socket.send(b"ON")
    time.sleep(5)
    socket.send(b"OFF")
    time.sleep(5)


# Close the connection

