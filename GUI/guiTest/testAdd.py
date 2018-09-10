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

class addWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'testAdd.ui'))

        self.db = database.DataBase()

        it = self.db.listOfItemType()
        IT = [x['item_type'] for x in it]
        self.ui.itemTypeBox.addItems(IT)

        desc = self.db.listOfDescription()
        DESC = [x['description'] for x in desc]
        self.ui.descriptionBox.addItems(DESC)

        mk = self.db.listOfMake()
        MK = [x['make'] for x in mk]
        self.ui.makeBox.addItems(MK)

        mdl = self.db.listOfModel()
        MDL = [x['model'] for x in mdl]
        self.ui.modelBox.addItems(MDL)

        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        self.ui.locationBox.addItems(LOC)

        usr = self.db.listOfUser()
        USR = [x['user'] for x in usr]
        self.ui.userBox.addItems(USR)




        self.ui.setWindowIcon(QtGui.QIcon('granthaLogo.png'))
        self.ui.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = addWidget()
    sys.exit(app.exec_())

