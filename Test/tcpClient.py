#!/usr/bin/python2
# *-* coding: utf-8 *-*

import socket

TCP_IP = '192.168.1.39'
TCP_PORT = 8080
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data
