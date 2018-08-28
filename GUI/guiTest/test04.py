#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test04.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import sys
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1295, 601)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 1291, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(10)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(650, 10, 94, 36))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(412, 10, 221, 34))
        self.lineEdit.setObjectName("lineEdit")

        self.completer()
        self.pushButton.clicked.connect(self.mySql)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Search"))

    def completer(self):
        db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        cursor = db.cursor()
        cursor.execute("SELECT serial_no, item_type, location FROM ITEMS")
        compList = list(set(sum(cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(compList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)
        cursor.close()
        db.close()

    def mySql(self):
        db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        cursor = db.cursor()
        cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
        col = sum(cursor.fetchall(), ())

        self.tableWidget.setHorizontalHeaderLabels(col)

        cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' OR item_type='%s' \
                        OR location='%s' " %(self.lineEdit.text(), self.lineEdit.text(), self.lineEdit.text()))
        allRows = cursor.fetchall()
        #print len(allRows)
        self.tableWidget.setRowCount(len(allRows))
        self.tableWidget.setColumnCount(10)

        cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' OR item_type='%s' \
                        OR location='%s' " %(self.lineEdit.text(), self.lineEdit.text(), self.lineEdit.text()))
        row = 0
        while True:
            result = cursor.fetchone()
            if result == None:
                break
            for col in range(0, 10):
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result[col])))
                self.tableWidget.resizeColumnsToContents()
                #self.tableWidget.setSortingEnabled(True)
            row += 1

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

