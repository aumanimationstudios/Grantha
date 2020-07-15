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
from collections import OrderedDict
import argparse

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

parser = argparse.ArgumentParser(description="Utility to repair items")
parser.add_argument("-i","--item",dest="item",help="name of item")
args = parser.parse_args()

class repairWidget():

    def __init__(self):

        self.loadVars()
        self.ui = uic.loadUi(os.path.join(uiDir,'Repair.ui'))

        self.ui.itemBox.currentIndexChanged.connect(self.loadLocation)
        self.ui.submissionDateButton.clicked.connect(self.showSubmissionCal)
        self.ui.expectedDateButton.clicked.connect(self.showExpectedCal)
        self.ui.submissionNoneButton.clicked.connect(self.submissionNone)
        self.ui.expectedNoneButton.clicked.connect(self.expectedNone)
        self.ui.cancelButton.clicked.connect(self.closeEvent)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.confirmation)
        self.load()

        if args.item:
            self.ui.itemBox.setEditText(str(args.item))
            self.loadLocation()


        self.ui.setWindowTitle('Repair')
        self.ui.submissionDateButton.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.expectedDateButton.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))
        self.ui.show()

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
        # locs = [x['location'] for x in LOCS]
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
        self.ui.locationBox.setText(loc)
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


    def confirmation(self):
        confirm = QtWidgets.QMessageBox()
        confirm.setIcon(QtWidgets.QMessageBox.Question)
        confirm.setWindowTitle("Confirmation")
        confirm.setInformativeText("Are you sure you want to save?")
        confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        cnfrm = confirm.exec_()
        if cnfrm == QtWidgets.QMessageBox.Ok:
            self.repair()
        else:
            pass

    def repair(self):
        userInput = OrderedDict()

        userInput["item"] = str(self.ui.itemBox.currentText().strip())
        userInput["location"] = str(self.ui.locationBox.text().strip())
        userInput["symptoms"] = str(self.ui.symptomsBox.text().strip())
        userInput["submission_date"] = str(self.ui.submissionDateBox.text().strip())
        userInput["expected_completion_date"] = str(self.ui.expectedDateBox.text().strip())
        userInput["user"] = os.environ['USER']

        keys = []
        values = []
        for key in userInput.keys():
            keys.append(key)
            values.append(userInput[key])

        item = str(self.ui.itemBox.currentText().strip())
        # loc = str(self.ui.locationBox.text().strip())
        # newLoc = "REPAIR"
        queryRepair = ""
        if item in slNos:
            queryRepair = "UPDATE ITEMS SET location = 'REPAIR' WHERE serial_no = '%s'" % (item)
        if item in blues:
            queryRepair = "UPDATE LOCATION SET parent_location = 'REPAIR' WHERE location = '%s'" % (item)

        queryRepairLog = "INSERT INTO repair_log (" + ','.join(keys) + ") VALUES %r" % (tuple(values),)
        debug.info(queryRepairLog)

        addRepair = db.execute(queryRepair)
        if addRepair == 1:
            addRepairLog = db.execute(queryRepairLog)
            if (addRepairLog == 1):
                logInput = OrderedDict()
                if item in slNos:
                    logInput["date"] = time.strftime('%Y-%m-%d %H:%M:%S')
                    logInput["serial_no"] = item
                    logInput["user"] = userInput["user"]
                    logInput["action"] = 'Update: location="REPAIR" '

                    logValues = []
                    for key in logInput.keys():
                        logValues.append(logInput[key])
                    columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE\
                                   TABLE_NAME = 'add_update_log' AND COLUMN_NAME NOT IN ('no')"
                    column = db.execute(columnQuery, dictionary=True)
                    logColumn = [x['COLUMN_NAME'] for x in column]
                    LogQuery = "INSERT INTO add_update_log (" + ','.join(logColumn) + ")\
                                VALUES %r" % (tuple(logValues),)
                    logAddUpdate =db.execute(LogQuery)
                    if (logAddUpdate == 1):
                        messageBox("item moved to repair")
                    else:
                        messageBox("Logging Failed")

                if item in blues:
                    logInput["date"] = time.strftime('%Y-%m-%d %H:%M:%S')
                    logInput["location"] = item
                    logInput["old_parent_location"] = userInput["location"]
                    logInput["new_parent_location"] = "REPAIR"
                    logInput["user"] = userInput["user"]
                    values = []
                    for key in logInput.keys():
                        values.append(logInput[key])
                    columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE \
                                   TABLE_NAME = 'location_update_log' AND COLUMN_NAME NOT IN ('no')"
                    column = db.execute(columnQuery, dictionary=True)
                    logColumn = [x['COLUMN_NAME'] for x in column]
                    updateLogQuery = "INSERT INTO location_update_log (" + ','.join(logColumn) + ")\
                                      VALUES %r" % (tuple(values),)
                    logUpdated = db.execute(updateLogQuery)
                    if (logUpdated == 1):
                        messageBox("item moved to repair")
                    else:
                        messageBox("Logging Failed")
            else:
                messageBox("addRepairLog failed")
        else:
            messageBox("addRepair Failed")


    def clearAll(self):
        self.ui.itemBox.setCurrentText(" ")
        self.ui.locationBox.clear()
        self.ui.symptomsBox.clear()
        self.submissionNone()
        self.expectedNone()

    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    setproctitle.setproctitle("REPAIR")
    app = QtWidgets.QApplication(sys.argv)
    window = repairWidget()
    sys.exit(app.exec_())
