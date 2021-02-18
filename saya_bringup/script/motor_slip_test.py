#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist

state1 = False
state2 = False
state3 = False
state4 = False
state5 = False
state6 = False
time_interval = 100 #seconds
speed = 2.0

def motor_rotate_sequence():
    global state1, state2, state3, state4, state5, state6, time_interval, speed
    data = Twist()
    data.linear.x = 0.0
    data.linear.y = 0.0
    data.angular.z = 0.0
    start_time = rospy.Time.now().secs
    rate = rospy.Rate(10)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    while not rospy.is_shutdown():
        if not state1:
            data.linear.x = speed
            pub.publish(data)
            rospy.loginfo("State 1: Moving Forward")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state1 = True
        elif not state2:
            data.linear.x = -1.0 * speed
            pub.publish(data)
            rospy.loginfo("State 2: Moving Backward")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state2 = True
        elif not state3:
            data.linear.y = speed
            pub.publish(data)
            rospy.loginfo("State 3: Strafing Left")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state3 = True
        elif not state4:
            data.linear.y = -1.0 * speed
            pub.publish(data)
            rospy.loginfo("State 4: Strafing Right")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state4 = True
        elif not state5:
            data.angular.z = -1.0 * speed
            pub.publish(data)
            rospy.loginfo("State 5: Rotating Clockwise")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state5 = True
        elif not state6:
            data.angular.z = speed
            pub.publish(data)
            rospy.loginfo("State 6: Rotating AntiClockwise")
            rate.sleep()
            current_time = rospy.Time.now().secs
            time_diff = current_time - start_time
            if(time_diff == time_interval):
				start_time = current_time
				rospy.loginfo("Time_Diff: " + str(time_diff))
				state6 = True
        else:
            state1 = False
            state2 = False
            state3 = False
            state4 = False
            state5 = False
            state6 = False
            rospy.loginfo("Resetting State Machine")
            rate.sleep()
        
if __name__ == '__main__':
    try:
        rospy.init_node('motor_sequence', anonymous=True)
        motor_rotate_sequence()
    except rospy.ROSInterruptException:
        pass
