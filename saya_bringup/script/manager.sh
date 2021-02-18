#!/bin/bash
#bash -c "source /opt/ros/kinetic/setup.bash && source /home/asimov/IRA_V2_ws/devel/setup.bash && roslaunch saya_bringup saya_manager.launch &"
sleep 5
usr/bin/tmux -2 new-session -d -s manager
usr/bin/tmux send-keys -t manager.0 "roslaunch saya_bringup saya_manager.launch" ENTER
sleep 1
