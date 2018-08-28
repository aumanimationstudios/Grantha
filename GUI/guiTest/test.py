#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import MySQLdb.cursors
import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-3])
uiFilePath = os.path.join(progPath,"GUI","guiTest","uiFiles")
sys.path.append(uiFilePath)

class myWindow():
    def __init__(self):
        # super(myWindow, self).__init__()
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'test.ui'))
        self.ui.show()

        self.ui.allButton.pressed.connect(self.onClick)
        self.ui.searchButton.clicked.connect(self.test)

        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))

    def onClick(self):
        db = database.DataBase()
        theColumn = db.getColumns()

        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        theRows = db.getAllRows()

        self.ui.tableWidget.setRowCount(len(theRows))

        # db.getValues()
        # print theValues
        row = 0
        db.getValues(init=True)
        while True:
            primaryResult = db.getValues()
            # print primaryResult
            if (not primaryResult):
                break
            col = 0
            for n in theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        # self.ui.resizeColumnsToContents()

        # print theFunc
        # print anotherFunc
        # for n in theFunc:
        #     result = anotherFunc[n]
        #     print result

    def test(self):
        print self.ui.lineEdit.text()

    # def onUnclick(self):
    #     print "False"

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = myWindow()
    sys.exit(app.exec_())

