#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic

class dateWidget():
    def __init__(self):
        self.ui = uic.loadUi('dateTest.ui')

        self.ui.toolButton.clicked.connect(self.showCal)
        self.ui.pushButton.clicked.connect(self.noDate)

        self.ui.toolButton.setIcon(QtGui.QIcon('cal.png'))

        self.ui.show()

    def showCal(self):
        self.cal = QtWidgets.QCalendarWidget()
        self.cal.clicked.connect(self.updateDate)
        self.cal.show()

    def updateDate(self):
        date = self.cal.selectedDate().toString(QtCore.Qt.ISODate)
        # print date
        self.ui.lineEdit.setText(date)

        self.cal.close()

    def noDate(self):
        self.ui.lineEdit.setText("0000-00-00")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = dateWidget()
    sys.exit(app.exec_())



