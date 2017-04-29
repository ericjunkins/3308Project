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

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while(True):
    data = s.recv(buffer_size)
    if not data: break
    print data
