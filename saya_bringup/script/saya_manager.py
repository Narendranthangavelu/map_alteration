#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Empty
from std_msgs.msg import Int16MultiArray
from rosgraph_msgs.msg import Log
from lcd_msgs.msg import lcd
from subprocess import check_output
import os
import sys
import subprocess
import time
import signal

error = False
close = False
finish = False

emergency = False
mode = "nav"
change_mode = False
turn_off_controller = False
turn_off_system = False
shut_data = None
controller_turned_off = True
long_press_count =0
first_off_state_received= False


def get_ip():
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips.replace("\n","")
    ip_list = []
    ip_list = ips.split()
    if len(ip_list) == 0:
        ip_list.append("")
    return ip_list[-1]
    
    
def clear_lcd():
    publish_display_text("",1)
    publish_display_text("",2)
    publish_display_text("",3)
def switch_cb(data):
    global emergency, turn_off_controller,controller_turned_off, shut_data, long_press_count,first_off_state_received
    em_sw = data.data[0]
    ip_but = data.data[1]
    #ip_but = 0
    
    # this is to check whether switches are connected during startup
    if ip_but == 1:
        first_off_state_received = True
    # this is to count for long press of ip button for shutdown command
    if ip_but == 0 and first_off_state_received:
        long_press_count += 1
    else:
        long_press_count = 0
        
    if long_press_count > 8:    # publish 2 messages per second ... 8 == 4 seconds
        shut_data = "shutdown"
        long_press_count = 0
    if not emergency and em_sw == 1:
        turn_off_controller = True
        publish_display_text("Emergency pressed")
        controller_turned_off = True
    emergency = (em_sw == 1)
    print("emergency_pressed",emergency)
    return

def show_link():
    try:
        ip = get_ip()
        link = ip + ":80"
        publish_display_text(link,3)
    except:
        print("cant find ip")

def publish_display_text(display_text,line = 1):
    text = lcd()
    text.line = line
    text.font = 'small'
    text.text = display_text
    # Publishing the text

    text_pub.publish(text)
    print("Text published. Closing Program")
    print(display_text)

    return


def mode_change(data):
    global mode, change_mode
    if mode == "nav" and data.data == "map":
        change_mode = True
    elif mode == "map" and data.data == "nav":
        change_mode = True
    mode = data.data
    return


def start_controllers():
    start_cmd = "sudo systemctl start start_controllers.service"
    active_cmd = "systemctl is-active start_controllers.service"
    start = subprocess.Popen(start_cmd.split())
    start.wait()
    return


def stop_controllers():
    stop_cmd = "sudo systemctl stop start_controllers.service"
    active_cmd = "systemctl is-active start_controllers.service"
    stop = subprocess.Popen(stop_cmd.split())
    stop.wait()
    return


def stop_map():
    stop_cmd = "sudo systemctl stop start_map.service"
    active_cmd = "systemctl is-active start_map.service"
    stop = subprocess.Popen(stop_cmd.split())
    stop.wait()
    return


def stop_nav():
    stop_cmd = "sudo systemctl stop start_nav.service"
    active_cmd = "systemctl is-active start_nav.service"
    stop = subprocess.Popen(stop_cmd.split())
    stop.wait()
    return


def start_nav():
    start_cmd = "sudo systemctl start start_nav.service"
    active_cmd_nav = "systemctl is-active start_nav.service"
    active_cmd_map = "systemctl is-active start_map.service"
    act = subprocess.Popen(active_cmd_map.split(), stdout=subprocess.PIPE)
    out, err = act.communicate()
    if "active" in out:
        stop_map()
    start = subprocess.Popen(start_cmd.split())
    start.wait()
    return


def start_map():
    start_cmd = "sudo systemctl start start_map.service"
    active_cmd_nav = "systemctl is-active start_nav.service"
    active_cmd_map = "systemctl is-active start_map.service"
    act = subprocess.Popen(active_cmd_nav.split(), stdout=subprocess.PIPE)
    out, err = act.communicate()
    if "active" in out:
        stop_nav()
    start = subprocess.Popen(start_cmd.split())
    start.wait()
    return


def shutdown_sys():
    shutdown_cmd = "sudo shutdown now"
    shut = subprocess.Popen(shutdown_cmd.split())
    shut.wait()


def shutdown_cb(data):
    global shut_data
    shut_data = data.data
    return


def check_controller():
    global emergency,controller_turned_off
    print("check controlerls")

    if not emergency:
        # ~ publish_display_text("starting operations")
        print("starting cotrol")
        active_cmd = "systemctl is-active start_controllers.service"
        act = subprocess.Popen(active_cmd.split(), stdout=subprocess.PIPE)
        out, err = act.communicate()
        if "inactive" in out or "failed" in out:
            start_controllers()
            publish_display_text("starting operations")
            controller_turned_off = False
    return


def check_main_function():
    global mode
    print("check function")
    if mode == "map":
        # print("check map")
        active_cmd = "systemctl is-active start_map.service"
        act = subprocess.Popen(active_cmd.split(), stdout=subprocess.PIPE)
        out, err = act.communicate()
        if "inactive" in out or "failed" in out:
            print("starting map")
            start_map()
    elif mode == "nav":
        print("check nav")
        active_cmd = "systemctl is-active start_nav.service"
        act = subprocess.Popen(active_cmd.split(), stdout=subprocess.PIPE)
        out, err = act.communicate()
        print(out)
        if "inactive" in out or "failed" in out:
            print("starting nav")
            start_nav()
    return


def manager():
    global emergency, turn_off_controller, mode, change_mode, shut_data,controller_turned_off
    clear_lcd()
    show_link()
    while not rospy.is_shutdown():
        rospy.sleep(3.0)
        if shut_data == "shutdown":
            clear_lcd()
            publish_display_text("shutting down")
            print("shutting down")
            #_ = subprocess.call('mpg123 /home/asimov/IRA_V2_ws/src/audio/shutdown.mp3', shell=True)
            stop_controllers()
            stop_map()
            stop_nav()
            shut_data = None
            shutdown_sys()

        check_controller()  # check if controller is stopped .. and turn on that controller
        if not controller_turned_off:
            check_main_function()  # check if main funciton is stopped .. and turn on that mainfunction(map or nav)

        if turn_off_controller:
            stop_controllers()
            turn_off_controller = False
            controller_turned_off = True
            stop_map()
            stop_nav()

        if change_mode:
            stop_nav()
            stop_map()
            change_mode = False

        if shut_data == "restart":
            
            stop_controllers()
            stop_map()
            stop_nav()
            shut_data = None
def node_shutdown():
    clear_lcd()

if __name__ == '__main__':
    rospy.init_node('manager', anonymous=True)
    rospy.Subscriber("/switch_state", Int16MultiArray, switch_cb)
    rospy.Subscriber("/shut", String, shutdown_cb)
    rospy.Subscriber("/working_mode", String, mode_change)
    text_pub = rospy.Publisher('/lcd_topic', lcd, queue_size=1)
    rospy.on_shutdown(node_shutdown)
    manager()
