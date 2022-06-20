#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
from utils import sleep

# 31 - right forward
# 32 - right backward
# 35 - left forward
# 36 - left backward


class Motor:
    def __init__(self):
        self.initialize_input_output()

    def initialize_input_output(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        for i in (31, 32, 35, 36):
            GPIO.setup(i, GPIO.OUT)

    def handle_move(self, delay, *ports):
        print(delay, ports)
        for port in ports:
            GPIO.output(port, GPIO.HIGH)

        sleep(delay)

        for port in ports:
            GPIO.output(port, GPIO.LOW)

    def move(self, movement):
        print(movement)

        if 'forward' in movement:
            self.handle_move(float(movement[8:]), 31, 35)
        elif 'backward' in movement:
            self.handle_move(float(movement[9:]), 32, 36)
        elif 'right' in movement:
            self.handle_move(float(movement[6:]), 35)
        elif 'left' in movement:
            self.handle_move(float(movement[5:]), 31)

