#!/bin/sh
# launcher.sh

cd /
cd home/pi/startUp
sudo pigpiod
sleep 10
sudo python rcCar.py
cd /

