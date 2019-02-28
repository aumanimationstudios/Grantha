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

# Reading the tag to get mask for select parameter command.
readStr = 'BB00220000227E'
read = readStr.decode('hex')
connection.send(read)

time.sleep(1)

data = connection.recv(10240)
dataHex = bytes_to_hex(data)
# print (dataHex)
mask = dataHex[16:40]
# print (mask)
selParam = '000C001301000000206000'+mask
# print (selParam)
selParamChecksum = checksumCalculator(selParam)
# print (selParamChecksum)

# Select Parameter Command.
selParamCommandHex = 'BB'+selParam+selParamChecksum+'7E'
# print (selParamCommandHex)
selParamCommand = selParamCommandHex.decode('hex')
try:
    connection.send(selParamCommand)

    time.sleep(1)

    data = connection.recv(10240)
    dataHex = bytes_to_hex(data)

    print (dataHex)
    if dataHex == 'BB010C0001000E7E':
        print ("set select successful.")

except:
    print"trying again"

connection.close()

