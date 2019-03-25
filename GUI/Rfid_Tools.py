#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
import database
import string
import random
from collections import OrderedDict
import zmq
import debug

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

context = zmq.Context()

class addWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Rfid_Tools.ui'))

        self.db = database.DataBase()

        # self.ui.readButton.clicked.connect(readRfidTag)



        self.ui.setWindowTitle('Rfid Tools')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))
        self.ui.show()


    # def readRfidTag(self):





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = addWidget()
    sys.exit(app.exec_())




