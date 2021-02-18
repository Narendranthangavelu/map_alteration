#!/usr/bin/env python

from saya_bringup.srv import *
import rospy
import numpy as np
import urllib
import cv2

def id_fun(req):

    url='http://localhost:8080/snapshot?topic=/camera/image_raw'
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite('/home/asimov/Documents/kp_bot_new_features/id_image/image1.png',image)
    rospy.loginfo(rospy.get_caller_id() + "I heard ")
    return "completed"

def id_image_server():
    rospy.init_node('id_image_server')
    s = rospy.Service('id_image_server', demo_srv, id_fun)
    
    rospy.spin()

if __name__ == "__main__":
    id_image_server()