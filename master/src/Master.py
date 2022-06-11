#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String


class Master:
    def __init__(self):
        rospy.init_node('master', anonymous=True)
        self.pub = rospy.Publisher('move_bot', String)

        self.pub.Publish('forward')
