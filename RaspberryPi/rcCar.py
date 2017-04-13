#!/usr/bin/env python

from pigpio import turn
from pigpio import throttle
import myPigpio
import time
from types import *
import os
import socket

'''
This file is for running the RC car. It will create a wifi socket and listen on that socket for data coming from the 
app.
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                                      INITILIZATION
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
data.txt will be used to store previous state of the motor signals sent,
which we will initialize to 0 for both throttle and steering
'''
f = open("data.txt","w")
f.write("0,0")
f.close()

#create an instance of the pigpio class, pi1 will be used to control steering
pi1 = pigpio.pi()

#steering is done on pin 23
pi1.set_mode(23,pigpio.OUTPUT)

#stop signals on pin 23 in case there is some when file started. Keeps from raspberry pi crashing
pi1.wave_tx_stop()
base_st = []

#turns wheels to "null" position at 0. 
base_st.append(pigpio.pulse(1<<23,0,1.5*1000))
base_st.append(pigpio.pulse(0,1<<23, 8.5*1000))
pi1.wave_add_generic(base_st)
st_wid = pi1.wave_create()
if st_wid >= 0:
        #repeate this signal until told something else
        pi1.wave_send_repeat(st_wid)

#create in instance of pigpio class, pi2 will be used to control throttle everything else same as for the steering. 
pi2 = pigpio.pi()
pi2.set_mode(14,pigpio.OUTPUT)
pi2.wave_tx_stop()
base_thr = []
base_thr.append(pigpio.pulse(1<<14,0,1.5*1000))
base_thr.append(pigpio.pulse(0,1<<14, 8.5*1000))
pi2.wave_add_generic(base_thr)
th_wid = pi2.wave_create()
if th_wid >= 0:
        pi2.wave_send_repeat(th_wid)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                             DATA RECEIVE OVER WIFI SOCKET
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#ip address of the raspberry pi, and port chosen
HOST = "192.168.42.1"
PORT = 5005

#small buffer size for speed
buffer_size=15
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen(1)
conn,addr = s.accept()
print "connected by", addr

while 1:
        #recieves the data from the connection
        data = conn.recv(buffer_size)
        
        if not data: break

        #print "recieved data:", data, len(data) data incoming is in the form of a CSV string
        dataSplit = data.split(",")

        #data should be of these lengths depending on the values sent from app
        if len(data) > 8 and len(data) < 15:
                #print dataSplit[1],dataSplit[2]
                move = int(dataSplit[1])
                steer = int(dataSplit[2])
                if (move >= -100 and move <=100 and steer <=100 and steer >= -100):
                        #read the previous values of move and steer from .txt
                        f = open("data.txt", "r")
                        sig = -1
                        oldData = f.readline()
                        f.close()
                        
                        oldDataSplit = oldData.split(",")
                        oldMove = int(oldDataSplit[0])
                        oldSteer = int(oldDataSplit[1])
                        '''
                        #if the values of the old and new move or steer are different than functions the respective 
                        #funtions must be called and values of old steer and new steer to be updated
                        '''

                        # TODO move is set to half its max values, for testing purposes, it eventually its full value
                        if (oldSteer != steer and oldMove != move):
                                os.remove("data.txt")
                                fnew = open("data.txt", "w")
                                fnew.write(str(move) + "," + str(steer))

                                #sig = 1 means both steering and moved have already been dealt with, dont need below calls
                                sig = 1
                                
                                fnew.close()
                                turn(steer,pi1)
                                throttle(move/2,pi2)
                                
                        if (oldSteer != steer and sig != 1):
                                os.remove("data.txt")
                                fnew = open("data.txt", "w")
                                fnew.write(str(move) + "," + str(steer))
                                fnew.close()
                                turn(steer,pi1)
                                
                        if (oldMove != move and sig != 1):
                                os.remove("data.txt")
                                fnew = open("data.txt", "w")
                                fnew.write(str(move) + "," + str(steer))
                                fnew.close()
                                throttle(move/2,pi2)


f.close()
conn.close()
