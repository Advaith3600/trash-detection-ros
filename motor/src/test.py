#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ports = (31, 32, 35, 36)

for port in ports:
    GPIO.setup(port, GPIO.OUT)

print('configured')


def moveRobo(*ports):
    for port in ports:
        GPIO.output(port, GPIO.HIGH)

    time.sleep(3)

    for port in ports:
        GPIO.output(port, GPIO.LOW)

    time.sleep(2)


for port in ports:
    print(port)
    moveRobo(port)


# print('moving forward')
# moveRobo([29, 31])

# print('moving backward')
# moveRobo([32, 33])

exit()

