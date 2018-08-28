#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test03.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import sys
import os

class Ui_MainWindow(object):
    def __init__(self, database, cursor):
        self.database = database
        self.cursor = cursor
        # self.db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        # self.cursor = self.db.cursor()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1303, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 1301, 601))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(540, 10, 241, 34))
        self.lineEdit.setObjectName("lineEdit")
        self.serialNoBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.serialNoBtn.setGeometry(QtCore.QRect(90, 10, 91, 24))
        self.serialNoBtn.setObjectName("serialNoBtn")
        self.itemTypeBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.itemTypeBtn.setGeometry(QtCore.QRect(210, 10, 101, 24))
        self.itemTypeBtn.setObjectName("tiemTypeBtn")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 10, 94, 36))
        self.pushButton.setObjectName("pushButton")
        self.userBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.userBtn.setGeometry(QtCore.QRect(460, 10, 71, 24))
        self.userBtn.setObjectName("userBtn")
        self.locationBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.locationBtn.setGeometry(QtCore.QRect(340, 10, 91, 24))
        self.locationBtn.setObjectName("locationBtn")

        self.serialNoBtn.pressed.connect(self.serialNoCompleter)
        self.itemTypeBtn.pressed.connect(self.itemTypeCompleter)
        self.locationBtn.pressed.connect(self.locationCompleter)
        self.userBtn.pressed.connect(self.userCompleter)

        self.pushButton.clicked.connect(self.mySql)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.tableWidget.setSortingEnabled(True)
        self.serialNoBtn.setText(_translate("MainWindow", "Serial No"))
        self.itemTypeBtn.setText(_translate("MainWindow", "Item Type"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.userBtn.setText(_translate("MainWindow", "User"))
        self.locationBtn.setText(_translate("MainWindow", "Location"))

    def serialNoCompleter(self):
        self.cursor.execute("SELECT serial_no FROM ITEMS")
        self.compList = list(set(sum(self.cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(self.compList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

    def itemTypeCompleter(self):
        self.cursor.execute("SELECT item_type FROM ITEMS")
        self.compList = list(set(sum(self.cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(self.compList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

    def locationCompleter(self):
        self.cursor.execute("SELECT location FROM ITEMS")
        self.compList = list(set(sum(self.cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(self.compList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

    def userCompleter(self):
        self.cursor.execute("SELECT user FROM ITEMS")
        self.compList = list(set(sum(self.cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(self.compList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

    def message(self):
        QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(),"Error!","Please Check Input.")

    def mySql(self):
        self.cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
        col = sum(self.cursor.fetchall(), ())

        self.tableWidget.setHorizontalHeaderLabels(col)
        self.tableWidget.setColumnCount(len(col))

        if self.serialNoBtn.isChecked():
            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' " %(self.lineEdit.text()))
            allRows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(allRows))
            # self.tableWidget.setColumnCount(10)

            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' " %(self.lineEdit.text()))
            row = 0
            while True:
                result = self.cursor.fetchone()
                if result == None:
                    break
                for col in range(0, 10):
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result[col])))
                    self.tableWidget.resizeColumnsToContents()
                    #self.tableWidget.setSortingEnabled(True)
                row += 1

        elif self.itemTypeBtn.isChecked():
            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE item_type='%s' " %(self.lineEdit.text()))
            allRows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(allRows))
            # self.tableWidget.setColumnCount(10)

            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE item_type='%s' " %(self.lineEdit.text()))
            row = 0
            while True:
                result = self.cursor.fetchone()
                if result == None:
                    break
                for col in range(0, 10):
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result[col])))
                    self.tableWidget.resizeColumnsToContents()
                    #self.tableWidget.setSortingEnabled(True)
                row += 1

        elif self.locationBtn.isChecked():
            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE location='%s' " %(self.lineEdit.text()))
            allRows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(allRows))
            # self.tableWidget.setColumnCount(10)

            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE location='%s' " %(self.lineEdit.text()))
            row = 0
            while True:
                result = self.cursor.fetchone()
                if result == None:
                    break
                for col in range(0, 10):
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result[col])))
                    self.tableWidget.resizeColumnsToContents()
                    #self.tableWidget.setSortingEnabled(True)
                row += 1

        elif self.userBtn.isChecked():
            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE user='%s' " %(self.lineEdit.text()))
            allRows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(allRows))
            # self.tableWidget.setColumnCount(10)

            self.cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE user='%s' " %(self.lineEdit.text()))
            row = 0
            while True:
                result = self.cursor.fetchone()
                if result == None:
                    break
                for col in range(0, 10):
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result[col])))
                    self.tableWidget.resizeColumnsToContents()
                    #self.tableWidget.setSortingEnabled(True)
                row += 1
        else:
            self.message()

    # self.cursor.close()
    # self.database.close()

if __name__ == "__main__":
    database = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
    cursor = database.cursor()

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(database, cursor)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

