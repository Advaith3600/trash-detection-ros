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
model = torch.hub.load('ultralytics/yolov5', 'custom', 'D:\\OneDrive\\Desktop\\ros\\yolov5-master\\runs\\train\\exp4\\weights\\best.torchscript',force_reload=True)
def get_dist(p1,p2):
    return math.sqrt((p1[1]-p2[1])**2 + (p1[0]-p2[0])**2)
def get_ang(xmin,ymin,xmax,ymax,img):
    mp_of_img= [(xmax-xmin)//2,(ymax-ymin)//2]
    mp_of_frame= [(img.shape[1])//2,0]
    hyp=get_dist(mp_of_img,mp_of_frame)
    base=(ymax-ymin)//2
    cos_theta=base/hyp
    return(math.acos(cos_theta))

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        global model
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        frame=None
        try:
            frame = pickle.loads(post_data)
        except:
            if frame:
                df_result = results.pandas().xyxy[0]
                dict_result = df_result.to_dict()
                # print(dict_result)
                scores = list(dict_result["confidence"].values())
                labels = list(dict_result["name"].values())
                if dict_result["confidence"]:
                    highest_pred_label=max(dict_result["confidence"])
                    highest_pred_val=dict_result["confidence"][highest_pred_label]
                    list_boxes = list()
                    # print(df_result.to_dict('records'))
                    dict_item=df_result.to_dict('records')[highest_pred_label]
                    list_boxes.append(list(dict_item.values())[:4])
                    count = 0
                    for xmin, ymin, xmax, ymax in list_boxes:
                        ang=get_ang(xmin,ymin,xmax,ymax,frame)
                        frame = cv2.rectangle(frame, pt1=(int(xmin),int(ymin)), pt2=(int(xmax),int(ymax)), \
                                                 color=(255,0, 0), thickness=2)
                        cv2.putText(frame, f"{labels[count]}: {round(highest_pred_val, 2)}", (int(xmin), int(ymin)-10), \
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                        self._set_response()
                        self.wfile.write(str(ang).encode('utf-8'))
                    cv2.imshow('Object Detector',frame)
                else:
                    self._set_response()
                    self.wfile.write("Could not detect a plastic bottle".encode('utf-8'))

            else:

                self._set_response()
                self.wfile.write("Give me a cv2 byte image DAMMMIT".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('192.168.1.3', port)
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
