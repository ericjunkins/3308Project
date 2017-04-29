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

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
print "connected by", addr

conn.send("hello")
