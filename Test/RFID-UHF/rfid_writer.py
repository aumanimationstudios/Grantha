#!/usr/bin/python2
# *-* coding: utf-8 *-*


import socket
import sys
import time
from helper import *
from device_config import *


def process_buffer(hexdata):
    # FINDING CARD ID IN CODE
    if len(hexdata) >= LENGTH_OF_CARD_RAW_DATA:
        start_index = hexdata.find(CARD_DATA_PREFIX)
        if start_index >= 0:
            hexdata = hexdata[start_index:]

            if len(hexdata) >= LENGTH_OF_CARD_RAW_DATA:
                hexdata = hexdata[CARD_DATA_PREFIX_LENGTH:]

                next_index = hexdata.find(CARD_DATA_PREFIX)
                if next_index < 0 or next_index >= CARD_VARIABLE_DATA_LENGTH:
                    card_data = CARD_DATA_PREFIX + hexdata[:CARD_VARIABLE_DATA_LENGTH]
                    print("card data : " + card_data)
                else:
                    hexdata = hexdata[next_index:]
                    print 'Bad Data'
        else:
            print 'Data Incomplete'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.39', 80)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        while True:
            time.sleep(1)
            selectStr = "BB0012000100147E"
            selectHex  = selectStr.decode('hex')
            connection.send(selectHex)
            time.sleep(1)
            dataSelect = connection.recv(1024)

            time.sleep(1)
            dataSelectHex = bytes_to_hex(dataSelect)

            print >> sys.stderr, 'selected  "%s"' % dataSelectHex

            writeStr = 'BB0049000D0000FFFF0300000002123456786D7E'
            # writeStr = 'BB003900090000FFFF0300000002457E'
            # writeStr = 'BB00220000227E'
            read = writeStr.decode('hex')

            print("sending : "+ writeStr)
            connection.sendall(read)
            data = connection.recv(1024)
            # data01 = data.encode('hex')
            # if(data = )
            dataHex = bytes_to_hex(data)
            # process_buffer(dataHex)
            print >>sys.stderr, 'received "%s"' % dataHex
            # write = 'BB0049000D0000FFFF0300000002123456786D7E'.decode('hex')
            # readmulti = 'BB00270003222710837E'.decode('hex')
            # readdata = 'BB003900090000FFFF0300000002457E'.decode('hex')

            # print >>sys.stderr, 'received "%s"' % data01

            if data:
                print >>sys.stderr, 'sending data back to the client'
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            break
    finally:
        connection.close()

    break
