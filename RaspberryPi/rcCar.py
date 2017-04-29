#!/usr/bin/env python

from myPigpio import turn
from myPigpio import throttle
import pigpio
import time
from types import *
import os
import socket
import time

'''
This file is for running the RC car. It will create a wifi socket and listen on
that socket for data coming from the app.
'''
#create an instance of the pigpio class, pi1 will be used to control steering
#steering is done on pin 23

pi1 = pigpio.pi()
stGPIO = 23
pi1.set_mode(stGPIO,pigpio.OUTPUT)

#stop signals on pin 23 in case there is some when file started. Keeps from
#raspberry pi crashing
pi1.wave_tx_stop()
base_st = []

#turns wheels to "null" position at 0. 
base_st.append(pigpio.pulse(1<<stGPIO,0,1.5*1000))
base_st.append(pigpio.pulse(0,1<<stGPIO, 8.5*1000))
pi1.wave_add_generic(base_st)
st_wid = pi1.wave_create()
if st_wid >= 0:
        #repeat this signal until told something else
        pi1.wave_send_repeat(st_wid)

#pin 14 is used to throttle
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

last_sig = (0,0)

#ip address of the raspberry pi, and port chosen
HOST = "192.168.42.1"
PORT = 5005
PORT2 = 5008
buffer_size=15
try:
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)

        s2.bind((HOST,PORT2))
        s2.listen(1)
        conn2, addr2 = s2.accept()
        print "connected by" , addr2
except:
        print "SOCKET already in use"
while(True):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        

        
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()
        
        print "connected by", addr

        while True:
                data = conn.recv(buffer_size)
                if not data: break
                
                #print "recieved data:", data, len(data)
                dataSplit = data.split(",")
                if len(data) <=15:                  
                        try:
                                #print dataSplit[1],dataSplit[2]
                                move = int(dataSplit[1])
                        except:
                                print "move not valid"
                                move = int(last_sig[0])
                                print last_sig[0]
                        try:
                                steer = int(dataSplit[2])
                                conn2.send("100," + dataSplit[2])
                        except:
                                print "steer not valid"
                                steer = int(last_sig[1])
                                conn2.send("100," + str(last_sig[1]))
                        #print "last sig:", last_sig
                        print "move, steer:", move, steer

                        #if (move >= -100 and move <=100 and steer <=100 and steer >= -100):
                        if (move >= -100 and move <= 100):
                                #read the previous values of move and steer from .txt
                                sig = -1
                                oldMove = last_sig[0]
                                oldSteer = last_sig[1]
                                '''
                                if (oldSteer != steer and oldMove != move):
                                        #print "1"
                                        #sig = 1 means both steering and moved have
                                        sig = 1
                                        throttle(move/2,pi2)
                                        turn(steer,pi1)
                                        last_sig = (move,steer)
                                        
                                if (oldSteer != steer and sig != 1):
                                        #print "2"
                                        turn(steer,pi1)
                                        time.sleep(float(1)/float(200))
                                        last_sig = (oldMove,steer)
                                        throttle(0,pi2)
                                        time.sleep(float(1)/float(500))
                                        throttle(move/2,pi2)
                                '''        
                                if (oldMove != move and sig != 1):
                                        #print "3"
                                        throttle(move/2,pi2)
                                        last_sig = (move,oldSteer)


        conn.close()
conn2.close()
