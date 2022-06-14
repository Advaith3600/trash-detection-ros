#!/usr/bin/env python3
import rospy
import time
import requests
import pickle
import cv2
from std_msgs.msg import String


class Master:
    def __init__(self):
        rospy.init_node('master', anonymous=True)
        self.pub = rospy.Publisher('move_bot', String, queue_size=10)
        self.camera = cv2.VideoCapture(0)

        print('starting...')
        # self.run()

    def run(self):
        ret, frame = self.camera.read()
        data = pickle.dumps(cv2.rotate(frame, cv2.ROTATE_180))

        response = requests.post('http://192.168.43.154:8080', data=data)
        content = response.json()

        self.handle_request(content)

    def handle_request(self, content):
        if content['status'] == 0:
            self.pub.publish('right|0.3')
            time.sleep(0.3)
            self.run()
        else:
            if content['dir'] == 'L':
                self.pub.publish('left|0.1')
                time.sleep(0.1)
                self.run()
            elif content['dir'] == 'R':
                self.pub.publish('right|0.1')
                time.sleep(0.1)
                self.run()
            else:
                print('object found and in path')
                self.move_forward()

    def move_forward(self):
        self.pub.publish('forward|2')
        time.sleep(2)


Master()
