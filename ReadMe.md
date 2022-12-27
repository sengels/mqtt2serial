# What is mqtt2serial?

mqtt2serial is used to bridge the gap between a [dcc++ basestation](https://github.com/Locoduino/DCCpp) and mqtt. it runs on a raspberry pi as a service side by side with the mosquitto mqtt broker and a web server for the web app. The pi in turn is connected via serial cable to the arduino.
Commands and answers can be send within your network; mqtt helps to not having to worry about multiple clients or an artificial NIH network protocol.

# how to install mqtt2serial
* sudo apt install python3-pip
* sudo pip3 install -r requirements.txt
(or
sudo apt install -y python3-paho-mqtt python3-lockfile python3-daemon python3-serial)
* sudo mkdir /var/log/nagf2rpi/
* sudo touch /var/log/nagf2rpi/mqtt2serial.log
* sudo touch /var/log/nagf2rpi/mqtt2seriald.log
* sudo chmod 775 -R /var/log/nagf2rpi/
* sudo chmod +x mqtt2seriald.py
* sudo ln -s mqtt2serial.service /etc/systemd/system/mqtt2serial.service
* sudo systemctl daemon-reload

# License etc.
There is limited use for this, thats why a permissive license. If it helps you I am glad too.
