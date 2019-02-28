#!/usr/bin/python2
# *-* coding: utf-8 *-*


import socket
import sys
import time
from device_config import *
import collections
from utils_uhf import *


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.39', 80)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

# dataDict  = collections.OrderedDict()
# readCardsCount = 5

# while True:
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

    # try:
print >>sys.stderr, 'connection from', client_address

        # while True:
# writeStr = 'BB0049000D0000FFFF0300000002123456786D7E'
# readStr = 'BB00270003222710837E'
# readStr = 'BB003900090000FFFF0300000002457E'
readStr = 'BB00220000227E'
read = readStr.decode('hex')

# print("sending : "+ readStr)
connection.send(read)
time.sleep(1)
data = connection.recv(10240)
# data01 = data.encode('hex')
# if(data = )
dataHex = bytes_to_hex(data)
# print (dataHex)

EPC = dataHex[16:40]

print (EPC)

# process_buffer(dataHex)
# print >>sys.stderr, 'received "%s"' % dataHex

# readCardsCount = 5
#
# dataDict = collections.OrderedDict()
#
# dataDict[dataHex] = 1
#
# if(len(dataDict.keys()) >= readCardsCount):
#     for x in dataDict.keys():
#         print("KEY : "+ x)
#
#     sys.exit(0)
# else:
#     print(len(dataDict.keys()))

# write = 'BB0049000D0000FFFF0300000002123456786D7E'.decode('hex')
# readmulti = 'BB00270003222710837E'.decode('hex')
# readdata = 'BB003900090000FFFF0300000002457E'.decode('hex')

# print >>sys.stderr, 'received "%s"' % data01

# if data:
#     print >>sys.stderr, 'sending data back to the client'
# else:
#     print >>sys.stderr, 'no more data from', client_address
    # break

    # finally:
connection.close()

