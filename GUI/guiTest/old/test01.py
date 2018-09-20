#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test01.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from collections import OrderedDict
import MySQLdb
import MySQLdb.cursors
import sys
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1297, 776)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 1281, 761))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 1261, 681))
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setGeometry(QtCore.QRect(570, 720, 111, 24))
        self.radioButton.setObjectName("radioButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton.setText(_translate("MainWindow", "All"))
        self.radioButton.clicked.connect(self.mySql)
        # self.tableWidget.setSortingEnabled(True)

    def mySql(self):
        db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
        col = cursor.fetchall()
        colName = [x['COLUMN_NAME'] for x in col]
        #print colName

        self.tableWidget.setColumnCount(len(colName))
        self.tableWidget.setHorizontalHeaderLabels(colName)

        # cursor.execute("SELECT " + ','.join(colName) + " FROM ITEMS ORDER BY item_type")
        cursor.execute("SELECT * FROM ITEMS ORDER BY item_type")
        allRows = cursor.fetchall()
        #print len(allRows)
        self.tableWidget.setRowCount(len(allRows))

        # cursor.execute("SELECT " + ','.join(colName) + " FROM ITEMS ORDER BY item_type")
        cursor.execute("SELECT * FROM ITEMS ORDER BY item_type")
        row = 0
        while True:
            primaryResult = cursor.fetchone()
            #print(primaryResult)
            if(not primaryResult):
                break
            col = 0
            for n in colName:
                result = primaryResult[n]
                #print(result)
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                col += 1
            row += 1

        self.tableWidget.resizeColumnsToContents()
        cursor.close()
        db.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

