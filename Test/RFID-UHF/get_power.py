#!/usr/bin/python2
# *-* coding: utf-8 *-*

import socket
import sys
import time
from utils_uhf import *
# from helper import *
# from device_config import *
# import collections


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.39', 80)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

print >>sys.stderr, 'connection from', client_address

getPwrStr = "BB00B70000B77E"

get = getPwrStr.decode('hex')
connection.send(get)

time.sleep(1)

data = connection.recv(10240)

dataHex = bytes_to_hex(data)
print dataHex

PW = int(dataHex[10:14], 16)
print(PW)

connection.close()

