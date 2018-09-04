#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

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

        self.ui.allButton.pressed.connect(self.allBtnClick)
        self.ui.serialNoButton.pressed.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.pressed.connect(self.itBtnClick)
        self.ui.locationButton.pressed.connect(self.locBtnClick)
        self.ui.userButton.pressed.connect(self.usrBtnClick)

        # self.ui.searchButton.clicked.connect(self.test)

        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))

        self.db = database.DataBase()

    def allBtnClick(self):
        #db = database.DataBase()
        column = self.db.getColumns()
        theColumn = [x['COLUMN_NAME'] for x in column]

        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        theRows = self.db.getAllRows()

        self.ui.tableWidget.setRowCount(len(theRows))

        row = 0
        self.db.getAllValues(init=True)
        while True:
            primaryResult = self.db.getAllValues()
            # print primaryResult
            if (not primaryResult):
                break
            col = 0
            for n in theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

    def slNoBtnClick(self):
        theList = self.db.Completer()
        slList = [x['serial_no'] for x in theList]
        self.model = QtCore.QStringListModel()
        self.model.setStringList(slList)
        self.completer()

    def itBtnClick(self):
        theList = self.db.Completer()
        itList = list(set([x['item_type'] for x in theList]))
        self.model = QtCore.QStringListModel()
        self.model.setStringList(itList)
        self.completer()

    def locBtnClick(self):
        theList = self.db.Completer()
        locList = list(set([x['location'] for x in theList]))
        self.model = QtCore.QStringListModel()
        self.model.setStringList(locList)
        self.completer()

    def usrBtnClick(self):
        theList = self.db.Completer()
        usrList = list(set([x['user'] for x in theList]))
        self.model = QtCore.QStringListModel()
        self.model.setStringList(usrList)
        self.completer()

    def completer(self):
        completer = QtWidgets.QCompleter()
        completer.setModel(self.model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.lineEdit.setCompleter(completer)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = myWindow()
    sys.exit(app.exec_())

