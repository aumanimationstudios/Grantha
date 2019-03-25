#!/usr/bin/python2
# *-* coding: utf-8 *-*

from multiprocessing import Process, Queue
import socket
import zmq
import time
import sys
import os
from utils_uhf import *
import setproctitle
import threading
import debug

threads = []

def GranthaServer(granthaQueue, socketQueue):
    debug.info ("GranthaServer Started.")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.1.183:4689")

    while True:
        msgFrmCli = socket.recv()
        debug.info ("Message From Client: "+msgFrmCli)
        # try:
        if (msgFrmCli == "READ"):
            granthaQueue.put("READ_SINGLE")
            tagIdSingle = socketQueue.get()
            debug.info (tagIdSingle)
            # try:
            if (tagIdSingle=="NO_CARD"):
                debug.info ("1 No Card Detected!")
                socket.send("NO CARD")
                # raise (ValueError)
            else:
                try:
                    socket.send(tagIdSingle)
                except:
                    debug.info (str(sys.exc_info()))

            # if (msgFrmCli == "READ_MULTI"):
        # try:
        if (msgFrmCli == "READ_MULTI"):
            # try:
            granthaQueue.put("READ_MULTI")
            socket.send("MULTI_READ_STARTED")

            # sqT = socketQThread(socketQueue)
            # sqT.start()

        if (msgFrmCli == "STOP"):
            granthaQueue.put("STOP")
            socket.send("STOPPING")
            # debug.info (msgFrmCli)
            # global threads
            # debug.info (threads)
            # if threads:
            #     # debug.info (threads)
            #     for runningThread in threads:
            #         runningThread.exitThread()
            #         socket.send("ackPass")



def SocketServer(granthaQueue, socketQueue):
    global threads
    debug.info ("SocketServer Started.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    server_address = ((ip, 80))
    sock.bind(server_address)
    sock.listen(1)

    connection, client_address = sock.accept()
    debug.info ("connection from: {}".format(client_address))

    while True:
        msgRecvd = granthaQueue.get()
        debug.info("Message Received:"+msgRecvd)
        if (msgRecvd == "READ_SINGLE"):
            tagId = readSingle(connection)
            socketQueue.put(tagId)

        if (msgRecvd == "READ_MULTI"):
            sqT = socketQThread(socketQueue)
            sqT.start()
            # global threads
            debug.info (threads)
            pollingTime = 10000
            readStr = severalTimesPollingCommandGen(pollingTime)
            # debug.info readStr
            read = readStr.decode('hex')
            connection.send(read)
            # time.sleep(1)
            rmT = readMultiThread(connection, socketQueue)
            # debug.info (type(rmT))
            threads.append(rmT)
            debug.info (threads)
            rmT.start()

        if (msgRecvd == "STOP"):
            debug.info (threads)
            if threads:
                # debug.info (threads)
                for runningThread in threads:
                    runningThread.exitThread()
                threads = []




def readSingle(connection):
    readStr = 'BB00220000227E'
    read = readStr.decode('hex')
    connection.send(read)

    time.sleep(1)

    data = connection.recv(10240)
    dataHex = bytes_to_hex(data)
    dataDict = readVerifier(dataHex)

    if not dataDict:
        debug.info ("2 No Cards Detected!")
        return ("NO_CARD")

    else:
        nearestRssi = None
        nearRestEpc = None
        for x in dataDict:
            if(not nearestRssi):
                nearestRssi = int(dataDict[x]["RSSI"],16)
                nearRestEpc = x
            else:
                if(int(dataDict[x]["RSSI"],16) >= nearestRssi):
                    nearestRssi = int(dataDict[x]["RSSI"],16)
                    nearRestEpc = x
        # debug.info (nearRestEpc)
        tagId = nearRestEpc[16:24]
        return (tagId)




def readMultiOutput(dataHex,socketQueue):
    # debug.info dataHex
    # dataHex = bytes_to_hex(data)

    dataDict = readVerifier(dataHex)
    # debug.info (dataDict)

    if(dataDict):
        for x in dataDict:
            tagId = x[16:24]
            debug.info(tagId)
            socketQueue.put(tagId)

            # debug.info (x)
            # self.ui.textEdit01.setTextColor(self.blueColor)
            # self.ui.textEdit01.append(x)


class socketQThread(threading.Thread):
    def __init__(self, socketQueue):
        super(socketQThread, self).__init__()

        self.socketQueue = socketQueue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while(True):
            try:
                self.socket.connect(("192.168.1.39",4695))
                break
            except:
                debug.info(sys.exc_info())

    def run(self):
        while(True):

            tagIdMulti = self.socketQueue.get()
            debug.info (tagIdMulti)

            self.socket.send(tagIdMulti)

            if (tagIdMulti == "MULTI_STOP"):
                # self.socket.shutdown(1)
                debug.info ("MULTI STOPPED")
                self.socket.close()
                break


class readMultiThread(threading.Thread):
    def __init__(self, connection, socketQueue):
        threading.Thread.__init__(self)
        self.connection = connection
        self.socketQueue = socketQueue
        self.stop = False


    def exitThread(self):
        self.stop = True

    def run(self):
        while True:
            if (self.stop == False):
                # self.connection.send(self.readStr)

                data = self.connection.recv(1024)
                dataHex = bytes_to_hex(data)
                # debug.info dataHex
                readMultiOutput(dataHex,self.socketQueue)
                # self.dataReceived.emit(dataHex)
                time.sleep(0.01)

            else:
                debug.info("Stopping..")
                stopStr = 'BB00280000287E'
                stop = stopStr.decode('hex')
                while True:
                    try:
                        self.connection.send(stop)
                        # time.sleep(0.2)
                        data = self.connection.recv(4096)
                        dataHex = bytes_to_hex(data)

                        if dataHex == "BB01280001002A7E":
                            debug.info ("Reading stopped.")
                            self.socketQueue.put("MULTI_STOP")
                            # self.ui.textEdit01.setTextColor(self.greenColor)
                            # self.ui.textEdit01.append("READING STOPPED!")
                            break
                        else:
                            raise ValueError('Unable to stop')
                    except:
                        debug.info ("Trying Again!" + str(sys.exc_info()))
                        # self.ui.textEdit01.append("TRYING AGAIN!")

                break









if __name__ =="__main__":
    setproctitle.setproctitle("RFIDUHFSERVER")

    GranthaQ = Queue()
    SocketQ = Queue()
    GS = Process(target=GranthaServer, args=(GranthaQ,SocketQ,))
    SS = Process(target=SocketServer, args=(GranthaQ,SocketQ,))
    GS.start()
    SS.start()

    GS.join()
    SS.join()

