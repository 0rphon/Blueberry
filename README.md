# Blueberry
written years ago. uploaded as part of me uploading all my old projects\
a custom touch screen music player made for the raspberry pi.\
plays music from a Music/ folder with each subdir as its own genre/playlist\
made for use on rasbian with adafruit-pitft touch screen display. no idea if it still works properly\
\
STEPS TO SET IT UP:\
#enable vnc\
raspi-config\
ENABLE VNC\
\
#enable touch screen\
cd ~\
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh\
chmod +x adafruit-pitft.sh\
sudo ./adafruit-pitft.sh\
\
#transfer Blueberry/ to /home/pi/\
\
#get dependancies\
sudo apt-get update\
sudo apt-get upgrade\
sudo apt-get install vlc\
sudo pip3 install python-vlc\
sudo apt-get install pulseaudio\
sudo apt-get install xdotool\
\
#change sound to analog and turn up\
\
#set up auto start\
mkdir /home/pi/.config/lxsession\
mkdir /home/pi/.config/lxsession/LXDE-pi\
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart\
ENTER INTO FILE\
@lxpanel --profile LXDE-pi\
@pcmanfm --desktop --profile LXDE-pi\
@xscreensaver splash\
@lxterminal -e /home/pi/Blueberry/run.sh\
\
#create run.sh\
nano /home/pi/Blueberry/run.sh\
ENTER INTO FILE\
#! /bin/bash\
/usr/bin/python3 /home/pi/Blueberry/Blueberry.py>>/home/pi/Blueberry/output\
xdotool windowminimize $(xdotool getactivewindow)\
\
chmod+x /home/pi/Blueberry/run.sh\
