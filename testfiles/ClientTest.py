import socket

# Create a socket and connect to the Raspberry Pi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.2.88', 12345))



# Send a command to turn the LED on
s.send(b"ON")

# Close the connection
s.close()