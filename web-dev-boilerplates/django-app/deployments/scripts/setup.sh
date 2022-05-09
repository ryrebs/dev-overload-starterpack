Arch-linux

# add system group 
sudo groupadd --system webapps
# add user and set webapps as default group
sudo useradd -r -m -g webapps -s  /bin/bash rpi
# change owner of the app folder to newly created folder
# and add users group 
sudo chown -R rpi:users /root/folder
# give group a write access
sudo chmod  -R g+w /root/folder
# update project folder to have webapps as group
sudo chown -R :webapps /project/folder

