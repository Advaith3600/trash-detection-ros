#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ports = (31, 32, 35, 36)

for port in ports:
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, GPIO.LOW)
    time.sleep(0.2)

GPIO.cleanup()