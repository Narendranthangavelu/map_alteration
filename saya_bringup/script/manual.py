#!/usr/bin/env python
import rospy
import rospkg
import sys
from std_msgs.msg import Empty,String
from sensor_msgs.msg import Joy
import subprocess
import time
import os

#path_pub = rospy.Publisher('load_paths', String, queue_size=10)
speech_pub = rospy.Publisher('speech/state', String, queue_size=1)

def process(data):
	global speech_pub
	if data.buttons[1] == 1:
		print("hi")
		time.sleep(1)
		string = 'python /home/asimov/IRA_V2_ws/src/triggers/salute.py'
		res = subprocess.call(string, shell=True)
		time.sleep(2)
	# if data.buttons[0] == 1:
	# 	print("")
	# 	time.sleep(1)
	# 	string = 'python /home/asimov/IRA_V2_ws/src/triggers/namaste.py'
	# 	res2 = subprocess.call(string, shell=True)
	# 	time.sleep(2)



if __name__=="__main__":
	rospy.init_node("joy_buttons")
	rospy.Subscriber("/joy", Joy, process, queue_size=1)
	rospy.spin()
