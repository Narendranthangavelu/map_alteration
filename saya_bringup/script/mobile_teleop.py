#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

pub1 = None
zero_count = 0
def cb(data):
    global pub1, zero_count
    min_lin = 0.3
    max_lin = 0.3
    min_ang = 0.3
    max_ang = 0.3

    # ~ if data.linear.x < min_lin:
        # ~ data.linear.x = min_lin
    # ~ if data.linear.x > max_lin:
        # ~ data.linear.x = max_lin
    # ~ if data.angular.z < min_ang:
        # ~ data.angular.z = min_ang
    # ~ if data.angular.z > max_ang:
        # ~ data.angular.z = max_ang
        
    if data.linear.x > min_lin:
        data.linear.x = 0.31
    elif data.linear.x < -min_lin:
        data.linear.x = -0.31
    else:
        data.linear.x = 0.0
        
    if data.angular.z > min_ang:
        data.angular.z = 0.6
    elif data.angular.z < -min_ang:
        data.angular.z = -0.6
    else:
        data.angular.z = 0.0

    if data.linear.x == 0.0 and data.angular.z == 0.0:
        zero_count += 1
    else:
        zero_count = 0

    if zero_count < 3:
        pub1.publish(data)
    



def listener():
    global pub1
    rospy.init_node('repub_cmd', anonymous=True)
    rospy.Subscriber("/joy_teleop/cmd_vel", Twist, cb)
    pub1 = rospy.Publisher("/ridgeback_velocity_controller/cmd_vel", Twist, queue_size=10)
    while not rospy.is_shutdown():
        rospy.spin()


if __name__ == '__main__':
    listener()
