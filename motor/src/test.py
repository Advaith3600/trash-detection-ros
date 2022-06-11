#!/usr/bin/env python3
import time
import rospy
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

print('configured')


def moveRobo(*ports):
    print(ports)
    for port in ports:
        GPIO.output(port, GPIO.HIGH)

    time.sleep(3)

    for port in ports:
        GPIO.output(port, GPIO.LOW)

    time.sleep(2)


# for i in (29, 31, 32, 33):
#     print(i)
#     moveRobo(i)


print('moving forward')
moveRobo([29, 31])

print('moving backward')
moveRobo([32, 33])

exit()

