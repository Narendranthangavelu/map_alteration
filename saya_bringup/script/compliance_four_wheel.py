#!/usr/bin/env python

import sys
import rospy
from dynamixel_controllers.srv import SetComplianceSlope,SetComplianceMargin



def set_compliance():
	#right wheel slope
	rospy.wait_for_service('front_right_wheel_joint/set_compliance_slope') 
	try:
		set_right = rospy.ServiceProxy('front_right_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_right(5)
        except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#left wheel slope
	rospy.wait_for_service('front_left_wheel_joint/set_compliance_slope')
	try:
		set_left = rospy.ServiceProxy('front_left_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_left(5)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

	rospy.wait_for_service('rear_right_wheel_joint/set_compliance_slope')
	try:
		set_left = rospy.ServiceProxy('rear_right_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_left(5)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

	rospy.wait_for_service('rear_left_wheel_joint/set_compliance_slope')
	try:
		set_left = rospy.ServiceProxy('rear_left_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_left(5)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e



if __name__ == "__main__":
	set_compliance()
