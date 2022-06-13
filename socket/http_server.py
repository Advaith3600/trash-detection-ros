#Imports
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np
import cv2
from pathlib import Path
import math
import json
import torch
import base64
#load Model from localhost Custom
model = torch.hub.load('ultralytics/yolov5', 'custom', 'D:\\OneDrive\\Desktop\\ros\\yolov5-master\\runs\\train\\exp4\\weights\\best.torchscript',force_reload=True)


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    def do_POST(self):
        global model
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        frame = pickle.loads(post_data)
        print("Does this work?")
        if len(frame)!=0:
            results = model(frame)
            df_result = results.pandas().xyxy[0] # <--- converts result into panda
            dict_result = df_result.to_dict()
            # scores = list(dict_result["confidence"].values()) # <--- gets confidence values
            # labels = list(dict_result["name"].values()) # <--- gets names
            if dict_result["confidence"]:
                highest_pred_label=max(dict_result["confidence"])# <--- selects label with highest confidence
                highest_pred_val=dict_result["confidence"][highest_pred_label]
                list_boxes = list()
                dict_item=df_result.to_dict('records')[highest_pred_label]# <---gets record of highest confidence label
                list_boxes.append(list(dict_item.values())[:4])# <--- Gets the bounding box for records
                count = 0
                for xmin, ymin, xmax, ymax in list_boxes:
                    ang,dir=get_ang(xmin,ymin,xmax,ymax,frame)
                    frame = cv2.rectangle(frame, pt1=(int(xmin),int(ymin)), pt2=(int(xmax),int(ymax)), \
                                             color=(255,0, 0), thickness=2) # <--- prints bounding box
                    cv2.putText(frame, f"{labels[count]}: {round(highest_pred_val, 2)}", (int(xmin), int(ymin)-10), \
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2) # <--- prints confidence values
                    cv2.imwrite("data.jpg",frame)
                    self._set_response()
                    message_dict={"status":1}
                    message_dict["angle"]=ang
                    message_dict["dir"]=dir
                    message = json.dumps(message_dict)
                    # cv2.imshow('Object Detector',frame)
                    self.wfile.write(bytes(message,encoding="utf-8"))

            else:
                self._set_response()
                message_dict={"status":0}
                message_dict["angle"]="Bottle Not FOund"
                cv2.imwrite("data.jpg",frame)
                message = json.dumps(message_dict)
                self.wfile.write(bytes(message,encoding='utf-8'))
        else:
            self._set_response()
            message_dict={"status":2}
            message_dict["angle"]="No frame"
            message = json.dumps(message_dict)
            self.wfile.write(bytes(message,encoding="utf-8"))


#get dist bw 2 points
def get_dist(p1,p2):
    return math.sqrt((p1[1]-p2[1])**2 + (p1[0]-p2[0])**2)
#calculate angle between two
def get_ang(xmin,ymin,xmax,ymax,img):
    mp_of_img= (int((xmin+xmax)/2),int((ymin+ymax)/2))
    mp_of_frame= (int((img.shape[1])//2),img.shape[0])
    print(mp_of_img,xmin,ymin,xmax,ymax)
    img=cv2.line(img,mp_of_img,mp_of_frame,(0,255,0),2)
    hyp=get_dist(mp_of_img,mp_of_frame)
    base=int((ymin+ymax)/2)
    img=cv2.line(img,((img.shape[1])//2,int(base)),mp_of_frame,(0,255,0),2)
    cos_theta=base/hyp
    dir="L"
    if mp_of_img[0]>mp_of_frame[0]:
        dir="R"

    return(math.acos(cos_theta)*180/3.14,dir)

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('192.168.43.154', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
