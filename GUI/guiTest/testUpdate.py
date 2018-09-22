#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database
from collections import OrderedDict
import time

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-3])
uiFilePath = os.path.join(progPath,"GUI","guiTest","uiFiles")
sys.path.append(uiFilePath)

class updateWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testUpdate01.ui'))

        self.db = database.DataBase()

        self.load()

        self.ui.serialNoBox.currentIndexChanged.connect(self.loadDetails)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.confirmation)

        self.ui.setWindowTitle('Update Item Information')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)

    def load(self):
        sn = self.db.listOfSerialNo()
        self.SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(self.SN)

        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        self.ui.newLocationBox.clear()
        self.ui.newLocationBox.addItems(LOC)

        usr = self.db.listOfUser()
        USR = [x['user'] for x in usr]
        self.ui.newUserBox.clear()
        self.ui.newUserBox.addItems(USR)


    def loadDetails(self):
        slNo = self.ui.serialNoBox.currentText()
        # print slNo
        if slNo in self.SN:
            query = "SELECT * FROM ITEMS WHERE serial_no='%s' " %(slNo)
            details = self.db.getDetails(query)
            # print details
            iT = details["item_type"]
            dSC = details["description"]
            mK = details["make"]
            mDL = details["model"]
            lOC = details["location"]
            uSR = details["user"]

            self.ui.itemTypeBox.setText(iT)
            self.ui.descriptionBox.setText(dSC)
            self.ui.makeBox.setText(mK)
            self.ui.modelBox.setText(mDL)
            self.ui.currentLocationBox.setText(lOC)
            self.ui.currentUserBox.setText(uSR)
        else:
            self.clearAll()

    def clearAll(self):
        self.ui.serialNoBox.clearEditText()
        self.ui.itemTypeBox.clear()
        self.ui.descriptionBox.clear()
        self.ui.makeBox.clear()
        self.ui.modelBox.clear()
        self.ui.currentLocationBox.clear()
        self.ui.currentUserBox.clear()
        self.ui.newLocationBox.setCurrentIndex(0)
        self.ui.newUserBox.setCurrentIndex(0)
        # self.load()

    def confirmation(self):
        confirm = QtWidgets.QMessageBox()
        confirm.setIcon(QtWidgets.QMessageBox.Question)
        confirm.setWindowTitle("Confirmation")
        confirm.setInformativeText("Are you sure you want to save?")
        confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        ret = confirm.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            self.update()
        else:
            pass

    def update(self):
        userInput = OrderedDict()

        userInput["dateTime"] = time.strftime('%Y-%m-%d %H:%M:%S')
        userInput["slNo"] = str(self.ui.serialNoBox.currentText())
        userInput["oldLocation"] = str(self.ui.currentLocationBox.text())
        # userInput["oldUser"] = str(self.ui.currentUserBox.text())
        if userInput["slNo"] in self.SN:
            userInput["newLocation"] = str(self.ui.newLocationBox.currentText())
            # userInput["newUser"] = str(self.ui.newUserBox.currentText())
            userInput["updatedBy"] = os.environ['USER']

            query = "UPDATE ITEMS SET location = '%s' WHERE serial_no = '%s' " %(userInput["newLocation"], userInput["slNo"])
            self.updated = self.db.update(query)

            values = []
            for key in userInput.keys():
                values.append(userInput[key])
            # print values
            column = self.db.getColumnsOfLog()
            self.theColumn = [x['COLUMN_NAME'] for x in column]

            queryLog = "INSERT INTO UPDATE_LOG (" + ','.join(self.theColumn) + ") VALUES %r" %(tuple(values),)
            self.db.updateLog(queryLog)

            self.updateMessage()

    def updateMessage(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText(self.updated)
        msg.exec_()

    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = updateWidget()
    sys.exit(app.exec_())

