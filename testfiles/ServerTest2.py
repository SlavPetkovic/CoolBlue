import socket
import RPi.GPIO as GPIO

# Set up the GPIO pin for output
import RPi.GPIO as GPIO


rc1 = 23
rc2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(rc1, GPIO.OUT)
# GPIO.output(rc1, True)

# Create a socket and bind to a port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 12345))
s.listen(1)

# Accept an incoming connection
conn, addr = s.accept()
print("Connected by", addr)

while True:
    # Receive data from the client
    data = conn.recv(1024)
    if not data:
        break
    data = data.decode()
    print("Received data:", data)

    # Control the LED based on the received data
    if data == "ON":
        GPIO.output(rc1, True)
    elif data == "OFF":
        GPIO.output(rc1, False)

# Close the connection
# conn.close()