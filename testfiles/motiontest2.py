import keyboard
import sys

def kb():
    while True:
        #your code here
        if keyboard.is_pressed("a"): #replace with your key
            print("Key interrupt detected")

        #or here
if __name__ == "__main__":
    kb()
