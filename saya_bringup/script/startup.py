from subprocess import check_output
import time
import subprocess


js_file = "/home/pi/ROS_Workspaces/NHBot_WS/src/ui/kp_bot_new_features/kp_bot_new_features/assets/js/data.js"
bash_file = "/home/pi/.bashrc"


def replace_line(file_name, search_word, replace_line):
    done = False
    with open(file_name, 'r') as file:
        filedata = file.readlines()
        for i, line in enumerate(filedata):
            if search_word in line:
                filedata[i] = replace_line + "\n"
                done = True
                file.close()
                break
    with open(file_name, 'w') as file:
        file.writelines(filedata)
        file.close()
    return done

def add_line(file_name,line):
    with open(file_name, 'a') as file:
        file.write("\n"+ line + "\n")
        file.close()


def change_bash(address,file_name= "bash.txt"):
    changed_ip = False
    changed_master = False
    master_line = "export ROS_MASTER_URI=http://" + address +":11311"
    ip_line = "export ROS_IP=" + address
    changed_master = replace_line(file_name,"ROS_MASTER",master_line)
    if not changed_master:
        add_line(file_name,master_line)

    changed_ip = replace_line(file_name, "ROS_IP", ip_line)
    if not changed_ip:
        add_line(file_name,ip_line)

def change_html(address,file_name= "data.js"):
    changed_html = False
    line = "url : 'ws://" + str(address) + ":9090'"
    changed_html = replace_line(file_name,"ws:",line)


def get_ip():
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips.replace("\n","")
    ip_list = []
    ip_list = ips.split()
    if len(ip_list) == 0:
        ip_list.append("")
    return ip_list[-1]

def change_all_ips(ip):
    print('changing')
    change_html(address=ip,file_name=js_file)
    change_bash(address=ip, file_name= bash_file)
    return

def change_html_ips(ip):
    print('changing')
    change_html(address=ip,file_name=js_file)
    return

def start_manager():
    print('starting manager')
    start_cmd = "sudo systemctl start start_manager.service"
    start = subprocess.Popen(start_cmd.split())
    start.wait()
    print("finish starting manager")
    return

def stop_manager():
    print('stopping manager')
    stop_cmd = "sudo systemctl stop start_manager.service"
    stop = subprocess.Popen(stop_cmd.split())
    stop.wait()
    print("finish stopping manager")
    return


old_ip = None
disconnect_count = 0


# to run the ip checking continuously ...
# ~ while(True):
    # ~ ip = get_ip()
    # ~ if ip != old_ip and ip != "":
        # ~ old_ip = ip
        # ~ print(ip)
        # ~ stop_manager()
        # ~ change_all_ips(ip)
        # ~ start_manager()
    # ~ if ip == "" and ip != old_ip:
        # ~ stop_manager()
        # ~ old_ip = ip
    # ~ time.sleep(1)
    
# to run ip check only once.
# ~ ip = get_ip()
# ~ while(True):
    # ~ if ip != old_ip and ip != "":
        # ~ old_ip = ip
        # ~ print(ip)
        # ~ stop_manager()
        # ~ change_all_ips(ip)
        # ~ start_manager()
    # ~ if ip == "" and ip != old_ip:
        # ~ stop_manager()
        # ~ old_ip = ip
        # ~ ip= get _ip()
    # ~ time.sleep(1)


# it will check the disconnection for 10 seconds . then it will turn off controller
    
while(True):
    ip = get_ip()
    if ip != old_ip and ip != "":
        old_ip = ip
        print(ip)
        stop_manager()
        # ~ change_all_ips(ip)
        change_html_ips(ip)
        start_manager()
    if ip == "" and ip != old_ip:
        disconnect_count += 1
        if disconnect_count > 100:  # wait for 100 seconds before cloisng if its not connected to wifi
            stop_manager()
            old_ip = ip
            
    if ip != "":
        disconnect_count = 0 
    

    time.sleep(1)






