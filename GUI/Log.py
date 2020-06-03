#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database
import debug
import dbGrantha

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

db = dbGrantha.dbGrantha()

class logWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Log.ui'))

        # self.db = database.DataBase()

        self.load()

        self.ui.allButton.clicked.connect(self.allLog)
        self.ui.serialNoBox.currentIndexChanged.connect(self.loadLog)

        self.ui.setWindowTitle('Update Log')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))
        # self.ui.move(470, 200)
        self.ui.show()

    def load(self):
        # sn = self.db.listOfSerialNo()
        sn = db.execute("SELECT * FROM SERIAL_NO", dictionary=True)
        debug.info(sn)
        self.SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(self.SN)

    def allLog(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        # column = self.db.getColumnsOfLog()
        column = db.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'UPDATE_LOG' \
                            AND COLUMN_NAME NOT IN ('no')", dictionary=True)
        self.theColumn = [x['COLUMN_NAME'] for x in column]
        debug.info(self.theColumn)
        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        self.query = "SELECT " + ','.join(self.theColumn) + " FROM UPDATE_LOG"
        rows = db.execute(self.query,dictionary=True)
        self.ui.tableWidget.setRowCount(len(rows))

        # row = 0
        # db.execute(self.query,dictionary=True)
        # while True:
        #     primaryResult = db.execute(self.query,dictionary=True)
        #     debug.info(primaryResult)
        #     if (not primaryResult):
        #         break
        #     col = 0
        #     for n in self.theColumn:
        #         result = primaryResult[n]
        #         self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
        #         col +=1
        #     row +=1

        row = 0
        while True:
            if (row == len(rows)):
                break
            primaryResult = rows[row]
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                col += 1
            row += 1

        self.ui.tableWidget.resizeColumnsToContents()




    def loadLog(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        # column = self.db.getColumnsOfLog()
        column = db.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'UPDATE_LOG' \
                            AND COLUMN_NAME NOT IN ('no')", dictionary=True)
        self.theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        self.query = "SELECT " + ','.join(self.theColumn) + " FROM UPDATE_LOG WHERE serial_no='%s' " % (self.ui.serialNoBox.currentText())
        rows = db.execute(self.query,dictionary=True)
        debug.info(rows)
        if rows != 0:
            self.ui.tableWidget.setRowCount(len(rows))

        # row = 0
        # self.db.getValuesOfLog(self.query,init=True)
        # while True:
        #     primaryResult = self.db.getValuesOfLog(self.query)
        #     if (not primaryResult):
        #         break
        #     col = 0
        #     for n in self.theColumn:
        #         result = primaryResult[n]
        #         self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
        #         col +=1
        #     row +=1

            row = 0
            while True:
                if (row == len(rows)):
                    break
                primaryResult = rows[row]
                col = 0
                for n in self.theColumn:
                    result = primaryResult[n]
                    self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                    col += 1
                row += 1

            self.ui.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = logWidget()
    sys.exit(app.exec_())




