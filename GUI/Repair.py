#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os
import sys
import psutil
from PyQt5 import QtGui, QtWidgets, uic, QtCore, QtSvg
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
import dbGrantha
import zmq
import socket
import debug
import subprocess
from Utils_Gui import *
import time
import setproctitle
import tempfile
import xml.dom.minidom
import glob
import datetime
import json

filePath = os.path.abspath(__file__)
# debug.info(filePath)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")
fileDir = os.path.join(projDir, "GUI")

sys.path.append(uiDir)
sys.path.append(imageDir)
sys.path.append(fileDir)

db = dbGrantha.dbGrantha()

slNos = []
blues = []

class repairWidget():

    def __init__(self):

        self.loadVars()
        self.ui = uic.loadUi(os.path.join(uiDir,'Repair.ui'))

        self.ui.itemBox.currentIndexChanged.connect(self.loadLocation)
        self.ui.submissionDateButton.clicked.connect(self.showSubmissionCal)
        self.ui.expectedDateButton.clicked.connect(self.showExpectedCal)
        self.ui.submissionNoneButton.clicked.connect(self.submissionNone)
        self.ui.expectedNoneButton.clicked.connect(self.expectedNone)


        self.ui.setWindowTitle('Repair')
        self.ui.submissionDateButton.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.expectedDateButton.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))
        self.ui.show()
        self.load()

        try:
            theme = os.environ['GRANTHA_THEME']
            # debug.info(theme)
            setStyleSheet(self.ui, theme)
        except:
            pass

    def loadVars(self):
        global slNos
        global blues

        getSN = "SELECT * FROM SERIAL_NO"
        sn = db.execute(getSN, dictionary=True)
        slNos = [x['serial_no'] for x in sn]
        slNos.sort()

        getLOC = "SELECT * FROM LOCATION"
        LOCS = db.execute(getLOC, dictionary=True)
        locs = [x['location'] for x in LOCS]
        pLocs = [x['parent_location'] for x in LOCS]

        for pl in pLocs:
            if pl != None:
                bloc = next(x['location'] for x in LOCS if x['parent_location'] == pl)
                blues.append(bloc)
        blues = list(set(blues))
        blues.sort()

    def load(self):
        # debug.info(slNos)
        # debug.info(blues)

        self.ui.itemBox.addItems(slNos)
        self.ui.itemBox.addItems(blues)

        currDate = time.strftime('%Y-%m-%d')
        self.ui.submissionDateBox.setText(currDate)

    def loadLocation(self):
        item = str(self.ui.itemBox.currentText().strip())
        getLoc = ""
        loc = ""
        if item in slNos:
            getLoc = "SELECT location FROM ITEMS WHERE serial_no='%s' " % (item)
            loc = db.execute(getLoc, dictionary=True)[0]['location']

        if item in blues:
            getLoc = "SELECT parent_location FROM LOCATION WHERE location='%s' " % (item)
            loc = db.execute(getLoc, dictionary=True)[0]['parent_location']
        # loc = ""
        # try:
        #     loc = db.execute(getLoc, dictionary=True)[0]['location']
        # except:
        #     pass
        # loc = loc[0]
        debug.info(loc)

    def showSubmissionCal(self):
        self.cal = QtWidgets.QCalendarWidget()
        self.cal.clicked.connect(self.updateSubmissionDate)
        self.cal.show()

    def showExpectedCal(self):
        self.cal = QtWidgets.QCalendarWidget()
        self.cal.clicked.connect(self.updateExpectedDate)
        self.cal.show()

    def updateSubmissionDate(self):
        date = self.cal.selectedDate().toString(QtCore.Qt.ISODate)
        self.ui.submissionDateBox.setText(date)
        self.cal.close()

    def updateExpectedDate(self):
        date = self.cal.selectedDate().toString(QtCore.Qt.ISODate)
        self.ui.expectedDateBox.setText(date)
        self.cal.close()

    def submissionNone(self):
        self.ui.submissionDateBox.setText("0000-00-00")

    def expectedNone(self):
        self.ui.expectedDateBox.setText("0000-00-00")

if __name__ == '__main__':
    setproctitle.setproctitle("REPAIR")
    app = QtWidgets.QApplication(sys.argv)
    window = repairWidget()
    sys.exit(app.exec_())
