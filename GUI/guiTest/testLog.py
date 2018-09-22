#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-3])
uiFilePath = os.path.join(progPath,"GUI","guiTest","uiFiles")
sys.path.append(uiFilePath)

class logWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testLog.ui'))

        self.db = database.DataBase()

        self.load()

        self.ui.serialNoBox.currentIndexChanged.connect(self.loadLog)

        self.ui.setWindowTitle('Update Log')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.move(470, 200)
        self.ui.show()

    def load(self):
        sn = self.db.listOfSerialNo()
        self.SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(self.SN)

    def loadLog(self):
        column = self.db.getColumnsOfLog()
        self.theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        # theRows = self.db.getAllRows()
        # self.ui.tableWidget.setRowCount(len(theRows))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = logWidget()
    sys.exit(app.exec_())




