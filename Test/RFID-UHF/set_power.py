#!/usr/bin/python2
# *-* coding: utf-8 *-*


import socket
import sys
import time
from utils_uhf import *


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.39', 80)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

print >>sys.stderr, 'connection from', client_address

power = 2600
setPwrStr = setPowerCommandGen(power)

set = setPwrStr.decode('hex')
connection.send(set)

time.sleep(1)

data = connection.recv(10240)

dataHex = bytes_to_hex(data)
print dataHex

connection.close()
