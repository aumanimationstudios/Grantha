#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test02.ui'
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
        MainWindow.resize(1293, 676)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(400, 10, 91, 31))
        self.radioButton.setObjectName("radioButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(510, 10, 241, 34))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 10, 94, 36))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(5, 51, 1281, 621))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)

        self.pushButton.clicked.connect(self.onClick)
        self.completer()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def completer(self):
        db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        cursor = db.cursor()
        cursor.execute("SELECT serial_no FROM ITEMS")
        self.slList = set(list(sum(cursor.fetchall(), ())))
        model = QtCore.QStringListModel()
        model.setStringList(self.slList)
        completer = QtWidgets.QCompleter()
        completer.setModel(model)
        self.lineEdit.setCompleter(completer)
        cursor.close()
        db.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton.setText(_translate("MainWindow", "Serial No"))
        self.pushButton.setText(_translate("MainWindow", "Search"))

    def onClick(self):
        self.mySql()
        #print(self.lineEdit.text())

    def message(self):
        QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(),"Error!","Check Serial No.")

    def mySql(self):
        db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
        cursor = db.cursor()

        # cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        # WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
        # col = sum(cursor.fetchall(), ())
        #
        # self.tableWidget.setHorizontalHeaderLabels(col)
        # self.tableWidget.setColumnCount(len(col))

        if self.radioButton.isChecked():
            if self.lineEdit.text() not in self.slList:
                self.message()

            cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
            WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
            col = sum(cursor.fetchall(), ())

            self.tableWidget.setHorizontalHeaderLabels(col)
            self.tableWidget.setColumnCount(len(col))

            cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' " %(self.lineEdit.text()))
            allRows = cursor.fetchall()
            #print len(allRows)
            self.tableWidget.setRowCount(len(allRows))
            #self.tableWidget.setColumnCount(10)

            cursor.execute("SELECT " + ','.join(col) + " FROM ITEMS WHERE serial_no='%s' " %(self.lineEdit.text()))
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
        else:
            self.message()

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

