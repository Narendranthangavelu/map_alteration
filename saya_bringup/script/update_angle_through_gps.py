#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf import TransformListener
import time
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class update_angle:

    def __init__(self):
        self.pub = rospy.Publisher("/set_pose", PoseWithCovarianceStamped, queue_size=2)
        self.odom_sub = rospy.Subscriber("/ridgeback_velocity_controller/odom",Odometry,self.receive_odom,queue_size=1)
        self.gps_sub = rospy.Subscriber("/hedge_pose_compensated", PoseWithCovarianceStamped, self.receive_gps)
        self.min_velocity_needed = 0.1
        self.tf = TransformListener()
        self.odom_x = []
        self.odom_y = []
        self.gps_x = []
        self.gps_y = []
        self.read_gps = False
        self.gps_count = 0
        self.odom_count = 0
        self.odom_miss_count = 0
        self.min_distance = 0.5
        self.stop_sampling = False
        self.variation_of_distance_allowed = 0.5
        self.max_samples_in_buffer = 150
        self.start_collecting = False
        self.update_limit = 1.57

    def calculate_distance(self,x,y):
        a = np.sqrt(pow((x[-1] -x[0]),2) + pow((y[-1] -y[0] ),2))
        return a

    def find_line_angle(self,x, y):
        m, b = np.polyfit(x, y, 1)
        angle = np.arctan(m)
        if x[0] > x[-1]:
            angle = np.pi + angle
        if angle < 0.0:
            angle = 2 * np.pi + angle
        return angle

    def receive_odom(self,data):
        if not self.stop_sampling:
            if abs(data.twist.twist.linear.x) > self.min_velocity_needed:
                self.start_collecting = True
                self.odom_miss_count = 0
            else:
                self.odom_miss_count += 1
                if self.odom_miss_count > 5:  # if continuous low speed reset every thing
                    self.start_collecting = False
                    self.reset()
            if self.start_collecting:
                position, quaternion = self.tf.lookupTransform("/odom", "/base_link", rospy.Time(0))
                self.odom_x.append(position[0])
                self.odom_y.append(position[1])
                self.read_gps = True
                self.odom_count +=1

                if self.calculate_distance(self.odom_x, self.odom_y) > self.min_distance:
                    self.start_collecting = False
                    self.stop_sampling = True
                if len(self.odom_x) > self.max_samples_in_buffer:
                    self.start_collecting = False
                    self.stop_sampling = True


    def reset(self):
        # ~ print("resetting", self.gps_count, self.odom_count, self.odom_miss_count)
        self.odom_x = []
        self.odom_y = []
        self.gps_x = []
        self.gps_y = []
        self.gps_count = 0
        self.odom_count = 0
        self.odom_miss_count = 0
        self.start_collecting = False


    def receive_gps(self, data):
        if self.start_collecting:
            self.gps_x.append(data.pose.pose.position.x)
            self.gps_y.append(data.pose.pose.position.y)
            self.gps_count += 1

    def process(self):
        # print("start")
        if self.stop_sampling:
            # print("sample")
            odom_travelled = self.calculate_distance(self.odom_x, self.odom_y)
            if self.gps_count > 4:
                gps_travelled = self.calculate_distance(self.gps_x, self.gps_y)
            else:
                gps_travelled = 0.0
            print("distance" , odom_travelled)
            distance_drifted = abs(odom_travelled - gps_travelled)
            if (self.gps_count > 4 and (self.variation_of_distance_allowed * odom_travelled > distance_drifted)):
                odom_angle = self.find_line_angle(self.odom_x, self.odom_y)
                gps_angle = self.find_line_angle(self.gps_x, self.gps_y)
                angle_diff = gps_angle - odom_angle
                if angle_diff > np.pi:
                    angle_diff = angle_diff - 2*np.pi
                elif angle_diff < -1 * np.pi:
                    angle_diff = angle_diff + 2 * np.pi
                print("diff_angle", angle_diff, odom_angle, gps_angle)
                calculated_quaternion = quaternion_from_euler(0,0,angle_diff)

                position, quaternion = self.tf.lookupTransform("/map", "/odom", rospy.Time(0))
                (roll,pitch,yaw)= euler_from_quaternion(quaternion)
                angle_diff_btw_tf_and_calculated = abs((yaw + np.pi)  - (angle_diff+ np.pi))
                if angle_diff_btw_tf_and_calculated > np.pi:
                    angle_diff_btw_tf_and_calculated = 2* np.pi - angle_diff_btw_tf_and_calculated
                print("diff-angle in tf and calcualted", angle_diff_btw_tf_and_calculated, yaw)
                if angle_diff_btw_tf_and_calculated > self.update_limit:
                    new_pose = PoseWithCovarianceStamped()
                    new_pose.pose.pose.position.x = self.gps_x[-1]
                    new_pose.pose.pose.position.y = self.gps_y[-1]
                    new_pose.pose.pose.position.z = 0.0
                    new_pose.pose.pose.orientation.x = calculated_quaternion[0]
                    new_pose.pose.pose.orientation.y = calculated_quaternion[1]
                    new_pose.pose.pose.orientation.z = calculated_quaternion[2]
                    new_pose.pose.pose.orientation.w = calculated_quaternion[3]
                    new_pose.header.frame_id = "map"
                    self.pub.publish(new_pose)
            print("resetting", self.gps_count, self.odom_count, self.odom_miss_count)
            self.reset()
            time.sleep(3)
            self.stop_sampling= False





if __name__ == '__main__':
    rospy.init_node('angle_update', anonymous=True)
    ang_update = update_angle()
    while not rospy.is_shutdown():
        time.sleep(1)
        ang_update.process()
