#!/usr/bin/env python3
import time
import requests
import pickle
import cv2
import RPi.GPIO as GPIO
from Motor import Motor

PUB_SUB_DELAY = 0
IR_SENSOR = 40  


class Master:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(IR_SENSOR, GPIO.IN)

        self.motor = Motor()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FPS, 5)

        print('starting...')
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
            self.motor.move('right|0.3')
        else:
            if content['dir'] == 'L':
                self.motor.move('left|0.1')
            elif content['dir'] == 'R':
                self.motor.move('right|0.1')
            else:
                print('object found and in path')
                self.move_forward()
                return False
        
        return True

    def move_forward(self):
        while GPIO.input(IR_SENSOR):
            self.motor.move('forward|0.2')


Master()