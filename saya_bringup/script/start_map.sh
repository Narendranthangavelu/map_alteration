#!/bin/bash

#starting controllers and bringup
sleep 10

/usr/bin/tmux -2 new-session -d -s web
/usr/bin/tmux send-keys -t web.0 "roslaunch saya_bringup web.launch" ENTER

/usr/bin/tmux -2 new-session -d -s server
/usr/bin/tmux send-keys -t server.0 "pushd /home/pi/ROS_Workspaces/NHBot_WS/src/ui/kp_bot_new_features/kp_bot_new_features; python -m SimpleHTTPServer 8000; popd;
" ENTER


usr/bin/tmux -2 new-session -d -s map
usr/bin/tmux send-keys -t map.0 "roslaunch saya_bringup mapping.launch" ENTER

sleep 3

