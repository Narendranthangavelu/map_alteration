#!/bin/bash




#closing controllers and bringup
/usr/bin/tmux send-keys -t bringup.0 "" C-c
sleep 6

#killing all tmux servers
/usr/bin/tmux kill-session -t bringup
/usr/bin/tmux kill-session -t web
/usr/bin/tmux kill-session -t server


