#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt
import zmq
import database


filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")
rfidPath = os .path.join(progPath, "RFID")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)
sys.path.append(rfidPath)

import debug



class startReadingThread(QThread):
    # waiting = pyqtSignal()
    def __init__(self, to, parent):
        super(startReadingThread, self).__init__(parent)
        self.to =to

    def run(self):
        # self.waiting.emit()
        self.context = zmq.Context()
        print("connecting to rfid Scanner Server...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")

        self.socket.send("FIND_TAG")

        rep = self.socket.recv()

        if (rep == "GIVE_TIMEOUT"):
            self.socket.send(self.to)

        ack = self.socket.recv()

        if (ack == "ackPass"):
            print ack
        else:
            pass


class searchTagThread(QThread):
    waiting = pyqtSignal()
    slNoReceived = pyqtSignal(str)
    wrongslNoRecieved = pyqtSignal(str)

    def __init__(self, slNoToSearch, parent):
        super(searchTagThread, self).__init__(parent)
        self.slNoToSearch = slNoToSearch

    def run(self):
        self.waiting.emit()

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://192.168.1.39:4691")

        while True:
            slNo = self.socket.recv()
            self.socket.send("received")
            debug.info (str(slNo) +" : " +str(self.slNoToSearch))

            if (str(slNo) == str(self.slNoToSearch)):
                # print slNo
                self.slNoReceived.emit(slNo)

            if (slNo == "FUCKINGDONE"):
                print "exiting"
                self.socket.close()
                self.context.term()
                break


def showWaiting(uiObj):
    uiObj.msgLabel.setText("Scanning Tags...s")

def showFoundMsg(slNo, uiObj):
    uiObj.msgLabel.setText("TagFound "+ str(slNo))

def wrongTagMsg(slNo, uiObj):
    uiObj.msgLabel.setText("wrongTag " + str(slNo))

def enableButtons(uiObj):
    uiObj.searchButton.setEnabled(True)
    ui.closeEvent = closeEventEnable

def closeEventDisable(event):
    debug.info("QUITTING DISABLED")
    event.ignore()

def closeEventEnable(event):
    debug.debug("QUITTING ENABLED")
    event.accept()


def startThreads():
    slNoToSearch = ui.comboBox.currentText()
    timeout = str(ui.spinBox.value())

    ui.searchButton.setEnabled(False)
    ui.closeEvent = closeEventDisable

    srT = startReadingThread(timeout, app)
    stT = searchTagThread(slNoToSearch, app)
    stT.waiting.connect(lambda  uiObj=ui: showWaiting(uiObj))
    stT.slNoReceived.connect(lambda slNo, uiObj=ui: showFoundMsg(slNo, uiObj))
    stT.wrongslNoRecieved.connect(lambda slNo, uiObj=ui: wrongTagMsg(slNo, uiObj))
    stT.finished.connect(lambda uiObj=ui: enableButtons(uiObj))

    srT.start()
    stT.start()

app = QApplication(sys.argv)

ui = uic.loadUi(os.path.join(uiFilePath, "Find_Tag.ui"))
ui.show()

db = database.DataBase()

sn = db.listOfSerialNo()
SN = [x['serial_no'] for x in sn]
ui.comboBox.addItems(SN)

ui.searchButton.clicked.connect(startThreads)

ui.setWindowIcon(QIcon(os.path.join(imgFilePath, "granthaLogo.png")))
ui.setWindowTitle("Find Tag")

sys.exit(app.exec_())

