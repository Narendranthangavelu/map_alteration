#!/bin/bash

#starting controllers and bringup
sleep 1
usr/bin/tmux -2 new-session -d -s controllers
usr/bin/tmux send-keys -t controllers.0 "roslaunch eva_arm_controller eva_arm_controller.launch" ENTER
sleep 14
usr/bin/tmux -2 new-session -d -s bringup
usr/bin/tmux send-keys -t bringup.0 "roslaunch saya_bringup saya_inaugration.launch" ENTER
sleep 10

#stating chrome
#usr/bin/tmux -2 new-session -d -s chrome
#usr/bin/tmux send-keys -t chrome.0 "google-chrome --noerrordialogs --kiosk file:///home/asimov/IRA_V2_ws/Saya_ui/eng/index.html" ENTER
#sleep 3



#you can connect to this session using command : "tmux attach-session -t pi"
tmux -2 new-session -d -s eye
tmux send-keys -t eye.0 "ssh pi@192.168.0.3" ENTER
sleep 5
tmux send-keys -t eye.0 "python /boot/Pi_Eyes/random_eyes.py" ENTER

