#!/usr/bin/env python


import socket
HOST='192.168.42.1'
PORT=5002
HOST = socket.gethostbyname(socket.gethostname())
print HOST
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
print s
s.listen(1)
conn,add = s.accept()
s.setsocopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
print "connected by", addr
