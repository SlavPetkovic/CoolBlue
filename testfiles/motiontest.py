
import board
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from picamera import PiCamera

from time import sleep
import pygame
import os

kit1 = MotorKit()
kit2 = MotorKit(address=0x61)

# Initialise the second hat on a different address
# kit2 = MotorKit(address=0x61)
rc1 = 23
rc2 = 24

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(rc1, GPIO.OUT)
GPIO.setup(rc2, GPIO.OUT)
kit1.motor1.throttle = 0
kit2.motor1.throttle = 0

GPIO.output(rc1, True)
GPIO.output(rc2, True)
GPIO.setwarnings(False)
camera = PiCamera()
# camera.close()
screen = pygame.display.set_mode([1, 1])

cam_state = 'off'
led_state = 'off'

try:
    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    kit1.motor1.throttle = 1.0
                    kit2.motor1.throttle = 1.0

                elif event.key == pygame.K_q:
                    pygame.quit()
                    camera.close()
                    kit1.motor1.thorttle = 0
                    kit2.motor1.thorttle = 0

                elif event.key == pygame.K_r:
                    if cam_state == 'off':
                        camera.start_preview()
                        cam_state = 'on'
                    elif cam_state == 'on':
                        camera.stop_preview()
                        camera.close()
                        cam_state = 'off'


                elif event.key == pygame.K_l:
                    if led_state == 'off':
                        GPIO.output(rc1, False)
                        GPIO.output(rc2, False)
                        led_state = 'on'
                    elif led_state == 'on':
                        GPIO.output(rc1, True)
                        GPIO.output(rc2, True)
                        led_state = 'off'

            elif event.type == pygame.KEYUP:
                kit1.motor1.throttle = 0
                kit2.motor1.throttle = 0

finally:
    GPIO.cleanup()
    camera.stop_preview()
    camera.close()

    cam_state = 'off'
    led_state = 'off'

