#!/usr/bin/env python3
import rospy
import time
import requests
import pickle
import cv2
import RPi.GPIO as GPIO
from std_msgs.msg import String

PUB_SUB_DELAY = 0.2
IR_SENSOR = 40


class Master:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(IR_SENSOR, GPIO.IN)

        rospy.init_node('master', anonymous=True)
        self.pub = rospy.Publisher('move_bot', String, queue_size=10)
        self.camera = cv2.VideoCapture(0)

        print('starting...')
        for i in range(2):
            self.run(movement=False)
        self.run()
        GPIO.cleanup()

    def run(self, movement=True):
        state = True
        while state:
            start = time.time()
            ret, frame = self.camera.read()
            data = pickle.dumps(cv2.rotate(frame, cv2.ROTATE_180))

            response = requests.post('http://192.168.43.154:8080', data=data)
            content = response.json()
            print('request sent: ', content, time.time() - start)

            state = self.handle_request(content) if movement else False

    def handle_request(self, content):
        if content['status'] == 0:
            self.pub.publish('right|0.3')
            rospy.sleep(0.3 + PUB_SUB_DELAY)
        else:
            if content['dir'] == 'L':
                self.pub.publish('left|0.1')
                rospy.sleep(0.1 + PUB_SUB_DELAY)
            elif content['dir'] == 'R':
                self.pub.publish('right|0.1')
                rospy.sleep(0.1 + PUB_SUB_DELAY)
            else:
                print('object found and in path')
                self.move_forward()
                return False
        
        return True

    def move_forward(self):
        while GPIO.input(IR_SENSOR):
            self.pub.publish('forward|0.2')
            rospy.sleep(0.2 + PUB_SUB_DELAY)


Master()