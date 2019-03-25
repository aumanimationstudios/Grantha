#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
import socket
import time
import collections
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QThread,pyqtSignal
from utils_uhf import *

threads = []

class ReaderWiter():
    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("initialized")

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        server_address = (ip, 80)
        # self.ui.textEdit01.append('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)

        self.sock.listen(1)

        self.ui = uic.loadUi("rfidReaderWriter.ui")

        self.ui.openConnectionButton.pressed.connect(self.openConnection)
        self.ui.closeConnectionButton.pressed.connect(self.closeConnection)
        self.ui.readSingleButton.pressed.connect(self.readSingle)
        self.ui.readMultiButton.pressed.connect(self.readMulti)
        self.ui.stopReadButton.pressed.connect(self.stopRead)
        self.ui.closeConnectionButton.setEnabled(False)
        self.ui.readSingleButton.setEnabled(False)
        self.ui.readMultiButton.setEnabled(False)
        self.ui.stopReadButton.setEnabled(False)
        self.ui.maskLine.setEnabled(False)
        self.ui.dataLine.setEnabled(False)
        self.ui.setSelectButton.setEnabled(False)
        self.ui.setSelectButton.pressed.connect(self.setSelect)
        self.ui.readButton.setEnabled(False)
        self.ui.writeButton.setEnabled(False)
        self.ui.readButton.pressed.connect(self.readEpc)
        self.ui.writeButton.pressed.connect(self.writeEpc)
        self.ui.cancelButton.pressed.connect(self.cancel)


        self.ui.clearButton.pressed.connect(self.clearText)


        self.ui.setWindowTitle("Rfid Reader Writer")
        self.ui.show()

        self.redColor = QColor(255, 0, 0)
        self.greenColor = QColor(0, 255, 0)
        self.blueColor = QColor(0, 0, 255)

    def openConnection(self):
        self.ui.textEdit01.setTextColor(self.greenColor)
        self.ui.textEdit01.append('waiting for a connection')
        self.connection, client_address = self.sock.accept()

        self.ui.textEdit01.append('connection from {}'.format(client_address))
        print ("Connection open.")
        self.ui.openConnectionButton.setEnabled(False)
        self.ui.openConnectionButton.setText("Connection Open")
        self.ui.closeConnectionButton.setEnabled(True)
        self.ui.readSingleButton.setEnabled(True)
        self.ui.readMultiButton.setEnabled(True)
        self.ui.stopReadButton.setEnabled(True)

    def closeConnection(self):

        self.connection.close()
        self.ui.textEdit01.setTextColor(self.redColor)
        self.ui.textEdit01.append("Connection closed.")
        print ("Connection closed.")
        self.ui.openConnectionButton.setEnabled(True)
        self.ui.openConnectionButton.setText("Open Connection")
        self.ui.closeConnectionButton.setEnabled(False)
        self.ui.readSingleButton.setEnabled(False)
        self.ui.readMultiButton.setEnabled(False)
        self.ui.stopReadButton.setEnabled(False)

    def readSingle(self):
        readStr = 'BB00220000227E'
        read = readStr.decode('hex')
        self.connection.send(read)

        time.sleep(1)

        data = self.connection.recv(10240)
        dataHex = bytes_to_hex(data)
        print dataHex
        dataDict = readVerifier(dataHex)
        print (dataDict)

        if not dataDict:
            print "No Cards Detected!"
            self.ui.textEdit01.setTextColor(self.redColor)
            self.ui.textEdit01.append("NO CARDS DETECTED!")
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

                # print type(dataDict)
            self.ui.textEdit01.setTextColor(self.blueColor)
            self.ui.textEdit01.append(nearRestEpc)
            self.ui.maskLine.setEnabled(True)
            self.ui.maskLine.setText(nearRestEpc)
            self.ui.setSelectButton.setEnabled(True)

        #     RSSI = x[8:10]
        #     print (RSSI)


        # print (dataHex)
        # EPC = dataHex[16:40]
        # if "300833B2DDD901" in EPC:
        #     self.ui.textEdit01.append(EPC)
        #     self.ui.maskLine.setEnabled(True)
        #     self.ui.maskLine.setText(EPC)
        #     self.ui.setSelectButton.setEnabled(True)
        #
        # else:
        #     self.ui.textEdit01.append("NO CARD DETECTED!")

    def readMulti(self):

        self.ui.maskLine.clear()
        self.ui.maskLine.setEnabled(False)
        self.ui.setSelectButton.setEnabled(False)
        self.ui.dataLine.setEnabled(False)
        self.ui.readButton.setEnabled(False)
        self.ui.writeButton.setEnabled(False)

        pollingTime = 10000
        readStr = severalTimesPollingCommandGen(pollingTime)
        # print readStr
        read = readStr.decode('hex')

        global threads
        rT = recieveThread(self.connection, read, app)
        rT.dataReceived.connect(self.readMultiOutput)
        print type(rT)
        threads.append(rT)
        rT.start()

    def readMultiOutput(self, dataHex):
        # print dataHex
        # dataHex = bytes_to_hex(data)

        dataDict = readVerifier(dataHex)
        # print (dataDict)

        if not dataDict:
            print "No Cards Detected!"
            # self.ui.textEdit01.setTextColor(self.redColor)
            # self.ui.textEdit01.append("NO CARDS DETECTED!")
        else:
            for x in dataDict:
                print (x)
                self.ui.textEdit01.setTextColor(self.blueColor)
                self.ui.textEdit01.append(x)

        # self.connection.send(read)
        #
        # time.sleep(1)
        #
        # data = self.connection.recv(1024)
        # dataHex = bytes_to_hex(data)
        #
        # dataDict = readVerifier(dataHex)
        # print (dataDict)
        #
        # if not dataDict:
        #     print "No Cards Detected!"
        #     self.ui.textEdit01.setTextColor(self.redColor)
        #     self.ui.textEdit01.append("NO CARDS DETECTED!")
        # else:
        #     for x in dataDict:
        #         self.ui.textEdit01.setTextColor(self.blueColor)
        #         self.ui.textEdit01.append(x)

        # dataArray = dataHex.split("7EBB")
        #
        # cleanDataArray = []
        #
        # for x in dataArray:
        #     if x.startswith("BB"):
        #         y = x[2:]
        #         cleanDataArray.append(y)
        #
        #     elif x.endswith("7E"):
        #         z = x[:-2]
        #         cleanDataArray.append(z)
        #
        #     else:
        #         cleanDataArray.append(x)
        #
        # dataDict = collections.OrderedDict()
        # # print (cleanDataArray)
        #
        # for x in cleanDataArray:
        #     Type = x[0:2]
        #
        #     Command = x[2:4]
        #
        #     if len(x) == 44:
        #         if Type == '02' and Command == '22':
        #             EPC = x[14:38]
        #             dataDict[EPC] = 1
        #             # print (dataDict)
        #
        #         elif Type == '01' and Command == 'FF':
        #             print "No Cards Detected!"
        #             self.ui.textEdit01.setTextColor(self.redColor)
        #             self.ui.textEdit01.append("NO CARDS DETECTED!")
        #
        # if not dataDict:
        #     print "No Cards Detected!"
        #     self.ui.textEdit01.setTextColor(self.redColor)
        #     self.ui.textEdit01.append("NO CARDS DETECTED!")
        #
        # else:
        #     for x in dataDict:
        #         print (x + "\n")
        #         self.ui.textEdit01.setTextColor(self.blueColor)
        #         self.ui.textEdit01.append(x)


    def stopRead(self):
        global threads
        if threads:
            print (threads)
            for runningThread in threads:
                runningThread.exitThread()


        stopStr = 'BB00280000287E'
        stop = stopStr.decode('hex')
        while True:
            try:
                self.connection.send(stop)
                # time.sleep(0.2)
                data = self.connection.recv(4096)
                dataHex = bytes_to_hex(data)

                if dataHex == "BB01280001002A7E":
                    print ("Reading stopped.")
                    self.ui.textEdit01.setTextColor(self.greenColor)
                    self.ui.textEdit01.append("READING STOPPED!")
                    break
                else:
                    raise ValueError('Unable to stop')
            except:
                print ("Trying Again!" + str(sys.exc_info()))
                # self.ui.textEdit01.append("TRYING AGAIN!")
        # print(dataHex)


    def clearText(self):
        self.ui.textEdit01.clear()

    def setSelect(self):

        mask = self.ui.maskLine.text()
        # print (mask)
        selParam = '000C001301000000206000'+mask
        # print (selParam)
        selParamChecksum = checksumCalculator(selParam)

        selParamCommandHex = 'BB'+selParam+selParamChecksum+'7E'

        selParamCommand = selParamCommandHex.decode('hex')
        while True:
            try:
                self.connection.send(selParamCommand)

                time.sleep(1)

                data = self.connection.recv(10240)
                dataHex = bytes_to_hex(data)
                print (dataHex)

                if dataHex == 'BB010C0001000E7E':
                    print ("set select successful.")
                    self.ui.textEdit02.setTextColor(self.greenColor)
                    self.ui.textEdit02.append("SET SELECT SUCCESSFUL.")
                    self.ui.dataLine.setEnabled(True)
                    self.ui.readButton.setEnabled(True)
                    self.ui.writeButton.setEnabled(True)
                    break
                else:
                    # self.ui.textEdit02.setTextColor(self.redColor)
                    # print ("Try Again!")
                    # self.ui.textEdit02.append("TRY AGAIN!")
                    raise ValueError('Unable to set select.')

            except:
                print ("Trying Again!" + str(sys.exc_info()))
                # self.ui.textEdit02.append("TRYING AGAIN!")

    def readEpc(self):

        readEpcStr = 'BB003900090000000001000000084B7E'
        readEpc = readEpcStr.decode('hex')
        self.connection.send(readEpc)

        time.sleep(1)

        data = self.connection.recv(10240)
        dataHex = bytes_to_hex(data)
        # print (dataHex)

        dataDict = readEpcVerifier(dataHex)
        print (dataDict)

        if not dataDict:
            print "No Cards Detected!"
            self.ui.textEdit02.setTextColor(self.redColor)
            self.ui.textEdit02.append("NO CARDS DETECTED!")
        else:
            for x in dataDict:
                print (x)
                self.ui.textEdit02.setTextColor(self.blueColor)
                self.ui.textEdit02.append(x)
                self.ui.dataLine.setText(x)

        # print (dataHex)
        # EPC = dataHex[40:72]
        # if len(dataHex) == 76:
        #     print ("read success.")
        #     self.ui.textEdit02.setTextColor(self.blueColor)
        #     self.ui.textEdit02.append(EPC)
        #     self.ui.dataLine.setText(EPC)
        # else:
        #     print ("read failed.")

    def writeEpc(self):
        # print ("writeEpc!")

        data = self.ui.dataLine.text()
        writeEpcStr = '00490019000000000100000008'+data

        writeEpcChecksum = checksumCalculator(writeEpcStr)

        writeEpcCommandHex = 'BB'+writeEpcStr+writeEpcChecksum+'7E'
        writeEpcCommand = writeEpcCommandHex.decode('hex')
        while True:
            try:
                self.connection.send(writeEpcCommand)

                time.sleep(0.5)

                data = self.connection.recv(1024)
                dataHex = bytes_to_hex(data)

                print (dataHex)
                Type = dataHex[2:4]

                Command = dataHex[4:6]

                if Type == '01' and Command == '49':
                    print ("Write Successful.")
                    self.ui.textEdit02.setTextColor(self.greenColor)
                    self.ui.textEdit02.append("WRITE SUCCESSFUL.")
                    break
                else:
                    raise ValueError('unable to write!')

            except:
                print ("Trying Again!" + str(sys.exc_info()))
                # self.ui.textEdit02.append("TRYING AGAIN!")

    def cancel(self):
        self.ui.dataLine.clear()



class recieveThread(QThread):
    # starting = pyqtSignal()
    dataReceived = pyqtSignal(str)

    def __init__(self, connection, readStr, parent):
        super(recieveThread, self).__init__(parent)
        self.connection = connection
        self.readStr = readStr
        self.stop = False
        self.connection.send(self.readStr)

    def exitThread(self):
        self.stop = True

    def run(self):
        # self.starting.emit()
        while True:
            if (self.stop == False):

                data = self.connection.recv(1024)
                dataHex = bytes_to_hex(data)
                self.dataReceived.emit(dataHex)
                time.sleep(0.01)
            else:
                break








if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReaderWiter()
    sys.exit(app.exec_())





