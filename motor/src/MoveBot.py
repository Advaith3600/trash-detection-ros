#!/usr/bin/env python3
import rospy
import time
import RPi.GPIO as GPIO
from std_msgs.msg import String

# 31 - right forward
# 32 - right backward
# 35 - left forward
# 36 - left backward


class MoveBot:
    def __init__(self):
        self.initialize_input_output()

        rospy.init_node('motor', anonymous=True)
        rospy.Subscriber('move_bot', String, self.handle_move)

        rospy.spin()

    def initialize_input_output(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        for i in (31, 32, 35, 36):
            GPIO.setup(i, GPIO.OUT)

    def move(self, delay, *ports):
        for port in ports:
            GPIO.output(port, GPIO.HIGH)

        rospy.sleep(delay)

        for port in ports:
            GPIO.output(port, GPIO.LOW)

    def handle_move(self, movement):
        movement = str(movement)[7:-1]
        print(movement)
        if 'forward' in movement:
            self.move(float(movement[8:]), 31, 35)
        elif 'backward' in movement:
            self.move(float(movement[9:]), 32, 36)
        elif 'right' in movement:
            self.move(float(movement[6:]), 35)
        elif 'left' in movement:
            self.move(float(movement[5:]), 31)


MoveBot()
