#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess
import shlex
import rospy
def callback(data):

    if (data.data == 'true'):
        subprocess.call('mpg123 /home/asimov/IRA_V2_ws/src/audio/speech_ready.mp3',shell=True) 
        try: 
            print "got result"   
            pr=subprocess.Popen(shlex.split("tmux new -d -s speech"),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
            subprocess.call(shlex.split('tmux send-keys -t speech.0 "roslaunch saya_states chatbot_esaf.launch" ENTER'))
            rospy.set_param('/speech_launch/processid',pr.pid)
        except rospy.ROSInterruptException:
            pass
        #subprocess.call('python /home/asimov/IRA_V2_ws/src/turnkey_setup/src/speech_launch.py', shell=True)
    if (data.data == 'false'):
        pr=subprocess.call(shlex.split("tmux kill-session -t speech"),shell=False)
        #subprocess.call('python /home/asimov/IRA_V2_ws/src/turnkey_setup/src/speech_kill.py', shell=True)
        subprocess.call('mpg123 /home/asimov/IRA_V2_ws/src/audio/speech_close.mp3',shell=True)
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('speech_node', anonymous=True)

    rospy.Subscriber("speech/state", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

