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
        self.ui.searchBox.currentIndexChanged.connect(self.searchLog)

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
            ln = db.execute("SELECT location FROM LOCATION WHERE location NOT LIKE 'aum%' AND location NOT LIKE 'REPAIR' AND location NOT LIKE 'OUTDATED' ", dictionary=True)
            # debug.info(ln)
            self.LN = [x['location'] for x in ln]
            self.ui.searchBox.clear()
            self.ui.searchBox.addItems(self.LN)


    # def allLog(self):
    #     self.ui.tableWidget.clearContents()
    #     self.ui.tableWidget.setRowCount(0)
    #     # column = self.db.getColumnsOfLog()
    #     column = db.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'UPDATE_LOG' \
    #                         AND COLUMN_NAME NOT IN ('no')", dictionary=True)
    #     self.theColumn = [x['COLUMN_NAME'] for x in column]
    #     debug.info(self.theColumn)
    #     self.ui.tableWidget.setColumnCount(len(self.theColumn))
    #     self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)
    #
    #     self.query = "SELECT " + ','.join(self.theColumn) + " FROM UPDATE_LOG"
    #     rows = db.execute(self.query,dictionary=True)
    #     self.ui.tableWidget.setRowCount(len(rows))
    #
    #     # row = 0
    #     # db.execute(self.query,dictionary=True)
    #     # while True:
    #     #     primaryResult = db.execute(self.query,dictionary=True)
    #     #     debug.info(primaryResult)
    #     #     if (not primaryResult):
    #     #         break
    #     #     col = 0
    #     #     for n in self.theColumn:
    #     #         result = primaryResult[n]
    #     #         self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
    #     #         col +=1
    #     #     row +=1
    #
    #     row = 0
    #     while True:
    #         if (row == len(rows)):
    #             break
    #         primaryResult = rows[row]
    #         col = 0
    #         for n in self.theColumn:
    #             result = primaryResult[n]
    #             self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
    #             col += 1
    #         row += 1
    #
    #     self.ui.tableWidget.resizeColumnsToContents()




    def loadLog(self,tablename):
        self.load()
        # pass
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        # column = self.db.getColumnsOfLog()
        columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND COLUMN_NAME NOT IN ('no')" %(tablename)
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


    def searchLog(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        # self.ui.tableWidget.setColumnCount(0)

        # tableName = ''
        # if self.ui.allItemsLog.isChecked():
        #     tableName = 'add_update_log'
        # elif self.ui.locationLog.isChecked():
        #     tableName = 'location_update_log'
        #
        # columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND COLUMN_NAME NOT IN ('no')" %(tableName)
        # column = db.execute(columnQuery, dictionary=True)
        # theColumn = [x['COLUMN_NAME'] for x in column]
        #
        # searchText = str(self.ui.searchBox.currentText().strip())

        # query = ""
        # if self.ui.allItemsLog.isChecked():
        #     query = "SELECT " + ','.join(theColumn) + " FROM '%s' " %(tableName)
        #     query = query.replace("\'", "")
        #     query = query + "WHERE serial_no='%s' " %(searchText)
        # elif self.ui.locationLog.isChecked():
        #     query = "SELECT " + ','.join(theColumn) + " FROM '%s' " %(tableName)
        #     query = query.replace("\'", "")
        #     query = query + "WHERE location='%s' " % (searchText)
        # query = "SELECT " + ','.join(theColumn) + " FROM '%s' WHERE serial_no='%s' or location='%s " % (tableName,searchText,searchText)
        # query = "SELECT " + ','.join(self.theColumn) + " FROM '%s' " % (tablename)
        # query = query.replace("\'", "")
        if self.ui.allItemsLog.isChecked():
            tableName = 'add_update_log'
            columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND COLUMN_NAME NOT IN ('no')" % (tableName)
            column = db.execute(columnQuery, dictionary=True)
            theColumn = [x['COLUMN_NAME'] for x in column]
            searchText = str(self.ui.searchBox.currentText().strip())
            query = "SELECT " + ','.join(theColumn) + " FROM '%s' " % (tableName)
            query = query.replace("\'", "")
            query = query + "WHERE serial_no='%s' " % (searchText)
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

        elif self.ui.locationLog.isChecked():
            tableName = 'location_update_log'
            columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND COLUMN_NAME NOT IN ('no')" % (tableName)
            column = db.execute(columnQuery, dictionary=True)
            theColumn = [x['COLUMN_NAME'] for x in column]
            searchText = str(self.ui.searchBox.currentText().strip())
            query = "SELECT " + ','.join(theColumn) + " FROM '%s' " % (tableName)
            query = query.replace("\'", "")
            query = query + "WHERE location='%s' " % (searchText)
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



if __name__ == '__main__':
    setproctitle.setproctitle("LOG")
    app = QtWidgets.QApplication(sys.argv)
    window = logWidget()
    sys.exit(app.exec_())




