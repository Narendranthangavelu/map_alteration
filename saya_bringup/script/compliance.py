#!/usr/bin/env python

import sys
import rospy
from dynamixel_controllers.srv import SetComplianceSlope,SetComplianceMargin

#Joint 1 slope and margin
slope1=6
margin1=10
#Joint 2 slope and margin
slope2=10
margin2=5
#Joint 3 slope and margin
slope3=8
margin3=10
#Joint 4 slope and margin
slope4=3
margin4=15
#Joint 5 slope and margin
slope5=6
margin5=10
#Joint 6 slope and margin
slope6=10
margin6=5
#Joint 7 slope and margin
slope7=8
margin7=10
#Joint 8 slope and margin
slope8=3
margin8=15

def set_compliance():
	#right wheel slope
	rospy.wait_for_service('front_right_wheel_joint/set_compliance_slope') 
	try:
		set_right = rospy.ServiceProxy('front_right_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_right(3)
        except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#left wheel slope
	rospy.wait_for_service('front_left_wheel_joint/set_compliance_slope')
	try:
		set_left = rospy.ServiceProxy('front_left_wheel_joint/set_compliance_slope', SetComplianceSlope)
		set_left(3)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint1 slope
	rospy.wait_for_service('joint1_controller/set_compliance_slope')
	try:
		set_joint1s = rospy.ServiceProxy('joint1_controller/set_compliance_slope', SetComplianceSlope)
		set_joint1s(slope1)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint1 margin
	rospy.wait_for_service('joint1_controller/set_compliance_margin')
	try:
		set_joint1m = rospy.ServiceProxy('joint1_controller/set_compliance_margin', SetComplianceMargin)
		set_joint1m(margin1)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint2 slope
	rospy.wait_for_service('joint2_controller/set_compliance_slope')
	try:
		set_joint2s = rospy.ServiceProxy('joint2_controller/set_compliance_slope', SetComplianceSlope)
		set_joint2s(slope2)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint2 margin
	rospy.wait_for_service('joint2_controller/set_compliance_margin')
	try:
		set_joint2m = rospy.ServiceProxy('joint2_controller/set_compliance_margin', SetComplianceMargin)
		set_joint2m(margin2)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint3 slope
	rospy.wait_for_service('joint3_controller/set_compliance_slope')
	try:
		set_joint3s = rospy.ServiceProxy('joint3_controller/set_compliance_slope', SetComplianceSlope)
		set_joint3s(slope3)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint3 margin
	rospy.wait_for_service('joint3_controller/set_compliance_margin')
	try:
		set_joint3m = rospy.ServiceProxy('joint3_controller/set_compliance_margin', SetComplianceMargin)
		set_joint3m(margin3)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint4 slope
	rospy.wait_for_service('joint4_controller/set_compliance_slope')
	try:
		set_joint4s = rospy.ServiceProxy('joint4_controller/set_compliance_slope', SetComplianceSlope)
		set_joint4s(slope4)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint4 margin
	rospy.wait_for_service('joint4_controller/set_compliance_margin')
	try:
		set_joint4m = rospy.ServiceProxy('joint4_controller/set_compliance_margin', SetComplianceMargin)
		set_joint4m(margin4)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint5 slope
	rospy.wait_for_service('joint5_controller/set_compliance_slope')
	try:
		set_joint5s = rospy.ServiceProxy('joint5_controller/set_compliance_slope', SetComplianceSlope)
		set_joint5s(slope5)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint5 margin
	rospy.wait_for_service('joint5_controller/set_compliance_margin')
	try:
		set_joint5m = rospy.ServiceProxy('joint5_controller/set_compliance_margin', SetComplianceMargin)
		set_joint5m(margin5)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint6 slope
	rospy.wait_for_service('joint6_controller/set_compliance_slope')
	try:
		set_joint6s = rospy.ServiceProxy('joint6_controller/set_compliance_slope', SetComplianceSlope)
		set_joint6s(slope6)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint6 margin
	rospy.wait_for_service('joint6_controller/set_compliance_margin')
	try:
		set_joint6m = rospy.ServiceProxy('joint6_controller/set_compliance_margin', SetComplianceMargin)
		set_joint6m(margin6)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint7 slope
	rospy.wait_for_service('joint7_controller/set_compliance_slope')
	try:
		set_joint7s = rospy.ServiceProxy('joint7_controller/set_compliance_slope', SetComplianceSlope)
		set_joint7s(slope7)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint7 margin
	rospy.wait_for_service('joint7_controller/set_compliance_margin')
	try:
		set_joint7m = rospy.ServiceProxy('joint7_controller/set_compliance_margin', SetComplianceMargin)
		set_joint7m(margin7)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint8 slope
	rospy.wait_for_service('joint8_controller/set_compliance_slope')
	try:
		set_joint8s = rospy.ServiceProxy('joint8_controller/set_compliance_slope', SetComplianceSlope)
		set_joint8s(slope8)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
	#joint8 margin
	rospy.wait_for_service('joint8_controller/set_compliance_margin')
	try:
		set_joint8m = rospy.ServiceProxy('joint8_controller/set_compliance_margin', SetComplianceMargin)
		set_joint8m(margin8) 
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

if __name__ == "__main__":
	set_compliance()
