#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database


filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-3])
uiFilePath = os.path.join(progPath,"GUI","guiTest","uiFiles")
sys.path.append(uiFilePath)

class updateWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testUpdate01.ui'))

        self.db = database.DataBase()

        sn = self.db.listOfSerialNo()
        SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(SN)


        self.ui.serialNoBox.currentIndexChanged.connect(self.loadLocnUsr)

        self.ui.setWindowTitle('Update Item Information')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)


    def loadLocnUsr(self):
        slNo = self.ui.serialNoBox.currentText()
        # print slNo

        query = "SELECT location, user FROM ITEMS WHERE serial_no='%s' " %(slNo)
        locnusr = self.db.getLocnUsr(query)
        print locnusr
        lOC = locnusr('location')
        iT = locnusr('user')
        print lOC
        print iT


        # self.ui.currentLocationBox.setText(lOC)
        # self.ui.cujrrentUserBox.setText(iT)

    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = updateWidget()
    sys.exit(app.exec_())

