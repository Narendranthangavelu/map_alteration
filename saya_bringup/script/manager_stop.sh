#!/bin/bash


/usr/bin/tmux send-keys -t manager.0 "" C-c
sleep 3
/usr/bin/tmux kill-session -t manager
sleep 1

usr/bin/tmux -2 new-session -d -s cont_stop
usr/bin/tmux send-keys -t cont_stop.0 "sudo systemctl stop start_controllers.service" ENTER
sleep 5

usr/bin/tmux -2 new-session -d -s map_stop
usr/bin/tmux send-keys -t map_stop.0 "sudo systemctl stop start_map.service" ENTER
sleep 5

usr/bin/tmux -2 new-session -d -s nav_stop
usr/bin/tmux send-keys -t nav_stop.0 "sudo systemctl stop start_nav.service" ENTER
sleep 5

/usr/bin/tmux kill-session -t cont_stop
/usr/bin/tmux kill-session -t map_stop
/usr/bin/tmux kill-session -t nav_stop


