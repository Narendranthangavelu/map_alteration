#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf import TransformListener
from std_msgs.msg import String
import time

class update_map:
    def __init__(self, ):
        self.tf = TransformListener()
        self.pub = rospy.Publisher("/update_map", String , queue_size=2)
        self.boundaries = rospy.get_param("~boundaries", [])
    def process(self):
        print(self.boundaries)




if __name__ == '__main__':
    rospy.init_node('map_update', anonymous=True)
    upd = update_map()
    upd.process()

