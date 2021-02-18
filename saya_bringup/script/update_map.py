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
        self.map_name = "map.pgm"
        self.altered_map_name = "map_alter.pgm"
        self.map_changed = False
        self.interval = 2

    def sort_positions(self, dic):
        if dic['x1'] < dic['x2']:
            a = dic['x1']
            b = dic['x2']
        else:
            b = dic['x1']
            a = dic['x2']
        if dic['y1'] < dic['y2']:
            c = dic['y1']
            d = dic['y2']
        else:
            d = dic['y1']
            c = dic['y2']
        return a,b,c,d

    def check_if_gets_stucked(self):
        # try:
        position, quaternion = self.tf.lookupTransform("/map", "/base_link", rospy.Time(0))
        for i in range(len(self.boundaries)):
            a,b,c,d = self.sort_positions(i)
            print(a,b,c,d)
            print(position)
            if a <= position[0] and b>= position[0]:
                if c<= position[1] and c>= position[1]:
                    return True
        return False
        # except:
        #     return False





    def process(self):
        while not rospy.is_shutdown():
            result = self.check_if_gets_stucked()
            print(result)
        #     if result and not self.map_changed:
        #         self.map_changed = True
        #         self.pub.publish(self.altered_map_name)
        #     if self.map_changed and not result:
        #         self.pub.publish(self.map_name)
            time.sleep(self.interval)







if __name__ == '__main__':
    rospy.init_node('map_update', anonymous=True)
    upd = update_map()
    upd.process()

