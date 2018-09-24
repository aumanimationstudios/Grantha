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

        self.ui.allButton.clicked.connect(self.allLog)
        self.ui.serialNoBox.currentIndexChanged.connect(self.loadLog)

        self.ui.setWindowTitle('Update Log')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        # self.ui.move(470, 200)
        self.ui.show()

    def load(self):
        sn = self.db.listOfSerialNo()
        self.SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(self.SN)

    def allLog(self):
        self.ui.tableWidget.clearContents()
        column = self.db.getColumnsOfLog()
        self.theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        self.query = "SELECT " + ','.join(self.theColumn) + " FROM UPDATE_LOG"
        rows = self.db.getRowsOfLog(self.query)
        self.ui.tableWidget.setRowCount(len(rows))

        row = 0
        self.db.getValuesOfLog(self.query,init=True)
        while True:
            primaryResult = self.db.getValuesOfLog(self.query)
            if (not primaryResult):
                break
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        self.ui.tableWidget.resizeColumnsToContents()




    def loadLog(self):
        column = self.db.getColumnsOfLog()
        self.theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        self.query = "SELECT " + ','.join(self.theColumn) + " FROM UPDATE_LOG WHERE serial_no='%s' " % (self.ui.serialNoBox.currentText())
        rows = self.db.getRowsOfLog(self.query)
        self.ui.tableWidget.setRowCount(len(rows))

        row = 0
        self.db.getValuesOfLog(self.query,init=True)
        while True:
            primaryResult = self.db.getValuesOfLog(self.query)
            if (not primaryResult):
                break
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        self.ui.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = logWidget()
    sys.exit(app.exec_())




