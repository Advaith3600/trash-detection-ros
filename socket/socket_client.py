#importing libraries
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
# from IPython.display import Image
import torch
def get_dist(p1,p2):
    return math.sqrt((p1[1]-p2[1])**2 + (p1[0]-p2[0])**2)
def get_ang(xmin,ymin,xmax,ymax,img):
    mp_of_img= [(xmax-xmin)//2,(ymax-ymin)//2]
    mp_of_frame= [(img.shape[1])//2,0)]
    hyp=get_dist(mp_of_img,mp_of_frame)
    base=(ymax-ymin)//2
    cos_theta=base/hyp
    return(math.acos(cos_theta))



model = torch.hub.load('ultralytics/yolov5', 'custom', 'D:\\OneDrive\\Desktop\\ros\\yolov5-master\\runs\\train\\exp4\\weights\\best.torchscript',force_reload=True)
# model=torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
# Client socket
# create an INET, STREAMing socket :
send_data = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.9'# Standard loopback interface address (localhost)
port1 = 10058 # Port to listen on (non-privileged ports are > 1023)
port2 = 3306
# now connect to the web server on the specified port number
client_socket.connect((host_ip,port1))
send_data.connect((host_ip,port2))
#'b' or 'B'produces an instance of the bytes type instead of the str type
#used in handling binary data from network connections
data = b""
# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    # results = model(imgs)
    # results.print()
    # results.save(".")
    results = model(frame)
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
            count = count + 1
            message_dict={}
            message_dict["angle"]=ang
            message = json.dumps(message_dict)
            send_data.sendall(message)

        cv2.imshow('Object Detector',frame);
    else:
        continue


    # cv2.imshow("Receiving...",frame)
    key = cv2.waitKey(10)
    if key  == 13:
        break
client_socket.close()
