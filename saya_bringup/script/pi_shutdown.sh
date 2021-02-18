#!/bin/bash
/usr/bin/tmux -2 new-session -d -s shutdownpi
/usr/bin/tmux send-keys -t shutdownpi.0 "ssh pi@192.168.0.3" ENTER
sleep 2
/usr/bin/tmux send-keys -t shutdownpi.0 "sudo shutdown now" ENTER
sleep 3


