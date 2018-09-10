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

class mainWindow():
    def __init__(self):
        # super(myWindow, self).__init__()
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'test.ui'))
        # self.ui.show()

        self.ui.allButton.pressed.connect(self.allBtnClick)
        self.ui.serialNoButton.pressed.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.pressed.connect(self.itBtnClick)
        self.ui.locationButton.pressed.connect(self.locBtnClick)
        self.ui.userButton.pressed.connect(self.usrBtnClick)

        self.ui.searchButton.clicked.connect(self.search)

        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))

        self.ui.show()

        self.db = database.DataBase()

    def allBtnClick(self):
        # self.ui.tableWidget.setSortingEnabled(False)
        # self.ui.tableWidget.resizeColumnsToContents()
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

        self.ui.tableWidget.resizeColumnsToContents()
        # self.ui.tableWidget.setSortingEnabled(True)




    def search(self):
        column = self.db.getColumns()
        self.theColumn = [x['COLUMN_NAME'] for x in column]

        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        if self.ui.serialNoButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(self.ui.lineEdit.text())
            rows = self.db.getRows(self.query)
            # print rows
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.itemTypeButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE item_type='%s' " %(self.ui.lineEdit.text())
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.locationButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE location='%s' " %(self.ui.lineEdit.text())
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.userButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE user='%s' " %(self.ui.lineEdit.text())
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        # else:
        #     self.message()

    def fillTable(self):
        row = 0
        self.db.getValues(self.query,init=True)
        while True:
            primaryResult = self.db.getValues(self.query)
            # print primaryResult
            if (not primaryResult):
                break
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        self.ui.tableWidget.resizeColumnsToContents()




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

    # def message(self):
    #     QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(),"Error!","Please Check Input.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

