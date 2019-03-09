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


def GranthaServer(granthaQueue, socketQueue):
    print ("GranthaServer Started.")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.1.183:4689")

    while True:
        msgFrmCli = socket.recv()

        if (msgFrmCli == "READ"):
            granthaQueue.put("READ_SINGLE")
            msg = socketQueue.get()
            print msg
            try:
                if (msg=="NO_CARD"):
                    print "1 No Card Detected!"
                    socket.send("NO CARD")
                    raise (ValueError)
                else:
                    socket.send(msg)
            except:
                print ("Trying Again!")


def SocketServer(granthaQueue, socketQueue):
    print ("SocketServer Started.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    server_address = ("192.168.1.183", 80)
    sock.bind(server_address)
    sock.listen(1)

    connection, client_address = sock.accept()
    print ("connection from: {}".format(client_address))

    while True:
        msg = granthaQueue.get()
        if (msg == "READ_SINGLE"):
            tagId = readSingle(connection)
            socketQueue.put(tagId)

def readSingle(connection):
    readStr = 'BB00220000227E'
    read = readStr.decode('hex')
    connection.send(read)

    time.sleep(1)

    data = connection.recv(10240)
    dataHex = bytes_to_hex(data)
    dataDict = readVerifier(dataHex)

    if not dataDict:
        print "2 No Cards Detected!"
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
        # print (nearRestEpc)
        tagId = nearRestEpc[16:24]
        return (tagId)



if __name__ =="__main__":
    setproctitle.setproctitle("RFIDUHFSERVER")

    Q = Queue()
    GS = Process(target=GranthaServer, args=(Q,Q,))
    SS = Process(target=SocketServer, args=(Q,Q,))
    GS.start()
    SS.start()

    GS.join()
    SS.join()



























# class Server:
#     def __init__(self):
#         self.context = zmq.Context()
#         self.socket = self.context.socket(zmq.REP)
#         self.socket.bind("tcp://192.168.1.183:4689")
#
#         while True:
#             msgFrmCli = self.socket.recv()
#             print "Message from Client: " + msgFrmCli
#
#             # if (msgFrmCli == "WRITE"):
#             #     self.WRITE()
#
#             if (msgFrmCli == "READ"):
#                 self.READ()
#
#             if (msgFrmCli == "READ_MULTI"):
#                 self.READ_MULTI()
#
#             # if (msgFrmCli == "WRITE_TAG"):
#             #     self.WRITE_TAG()
#             #
#             # if (msgFrmCli == "FIND_TAG"):
#             #     self.FIND_TAG()
#
#
#     # def WRITE(self):
#     #     print "Sending Reply"
#     #     self.socket.send("INPUT")
#     #
#     #     serialNo = self.socket.recv()
#     #     print "Message from Client: " + serialNo
#     #     print("Now place your tag to write")
#     #
#     #     while True:
#     #         try:
#     #             reader = SimpleMFRC522.SimpleMFRC522()
#     #             msg = reader.write(serialNo)
#     #             if (msg):
#     #                 print("Written")
#     #             GPIO.cleanup()
#     #             break
#     #
#     #         except:
#     #             print("trying to screw harder : " + str(sys.exc_info()))
#     #             GPIO.cleanup()
#     #
#     #     self.socket.send("Data Written to Tag")
#
#
#     def READ(self):
#         print "Now place your tag to read"
#         try:
#             # queue.put("READ")
#             reader = SimpleMFRC522.SimpleMFRC522()
#             id, text = reader.read()
#             slNo = text.strip()
#             self.socket.send(slNo)
#             print "message sent"
#             GPIO.cleanup()
#
#         except:
#             print("trying hard : " + str(sys.exc_info()))
#             # GPIO.cleanup()
#
#
#     # def WRITE_TAG(self):
#     #     print "Sending Reply"
#     #     self.socket.send("INPUT")
#     #
#     #     serialNo = self.socket.recv()
#     #     print "Message from Client: " + serialNo
#     #     print("Now place your tag to write")
#     #
#     #     while True:
#     #         try:
#     #             reader = SimpleMFRC522.SimpleMFRC522()
#     #             msg = reader.write(serialNo)
#     #             if (msg):
#     #                 print("Written")
#     #             GPIO.cleanup()
#     #             break
#     #
#     #         except:
#     #             print("trying to screw harder : " + str(sys.exc_info()))
#     #             GPIO.cleanup()
#     #
#     #     self.socket.send("Data Written to Tag")
#
#
#     def READ_MULTI(self):
#         try:
#             self.socket.send("GIVE_TIMEOUT")
#
#             timeout = self.socket.recv()
#             subprocess.Popen(["python", "readMultiple02.py", "%s" %(timeout)])
#
#             self.socket.send("ackPass")
#             print "message sent"
#
#         except:
#             print("trying hard : " + str(sys.exc_info()))
#             self.socket.send("ackFail")
#             print("Failed to run Multi reader")
#
#
#     # def FIND_TAG(self):
#     #     try:
#     #         self.socket.send("GIVE_TIMEOUT")
#     #
#     #         timeout = self.socket.recv()
#     #         subprocess.Popen(["python", "findTag.py", "%s" %(timeout)])
#     #
#     #         self.socket.send("ackPass")
#     #         print "message sent"
#     #
#     #     except:
#     #         print("trying hard : " + str(sys.exc_info()))
#     #         self.socket.send("ackFail")
#     #         print("Failed to run Multi reader")
#
#
#
#
# if __name__ == "__main__":
#     Server()
#
#
#
#
#
#
#
#
#
# class ReaderWiter():
#     def __init__(self):
#
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         hostname = socket.gethostname()
#         ip = socket.gethostbyname(hostname)
#         server_address = (ip, 80)
#         self.sock.bind(server_address)
#         self.sock.listen(1)
#
#         self.connection, client_address = self.sock.accept()
#
#
#     def closeConnection(self):
#
#         self.connection.close()
#
#         print ("Connection closed.")
#
#
#     def readSingle(self):
#         readStr = 'BB00220000227E'
#         read = readStr.decode('hex')
#         self.connection.send(read)
#
#         time.sleep(1)
#
#         data = self.connection.recv(10240)
#         dataHex = bytes_to_hex(data)
#         print dataHex
#         dataDict = readVerifier(dataHex)
#         print (dataDict)
#
#         if not dataDict:
#             print "No Cards Detected!"
#             self.ui.textEdit01.setTextColor(self.redColor)
#             self.ui.textEdit01.append("NO CARDS DETECTED!")
#         else:
#             nearestRssi = None
#             nearRestEpc = None
#             for x in dataDict:
#                 if(not nearestRssi):
#                     nearestRssi = int(dataDict[x]["RSSI"],16)
#                     nearRestEpc = x
#                 else:
#                     if(int(dataDict[x]["RSSI"],16) >= nearestRssi):
#                         nearestRssi = int(dataDict[x]["RSSI"],16)
#                         nearRestEpc = x
#
#                 # print type(dataDict)
#
#             print (nearRestEpc)
#
#
#
#     def readMulti(self):
#
#
#         pollingTime = 10000
#         readStr = severalTimesPollingCommandGen(pollingTime)
#         # print readStr
#         read = readStr.decode('hex')
#
#         global threads
#         rT = recieveThread(self.connection, read, app)
#         rT.dataReceived.connect(self.readMultiOutput)
#         threads.append(rT)
#         rT.start()
#
#     def readMultiOutput(self, dataHex):
#
#
#         dataDict = readVerifier(dataHex)
#         # print (dataDict)
#
#         if not dataDict:
#             print "No Cards Detected!"
#
#         else:
#             for x in dataDict:
#                 print (x)
#
#
#     def stopRead(self):
#         global threads
#         if threads:
#             for runningThread in threads:
#                 runningThread.exit()
#
#
#         stopStr = 'BB00280000287E'
#         stop = stopStr.decode('hex')
#         while True:
#             try:
#                 self.connection.send(stop)
#                 # time.sleep(0.2)
#                 data = self.connection.recv(4096)
#                 dataHex = bytes_to_hex(data)
#
#                 if dataHex == "BB01280001002A7E":
#                     print ("Reading stopped.")
#
#                     break
#                 else:
#                     raise ValueError('Unable to stop')
#             except:
#                 print ("Trying Again!" + str(sys.exc_info()))
#
#
#
#
#     def setSelect(self):
#
#
#         # print (mask)
#         selParam = '000C001301000000206000'+mask
#         # print (selParam)
#         selParamChecksum = checksumCalculator(selParam)
#
#         selParamCommandHex = 'BB'+selParam+selParamChecksum+'7E'
#
#         selParamCommand = selParamCommandHex.decode('hex')
#         while True:
#             try:
#                 self.connection.send(selParamCommand)
#
#                 time.sleep(1)
#
#                 data = self.connection.recv(10240)
#                 dataHex = bytes_to_hex(data)
#                 print (dataHex)
#
#                 if dataHex == 'BB010C0001000E7E':
#                     print ("set select successful.")
#
#                     break
#                 else:
#
#                     raise ValueError('Unable to set select.')
#
#             except:
#                 print ("Trying Again!" + str(sys.exc_info()))
#
#     def readEpc(self):
#
#         readEpcStr = 'BB003900090000000001000000084B7E'
#         readEpc = readEpcStr.decode('hex')
#         self.connection.send(readEpc)
#
#         time.sleep(1)
#
#         data = self.connection.recv(10240)
#         dataHex = bytes_to_hex(data)
#         # print (dataHex)
#
#         dataDict = readEpcVerifier(dataHex)
#         print (dataDict)
#
#         if not dataDict:
#             print "No Cards Detected!"
#
#         else:
#             for x in dataDict:
#                 print (x)
#
#
#
#
#     def writeEpc(self):
#         # print ("writeEpc!")
#
#         data = self.ui.dataLine.text()
#         writeEpcStr = '00490019000000000100000008'+data
#
#         writeEpcChecksum = checksumCalculator(writeEpcStr)
#
#         writeEpcCommandHex = 'BB'+writeEpcStr+writeEpcChecksum+'7E'
#         writeEpcCommand = writeEpcCommandHex.decode('hex')
#         while True:
#             try:
#                 self.connection.send(writeEpcCommand)
#
#                 time.sleep(0.5)
#
#                 data = self.connection.recv(1024)
#                 dataHex = bytes_to_hex(data)
#
#                 print (dataHex)
#                 Type = dataHex[2:4]
#
#                 Command = dataHex[4:6]
#
#                 if Type == '01' and Command == '49':
#                     print ("Write Successful.")
#
#                     break
#                 else:
#                     raise ValueError('unable to write!')
#
#             except:
#                 print ("Trying Again!" + str(sys.exc_info()))
#
#
#
#
#
# class recieveThread(QThread):
#     # starting = pyqtSignal()
#     dataReceived = pyqtSignal(str)
#
#     def __init__(self, connection, readStr, parent):
#         super(recieveThread, self).__init__(parent)
#         self.connection = connection
#         self.readStr = readStr
#         self.stop = False
#
#     def exit(self):
#         self.stop = True
#
#     def run(self):
#         # self.starting.emit()
#         while True:
#             if (self.stop == False):
#                 self.connection.send(self.readStr)
#
#                 data = self.connection.recv(1024)
#                 dataHex = bytes_to_hex(data)
#                 self.dataReceived.emit(dataHex)
#                 time.sleep(0.01)
#             else:
#                 break
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ReaderWiter()
#     sys.exit(app.exec_())


