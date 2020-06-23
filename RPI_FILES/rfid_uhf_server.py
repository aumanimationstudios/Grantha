#!/usr/bin/python2
# *-* coding: utf-8 *-*

### Server for Uhf rfid reading ###
### Needs to be Run as sudo ###

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
import signal
import subprocess

threads = []
user = os.environ['USER']

def GranthaServer(granthaQueue, socketQueue):
    """
    zmq Server to communicate with Grantha
    :param granthaQueue:
    :param socketQueue:
    :return:
    """
    debug.info ("GranthaServer Started.")
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    debug.info(hostname)
    debug.info(ip)
    # Binding REP Socket to tcp port 4689
    sock.bind("tcp://"+ip+":4689")

    while True:
        # Wait for next request from client
        msgFrmCli = sock.recv_multipart()
        debug.info ("Message From Client: "+msgFrmCli[0])

        if (msgFrmCli[0] == "READ"):
            # Put item into the queue
            granthaQueue.put("READ_SINGLE")
            # Remove and return an item from the queue
            tagIdSingle = socketQueue.get()
            debug.info (tagIdSingle)

            if (tagIdSingle=="NO_CARD"):
                debug.info ("No Card Detected!")
                # Send reply back to client
                sock.send_multipart(["NO CARD"])
            else:
                try:
                    sock.send_multipart([tagIdSingle])
                except:
                    debug.info (str(sys.exc_info()))

        if (msgFrmCli[0] == "READ_MULTI"):
            granthaQueue.put(["READ_MULTI",msgFrmCli[1]])
            sock.send("MULTI_READ_STARTED")

        if (msgFrmCli[0] == "STOP"):
            granthaQueue.put("STOP")
            sock.send("STOPPING")

        if (msgFrmCli[0] == "WRITE"):
            granthaQueue.put(["WRITE",msgFrmCli[1]])
            ack = socketQueue.get()
            debug.info(ack)
            sock.send_multipart([ack])

        if (msgFrmCli[0] == "START_CAMERA_PREVIEW"):
            try:
                # Kill Rpi camera live previewing script if running
                os.system("pkill -9 RPI_CAMERA_LIVE")
            except:
                debug.info(str(sys.exc_info()))
            # Run Rpi Camera Previewing script
            subprocess.Popen(["python3", "/home/pi/Grantha/RPI_FILES/rpi_camera_live.py"])
            sock.send("Previewing")

        if (msgFrmCli[0] == "CAPTURE"):
            try:
                os.system("pkill -9 RPI_CAMERA_LIVE")
            except:
                debug.info(str(sys.exc_info()))

            debug.info(msgFrmCli[1])
            # Run Camera Script
            cam = subprocess.Popen(["python3", "/home/pi/Grantha/RPI_FILES/camera.py", msgFrmCli[1]],stdout=subprocess.PIPE)
            for line in iter(cam.stdout.readline,''):
                debug.info(line)
            sock.send("Captured")



def SocketServer(granthaQueue, socketQueue):
    """
    Socket Server to communicate with the Rfid Reader Module
    :param granthaQueue:
    :param socketQueue:
    :return:
    """
    global threads
    debug.info ("SocketServer Started.")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    debug.info(hostname)
    debug.info(ip)
    server_address = ((ip, 80))
    # Bind socket to port 80
    sock.bind(server_address)
    sock.listen(1)

    connection, client_address = sock.accept()
    debug.info ("connection from: {}".format(client_address))

    while True:
        # Remove and return an item from the queue
        msgRecvd = granthaQueue.get()
        debug.info(msgRecvd)

        if (msgRecvd == "READ_SINGLE"):
            tagId = readSingle(connection)
            # Put item into the queue
            socketQueue.put(tagId)

        if (msgRecvd[0] == "READ_MULTI"):
            sqT = socketQThread(socketQueue,msgRecvd[1])
            sqT.start()

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
        if (msgRecvd[0] == "WRITE"):
            # ack = "Recvd"
            ack = writeEpc(connection,msgRecvd[1])
            socketQueue.put(ack)



def readSingle(connection):
    """
    Read Rfid Tag and return tag id
    :param connection:
    :return tagId:
    """
    readStr = 'BB00220000227E'
    read = readStr.decode('hex')
    # Send single polling command to Uhf Reader module
    connection.send(read)

    time.sleep(1)
    # Receive response frame from the Uhf Reader module
    data = connection.recv(10240)
    dataHex = bytes_to_hex(data)
    debug.info(dataHex)
    dataDict = readVerifier(dataHex)

    if not dataDict:
        debug.info ("No Cards Detected!")
        return ("NO_CARD")

    else:
        # Find nearest Epc value and return tag id from it.
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

def writeEpc(connection,tagId):
    readStr = 'BB00220000227E'
    read = readStr.decode('hex')
    connection.send(read)
    time.sleep(1)
    data = connection.recv(10240)
    dataHex = bytes_to_hex(data)
    dataDict = readVerifier(dataHex)
    if not dataDict:
        debug.info ("No Cards Detected!")
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
        debug.info(nearRestEpc)
    selParam = '000C001301000000206000'+nearRestEpc
    selParamChecksum = checksumCalculator(selParam)
    selParamCommandHex = 'BB'+selParam+selParamChecksum+'7E'
    selParamCommand = selParamCommandHex.decode('hex')
    while True:
        try:
            connection.send(selParamCommand)
            time.sleep(1)
            data = connection.recv(10240)
            dataHex = bytes_to_hex(data)
            # print (dataHex)
            if dataHex == 'BB010C0001000E7E':
                debug.info ("set select successful.")
                readEpcStr = 'BB003900090000000001000000084B7E'
                readEpc = readEpcStr.decode('hex')
                connection.send(readEpc)
                time.sleep(1)
                data = connection.recv(10240)
                dataHex = bytes_to_hex(data)
                dataDict = readEpcVerifier(dataHex)
                # debug.info (dataDict)
                if not dataDict:
                    debug.info("No Cards Detected!")
                else:
                    for x in dataDict:
                        debug.info(x)
                        debug.info(x[0:24])
                        # debug.info(x[24:32])
                        epc = x[0:24]+tagId
                        debug.info(epc)
                        writeEpcStr = '00490019000000000100000008' + epc
                        writeEpcChecksum = checksumCalculator(writeEpcStr)
                        writeEpcCommandHex = 'BB' + writeEpcStr + writeEpcChecksum + '7E'
                        writeEpcCommand = writeEpcCommandHex.decode('hex')
                        while True:
                            try:
                                connection.send(writeEpcCommand)
                                time.sleep(0.5)
                                data = connection.recv(1024)
                                dataHex = bytes_to_hex(data)
                                # print (dataHex)
                                Type = dataHex[2:4]
                                Command = dataHex[4:6]
                                debug.info(Type+Command)
                                if Type == '01' and Command == '49':
                                    debug.info ("Write Successful.")
                                    ack = "ack_pass"
                                    return ack
                                else:
                                    debug.info("Unable to write!")
                                    raise Exception('unable to write!')
                            except:
                                # print ("Trying Again!" + str(sys.exc_info()))
                                ack = str(sys.exc_info())
                                print ("Write Failed!" + ack)
                                return ack
            else:
                debug.info("Unable to set select!")
                raise Exception('Unable to set select.')
        except:
            ack = str(sys.exc_info())
            print ("Write Failed!" + ack)
            return ack



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

def keyboardInterruptHandler(signal, frame):
    debug.info("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


class socketQThread(threading.Thread):
    def __init__(self, socketQueue, ip):
        super(socketQThread, self).__init__()

        self.socketQueue = socketQueue
        self.ip = ip

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while(True):
            try:
                self.socket.connect((self.ip,4695))
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

signal.signal(signal.SIGINT, keyboardInterruptHandler)


if __name__ =="__main__":
    setproctitle.setproctitle("RFID_UHF_SERVER")

    if user=="root":
        time.sleep(60)
        GranthaQ = Queue()
        SocketQ = Queue()
        GS = Process(target=GranthaServer, args=(GranthaQ,SocketQ,))
        SS = Process(target=SocketServer, args=(GranthaQ,SocketQ,))
        GS.start()
        SS.start()

        GS.join()
        SS.join()
    else:
        debug.info("No Permission, Run as Root")
        exit(0)

