#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
import subprocess
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtCore import *
import MySQLdb
import MySQLdb.cursors
import argparse
import zmq
import Utils_Gui

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")
databasePath = os.path.join(progPath, "GUI")
sys.path.append(uiFilePath)
sys.path.append(imgFilePath)
sys.path.append(databasePath)

import dbGrantha
import debug

parser = argparse.ArgumentParser(description="Utility to preview image of PiCamera")
parser.add_argument('filename', metavar='N', type=str, help='file name')
args = parser.parse_args()

context = zmq.Context()

class captureThread(QtCore.QThread):
    # waiting = pyqtSignal()
    ackReceived = QtCore.pyqtSignal(str)

    def __init__(self, slNo, parent):
        super(captureThread, self).__init__(parent)
        self.slNo = slNo

    def run(self):
        # self.waiting.emit()

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
            debug.info("connected.")
        except:
            debug.info(str(sys.exc_info()))
        self.socket.send_multipart(["CAPTURE",self.slNo])

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        try:
            ack = self.socket.recv()
            debug.info(ack)
            self.ackReceived.emit(ack)
        except:
            debug.info(str(sys.exc_info()))

        self.socket.close()

        if (self.socket.closed == True):
            debug.info("Capture Socket closed.")

def captureImage():
    i = args.filename
    cT = captureThread(i, app)
    # cT.waiting.connect(self.openPlaceTagMessage)
    cT.ackReceived.connect(closeWindow)
    cT.start()

def closeWindow():
    app.closeAllWindows()
    message = Utils_Gui.TimerMessageBox(1,"Captured")
    message.exec_()

app = QtWidgets.QApplication(sys.argv)

ui = uic.loadUi(os.path.join(uiFilePath,"Pi_Camera_Preview.ui"))
ui.captureButton.clicked.connect(captureImage)

ui.show()
sys.exit(app.exec_())
