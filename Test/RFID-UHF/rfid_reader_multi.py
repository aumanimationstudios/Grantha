#!/usr/bin/python2
# *-* coding: utf-8 *-*


import socket
import sys
import time
from helper import *
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

print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

print >>sys.stderr, 'connection from', client_address
pollingTime = 1000
# readStr = 'BB00270003222710837E'
readStr = severalTimesPollingCommandGen(pollingTime)

read = readStr.decode('hex')
# print readStr
connection.send(read)

time.sleep(1)
# print("sending : "+ readStr)

data = connection.recv(10240)
# data01 = data.encode('hex')
# if(data = )
dataHex = bytes_to_hex(data)
# print dataHex


dataArray = dataHex.split("7EBB")
# print dataArray

cleanDataArray = []

for x in dataArray:
    # if len(x) == 46:
    if x.startswith("BB"):
        # dataArray.remove(x)
        y = x[2:]
        cleanDataArray.append(y)
        # print dataArray

    elif x.endswith("7E"):
        # dataArray.remove(x)
        z = x[:-2]
        cleanDataArray.append(z)
        # print dataArray

    else:
        cleanDataArray.append(x)

# print cleanDataArray
dataDict = collections.OrderedDict()
# print dataDict

for x in cleanDataArray:
    if len(x) == 44:
        # print(x +"\n")

        Type = x[0:2]
        # print (Type)

        Command = x[2:4]
        # print (Command)

        PL = x[4:8]
        # print (PL)

        RSSI = x[8:10]
        # print (RSSI)

        PC = x[10:14]
        # print (PC)

        EPC = x[14:38]
        # print (EPC)
        dataDict[EPC] = 1
        CRC = x[38:42]
        # print (CRC)

        Checksum = x[42:44]
        # print (Checksum)



    # print len(x)
# process_buffer(dataHex)
# print >>sys.stderr, 'received "%s"' % dataHex

# dataDict[dataHex] = 1

# if(len(dataDict.keys()) >= readCardsCount):
#     for x in dataDict.keys():
#         print("KEY : "+ x)

stopStr = 'BB00280000287E'
stop = stopStr.decode('hex')
connection.send(stop)
data = connection.recv(4096)
dataHex = bytes_to_hex(data)
# print(dataHex)
connection.close()

for x in dataDict:
    print (x+"\n")





