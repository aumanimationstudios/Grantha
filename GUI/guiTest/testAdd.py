#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database
import string
import random
from collections import OrderedDict


filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-3])
uiFilePath = os.path.join(progPath,"GUI","guiTest","uiFiles")
sys.path.append(uiFilePath)

class addWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testAdd01.ui'))

        self.db = database.DataBase()

        self.load()
        self.ui.priceBox.setText('0.00')

        self.ui.randomButton.clicked.connect(self.slNoGen)
        self.ui.purchaseNoneButton.clicked.connect(self.purchaseNone)
        self.ui.validNoneButton.clicked.connect(self.validNone)
        self.ui.locationNoneButton.clicked.connect(self.locationNone)
        self.ui.userNoneButton.clicked.connect(self.userNone)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.confirmation)

        self.ui.setWindowTitle('Add Item')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)

    def load(self):
        it = self.db.listOfItemType()
        IT = [x['item_type'] for x in it]
        self.ui.itemTypeBox.clear()
        self.ui.itemTypeBox.addItems(IT)

        desc = self.db.listOfDescription()
        self.DESC = [x['description'] for x in desc]
        self.ui.descriptionBox.clear()
        self.ui.descriptionBox.addItems(self.DESC)

        mk = self.db.listOfMake()
        self.MK = [x['make'] for x in mk]
        self.ui.makeBox.clear()
        self.ui.makeBox.addItems(self.MK)

        mdl = self.db.listOfModel()
        self.MDL = [x['model'] for x in mdl]
        self.ui.modelBox.clear()
        self.ui.modelBox.addItems(self.MDL)

        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        self.ui.locationBox.clear()
        self.ui.locationBox.addItems(LOC)

        usr = self.db.listOfUser()
        USR = [x['user'] for x in usr]
        self.ui.userBox.clear()
        self.ui.userBox.addItems(USR)

        self.ui.priceBox.setText('0.00')


    def slNoGen(self):
        slNo = self.slNoGenerator()

        sn = self.db.listOfSerialNo()
        SN = [x['serial_no'] for x in sn]

        if slNo in SN:
            self.slNoGen()
        else:
            self.ui.serialNoBox.setText(slNo)

    def slNoGenerator(self, size=10, chars=string.ascii_uppercase + string.digits):
        slNo = ''.join(random.SystemRandom().choice(chars) for n in range(size))
        return slNo

    def purchaseNone(self):
        self.ui.purchaseYYYY.setCurrentIndex(1)
        self.ui.purchaseMM.setCurrentIndex(1)
        self.ui.purchaseDD.setCurrentIndex(1)

    def validNone(self):
        self.ui.validYYYY.setCurrentIndex(1)
        self.ui.validMM.setCurrentIndex(1)
        self.ui.validDD.setCurrentIndex(1)

    def locationNone(self):
        self.ui.locationBox.setCurrentIndex(0)

    def userNone(self):
        self.ui.userBox.setCurrentIndex(0)

    def clearAll(self):
        self.ui.serialNoBox.clear()
        self.ui.itemTypeBox.setCurrentIndex(0)
        self.ui.descriptionBox.clearEditText()
        self.ui.makeBox.clearEditText()
        self.ui.modelBox.clearEditText()
        self.ui.priceBox.setText('0.00')
        self.purchaseNone()
        self.validNone()
        self.locationNone()
        self.userNone()
        self.load()

    def confirmation(self):
        confirm = QtWidgets.QMessageBox()
        confirm.setIcon(QtWidgets.QMessageBox.Question)
        confirm.setWindowTitle("Confirmation")
        confirm.setInformativeText("Are you sure you want to save?")
        confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # confirm.question(confirm,"Confirmation","Are you sure you want to save?", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
        ret = confirm.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            self.addNew()
        else:
            pass

    def addNew(self):
        userInput = OrderedDict()

        userInput["sN"] = str(self.ui.serialNoBox.text())
        userInput["iT"] = str(self.ui.itemTypeBox.currentText())
        userInput["dSC"] = str(self.ui.descriptionBox.currentText())
        userInput["mK"] = str(self.ui.makeBox.currentText())
        userInput["mDL"] = str(self.ui.modelBox.currentText())
        userInput["pRC"] = str(self.ui.priceBox.text())
        pY = str(self.ui.purchaseYYYY.currentText())
        pM = str(self.ui.purchaseMM.currentText())
        pD = str(self.ui.purchaseDD.currentText())
        userInput["pDT"] = pY+'-'+pM+'-'+pD
        vY = str(self.ui.validYYYY.currentText())
        vM = str(self.ui.validMM.currentText())
        vD = str(self.ui.validDD.currentText())
        userInput["vDT"] = vY+'-'+vM+'-'+vD
        userInput["lC"] = str(self.ui.locationBox.currentText())
        userInput["uSR"] = str(self.ui.userBox.currentText())

        values = []
        for key in userInput.keys():
            values.append(userInput[key])
        print values

        if userInput["dSC"] not in self.DESC:
            query = "INSERT INTO DESCRIPTION (description) VALUES (%r)" %(userInput["dSC"])
            self.db.insertDescription(query)
            # print "description added"

        if userInput["mK"] not in self.MK:
            query = "INSERT INTO MAKE (make) VALUES (%r)" %(userInput["mK"])
            self.db.insertMake(query)
            # print "make added"

        if userInput["mDL"] not in self.MDL:
            query = "INSERT INTO MODEL (model) VALUES (%r)" %(userInput["mDL"])
            self.db.insertModel(query)
            # print "model added"

        column = self.db.getColumns()
        self.theColumn = [x['COLUMN_NAME'] for x in column]

        queryAddItem = "INSERT INTO ITEMS (" + ','.join(self.theColumn) + ") VALUES %r" %(tuple(values),)
        queryAddSlNo = "INSERT INTO SERIAL_NO (serial_no) VALUES ('%s') " %(userInput["sN"])

        self.addItem = self.db.insertItem(queryAddItem)
        self.db.insertSerialNo(queryAddSlNo)
        # print self.addItem

        self.insertMessage()
        self.load()

    def insertMessage(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText(self.addItem)
        msg.exec_()
        # msg.resize(0,0)
        # msg.about(msg,"Message", self.addItem)

    # def okMessage(self):
    #     msgBox = QtWidgets.QMessageBox()
    #     msgBox.resize(0,0)
    #     msgBox.about(msgBox,"Confirmation","Item Added. \nSl.No: "+ self.ui.serialNoBox.text())

    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = addWidget()
    sys.exit(app.exec_())

