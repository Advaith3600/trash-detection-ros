#!/usr/bin/env python3
import rospy
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN)

try:
    while True:
        print(GPIO.input(40))
finally:
    GPIO.cleanup()
