#!/usr/bin/env python3
import rospy
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from std_msgs.msg import String

publisher = None
hostName = "192.168.43.4"
serverPort = 3600


class RoboServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        filename = Path(__file__).resolve().parent / 'control.html'
        with open(filename, 'r') as file:
            for line in file:
                self.wfile.write(bytes(line, 'utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself

        if publisher:
            direction = post_data['direction']
            delay = post_data['delay']
            publisher.publish(f'{direction}|{delay}')
            self.wfile.write(bytes(json.dumps({ 'success': True }), 'utf-8'))


if __name__ == "__main__":
    rospy.init_node('control', anonymous=True)
    publisher = rospy.Publisher('move_bot', String, queue_size=10)

    webServer = HTTPServer((hostName, serverPort), RoboServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
