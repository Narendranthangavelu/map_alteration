#!/bin/bash




#closing controllers
/usr/bin/tmux send-keys -t controllers.0 "" C-c
sleep 6

#killing all tmux servers
/usr/bin/tmux kill-session -t controllers



