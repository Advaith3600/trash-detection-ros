#!/usr/bin/env python3
import rospy
import time
import RPi.GPIO as GPIO
from std_msgs.msg import String


class MoveBot:
    def __init__(self):
        self.initialize_input_output()

        rospy.init_node('motor', anonymous=True)
        pub = rospy.Subscriber('move_bot', String, self.handle_move) 

    def initialize_input_output(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(29, GPIO.OUT)
        GPIO.setup(31, GPIO.OUT)
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)


    def move(self, *ports):
        for port in ports:
            GPIO.output(port, GPIO.HIGH)

        time.sleep(3)

        for port in ports:
            GPIO.output(port, GPIO.LOW)

    def handle_move(self, movement):
        if movement == 'forward':
            self.move(29, 31)
        elif movement == 'backward':
            self.move(32, 33)
        elif movement == 'right':
            self.move(29, 32)
        elif movement == 'left':
            self.move(31, 33)
            

MoveBot()
