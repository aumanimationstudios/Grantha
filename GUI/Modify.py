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

        self.ui.locationBox.currentIndexChanged.connect(self.loadPrimaryLocation)
        self.ui.clearButton.clicked.connect(self.clearAll)



        self.ui.setWindowTitle('Modify Parent Location')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))

        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.ui.close)

    def load(self):
        query01 = "SELECT location FROM LOCATION WHERE location NOT LIKE 'aum%' AND location NOT LIKE 'REPAIR' "
        loc = self.db.getLocation(query01)
        LOC = [x['location'] for x in loc]
        self.ui.locationBox.clear()
        self.ui.locationBox.addItems(LOC)

        query02 = "SELECT location FROM LOCATION WHERE location NOT LIKE 'blue%' "
        par = self.db.getLocation(query02)
        PAR = [x['location'] for x in par]
        self.ui.newParentLocationBox.clear()
        self.ui.newParentLocationBox.addItems(PAR)

    def loadPrimaryLocation(self):
        loc = self.ui.locationBox.currentText()
        query = "SELECT parent_location FROM LOCATION WHERE location='%s' " %(loc)
        pL = self.db.getParentLocation(query)
        parentLoc = pL["parent_location"]
        self.ui.currentParentLocationBox.setText(parentLoc)

    def clearAll(self):
        self.ui.locationBox.setCurrentIndex(0)
        self.ui.newParentLocationBox.setCurrentIndex(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = modifyWidget()
    sys.exit(app.exec_())

