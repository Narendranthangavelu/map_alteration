#!/bin/bash

sleep 2
usr/bin/tmux -2 new-session -d -s startup
usr/bin/tmux send-keys -t startup.0 "python /home/pi/ROS_Workspaces/NHBot_WS/src/saya_bringup/script/startup.py" ENTER
sleep 1
