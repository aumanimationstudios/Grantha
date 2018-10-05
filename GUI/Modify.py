#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI", "uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

class modifyWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Modify.ui'))

        self.db = database.DataBase()

        self.load()

        # self.ui.locationBox.currentIndexChanged.connect(self.loadPrimaryLocation)



        self.ui.setWindowTitle('Modify Parent Location')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))

        self.ui.show()

    def load(self):
        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        self.ui.locationBox.clear()
        self.ui.locationBox.addItems(LOC)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = modifyWidget()
    sys.exit(app.exec_())

