#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database
import debug
import dbGrantha
import setproctitle
from Utils_Gui import *


filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")

sys.path.append(uiDir)
sys.path.append(imageDir)

db = dbGrantha.dbGrantha()

class logWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiDir,'Log.ui'))

        # self.db = database.DataBase()

        self.load()

        # self.ui.allButton.clicked.connect(self.allLog)
        self.loadLog("add_update_log")
        self.ui.allItemsLog.clicked.connect(lambda x, log="add_update_log": self.loadLog(log))
        self.ui.locationLog.clicked.connect(lambda x, log="location_update_log": self.loadLog(log))
        self.ui.repairLog.clicked.connect(lambda x, log="repair_log": self.loadLog(log))
        self.ui.searchBox.currentIndexChanged.connect(self.searchLog)

        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.center()
        self.ui.setWindowTitle('Log')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))
        # self.ui.move(470, 200)
        self.ui.show()

        try:
            theme = os.environ['GRANTHA_THEME']
            # debug.info(theme)
            setStyleSheet(self.ui, theme)
        except:
            pass



    def load(self):
        if self.ui.allItemsLog.isChecked():
            self.ui.label.setText("serial no:")
            sn = db.execute("SELECT * FROM SERIAL_NO", dictionary=True)
            # debug.info(sn)
            self.SN = [x['serial_no'] for x in sn]
            self.SN.sort()
            self.ui.searchBox.clear()
            self.ui.searchBox.addItems(self.SN)

        elif self.ui.locationLog.isChecked():
            self.ui.label.setText("location:")
            ln = db.execute("SELECT location FROM LOCATION WHERE location NOT LIKE 'aum%' AND location NOT LIKE \
                            'REPAIR' AND location NOT LIKE 'OUTDATED' ", dictionary=True)
            # debug.info(ln)
            self.LN = [x['location'] for x in ln]
            self.ui.searchBox.clear()
            self.ui.searchBox.addItems(self.LN)

        elif self.ui.repairLog.isChecked():
            self.ui.label.setText("item:")
            # getSN = "SELECT * FROM SERIAL_NO"
            sn = db.execute("SELECT * FROM SERIAL_NO", dictionary=True)
            slNos = [x['serial_no'] for x in sn]
            slNos.sort()
            # getLOC = "SELECT * FROM LOCATION"
            LOCS = db.execute("SELECT * FROM LOCATION", dictionary=True)
            # locs = [x['location'] for x in LOCS]
            pLocs = [x['parent_location'] for x in LOCS]
            blues=[]
            for pl in pLocs:
                if pl != None:
                    bloc = next(x['location'] for x in LOCS if x['parent_location'] == pl)
                    blues.append(bloc)
            blues = list(set(blues))
            blues.sort()
            self.ui.searchBox.clear()
            self.ui.searchBox.addItems(slNos)
            self.ui.searchBox.addItems(blues)


    def loadLog(self,tablename):
        self.load()
        # pass
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        # column = self.db.getColumnsOfLog()
        columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND \
                       COLUMN_NAME NOT IN ('no')" %(tablename)
        column = db.execute(columnQuery, dictionary=True)
        theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        query = "SELECT " + ','.join(theColumn) + " FROM '%s' " % (tablename)
        query = query.replace("\'", "")
        rows = db.execute(query,dictionary=True)
        # debug.info(rows)
        if rows != 0:
            self.ui.tableWidget.setRowCount(len(rows))

            row = 0
            while True:
                if (row == len(rows)):
                    break
                primaryResult = rows[row]
                col = 0
                for n in theColumn:
                    result = primaryResult[n]
                    self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                    col += 1
                row += 1

        # self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.resizeColumnsToContents()
        if (tablename == "add_update_log"):
            self.ui.resize(700, 700)
        else:
            header = self.ui.tableWidget.horizontalHeader()
            self.ui.resize(header.length()+52, 700)


    def searchLog(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)

        tableName = ''
        item = ''
        if self.ui.allItemsLog.isChecked():
            tableName = 'add_update_log'
            item = 'serial_no'
        elif self.ui.locationLog.isChecked():
            tableName = 'location_update_log'
            item = 'location'
        elif self.ui.repairLog.isChecked():
            tableName = 'repair_log'
            item = 'item'

        columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND \
                       COLUMN_NAME NOT IN ('no')" % (tableName)
        column = db.execute(columnQuery, dictionary=True)
        theColumn = [x['COLUMN_NAME'] for x in column]
        searchText = str(self.ui.searchBox.currentText().strip())
        query = "SELECT " + ','.join(theColumn) + " FROM '%s' " % (tableName)
        query = query.replace("\'", "")
        query = query + "WHERE "+item+"='%s' " % (searchText)
        rows = db.execute(query, dictionary=True)
        # debug.info(rows)
        if rows != 0:
            self.ui.tableWidget.setRowCount(len(rows))

            row = 0
            while True:
                if (row == len(rows)):
                    break
                primaryResult = rows[row]
                col = 0
                for n in theColumn:
                    result = primaryResult[n]
                    self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                    col += 1
                row += 1

    def center(self):
        qr = self.ui.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())


if __name__ == '__main__':
    setproctitle.setproctitle("LOG")
    app = QtWidgets.QApplication(sys.argv)
    window = logWidget()
    sys.exit(app.exec_())




