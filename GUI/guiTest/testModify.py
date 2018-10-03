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

class modifyWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testModify.ui'))

        self.ui.setWindowTitle('Modify Parent Location')
        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))

        self.ui.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = modifyWidget()
    sys.exit(app.exec_())

