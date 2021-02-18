#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf import TransformListener
import time


class update_amcl:

    def __init__(self, x_max, x_min, y_max, y_min, interval=4):
        self.tf = TransformListener()
        self.pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=2)
        self.sub = rospy.Subscriber("/amcl_pose",PoseWithCovarianceStamped,self.receive_amcl)
        self.position = None
        self.quaternion = None
        self.interval = interval
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.update_fin = False
        self.old_amcl = PoseWithCovarianceStamped()
        self.amcl_count = 0

    def get_position(self):
        try:
            position, quaternion = self.tf.lookupTransform("/map", "/base_link", rospy.Time(0))
            self.position = position
            self.quaternion = quaternion
            return True
        except:
            return False

    def in_boundary(self):
        if self.x_min < self.position[0] < self.x_max:
            if self.y_min < self.position[1] < self.y_max:
                return True
        return False

    def receive_amcl(self,data):
        self.amcl_count += 1
        self.old_amcl = data
        self.old_amcl.pose.covariance =  [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.06853892326654787]

    def publish_pose(self):
        pos = PoseWithCovarianceStamped()
        pos.header.frame_id = "map"
        pos.pose.pose.position.x = self.position[0]
        pos.pose.pose.position.y = self.position[1]
        pos.pose.pose.orientation.w = self.quaternion[3]
        pos.pose.pose.orientation.z = self.quaternion[2]
        pos.pose.covariance = [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.06853892326654787]
        self.pub.publish(pos)

    def process(self):
        count = 0
        while not rospy.is_shutdown():
            time.sleep(self.interval)
            print(self.get_position())
            if self.get_position():
                print(self.position)
                if self.in_boundary() :
                    print("in")
                    if not self.update_fin or count > 3 :
                        if self.amcl_count > 2:
                            self.publish_pose()
                            self.amcl_count = 0
                        self.update_fin = True
                        count = 0
                    else:
                        count += 1
                else:
                    count = 0
                    self.update_fin = False
                    if self.amcl_count > 2:
                        self.pub.publish(self.old_amcl)
                        self.amcl_count = 0



if __name__ == '__main__':
    rospy.init_node('amcl_update', anonymous=True)
    interval = 3
    # ~ x_min = -1.0
    # ~ x_max = 3.5
    # ~ y_min = 0.0
    # ~ y_max = 9.8
    
    x_min = 0.0
    x_max = 0.0
    y_min = 0.0
    y_max = 0.0

    upd = update_amcl(x_max, x_min, y_max, y_min, interval)
    upd.process()





