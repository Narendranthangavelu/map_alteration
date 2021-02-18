#!/bin/bash

#starting controllers 
sleep 1

/usr/bin/tmux -2 new-session -d -s controllers
/usr/bin/tmux send-keys -t controllers.0 "roslaunch eva_arm_controller eva_arm_controller.launch" ENTER

sleep 6



