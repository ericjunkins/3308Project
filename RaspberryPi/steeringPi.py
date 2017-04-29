from myPigpio import turn
from myPigpio import throttle
import pigpio
import time
from types import *
import os
import socket
import time


HOST = "192.168.42.1"
PORT = 5008
buffer_size = 1024

last_sig = 0

pi = pigpio.pi()
stGPIO = 23
pi.set_mode(stGPIO,pigpio.OUTPUT)

#stop signals on pin 23 in case there is some when file started. Keeps from
#raspberry pi crashing
pi.wave_tx_stop()
base_st = []

#turns wheels to "null" position at 0. 
base_st.append(pigpio.pulse(1<<stGPIO,0,1.5*1000))
base_st.append(pigpio.pulse(0,1<<stGPIO, 8.5*1000))
pi.wave_add_generic(base_st)
st_wid = pi.wave_create()
if st_wid >= 0:
        #repeat this signal until told something else
        pi.wave_send_repeat(st_wid)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while(True):
    data = s.recv(buffer_size)
    if not data: break
    print data
    dataSplit = data.split(",")
    try:
        steer = int(dataSplit[1])
    except:
        steer = last_sig
    if (last_sig != steer):
        turn(steer,pi)
        last_sig = steer
    
