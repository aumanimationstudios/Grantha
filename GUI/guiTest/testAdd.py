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
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testAdd.ui'))

        self.db = database.DataBase()

        it = self.db.listOfItemType()
        IT = [x['item_type'] for x in it]
        self.ui.itemTypeBox.addItems(IT)

        desc = self.db.listOfDescription()
        DESC = [x['description'] for x in desc]
        self.ui.descriptionBox.addItems(DESC)

        mk = self.db.listOfMake()
        MK = [x['make'] for x in mk]
        self.ui.makeBox.addItems(MK)

        mdl = self.db.listOfModel()
        MDL = [x['model'] for x in mdl]
        self.ui.modelBox.addItems(MDL)

        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        self.ui.locationBox.addItems(LOC)

        usr = self.db.listOfUser()
        USR = [x['user'] for x in usr]
        self.ui.userBox.addItems(USR)

        self.ui.priceBox.setText('0.00')

        self.ui.randomButton.clicked.connect(self.slNoGen)
        self.ui.purchaseNoneButton.clicked.connect(self.purchaseNone)
        self.ui.validNoneButton.clicked.connect(self.validNone)
        self.ui.locationNoneButton.clicked.connect(self.locationNone)
        self.ui.userNoneButton.clicked.connect(self.userNone)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.addNew)

        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)

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
        self.ui.descriptionBox.clearEditText()
        self.ui.makeBox.clearEditText()
        self.ui.modelBox.clearEditText()
        self.ui.priceBox.setText('0.00')
        self.purchaseNone()
        self.validNone()
        self.locationNone()
        self.userNone()

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

        # column = self.db.getColumns()
        # self.theColumn = [x['COLUMN_NAME'] for x in column]
        #
        # self.query = "INSERT INTO ITEMS (" + ','.join(self.theColumn) + ") VALUES %r" %(tuple(values),)
        # self.db.insertItem(self.query)
        # self.message()

    def message(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.resize(0,0)
        msgBox.about(msgBox,"Confirmation","Item Added. \nSl.No: "+ self.ui.serialNoBox.text())


    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = addWidget()
    sys.exit(app.exec_())

