usr/bin/tmux -2 new-session -d -s nodemon
usr/bin/tmux send-keys -t nodemon.0 "cd ~/Documents/kp_bot_new_features/kpbotservices" ENTER
sleep 1
usr/bin/tmux send-keys -t nodemon.0 "nodemon" ENTER