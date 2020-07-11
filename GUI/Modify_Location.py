#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,uic
import dbGrantha
import debug
from Utils_Gui import *
import argparse
import setproctitle
from collections import OrderedDict
import time

filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI", "uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")

sys.path.append(uiDir)
sys.path.append(imageDir)

parser = argparse.ArgumentParser(description="Utility to modify location")
parser.add_argument("-n","--name",dest="name",help="name of location")
args = parser.parse_args()


class modifyWidget():
    db = dbGrantha.dbGrantha()

    queryLoc = "SELECT location FROM LOCATION WHERE location NOT LIKE 'aum%' AND location NOT LIKE 'REPAIR' AND location NOT LIKE 'OUTDATED' "
    loc = db.execute(queryLoc, dictionary=True)
    LOC = [x['location'] for x in loc]

    queryParLoc = "SELECT location FROM LOCATION WHERE location NOT LIKE 'blue%' "
    par = db.execute(queryParLoc, dictionary=True)
    PAR = [x['location'] for x in par]


    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiDir, 'Modify_Location.ui'))

        # self.db = database.DataBase()

        self.load()
        if args.name:
            self.ui.locationBox.setEditText(str(args.name))
            self.loadParentLocation()

        self.ui.locationBox.currentIndexChanged.connect(self.loadParentLocation)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.confirmation)


        self.ui.setWindowTitle('Modify Parent Location')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))

        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)

        # setStyleSheet(self.ui
        try:
            theme = os.environ['GRANTHA_THEME']
            debug.info(theme)
            setStyleSheet(self.ui, theme)
        except:
            pass

    def load(self):

        self.ui.locationBox.clear()
        self.ui.locationBox.addItems(self.LOC)

        self.ui.newParentLocationBox.clear()
        self.ui.newParentLocationBox.addItems(self.PAR)

    def loadParentLocation(self):
        loc = self.ui.locationBox.currentText().strip()
        getParentLocation = "SELECT parent_location FROM LOCATION WHERE location='%s' " %(loc)
        # pL = self.db.getParentLocation(query)
        pL = self.db.execute(getParentLocation,dictionary=True)
        pL = pL[0]
        debug.info(pL)
        parentLoc = pL["parent_location"]
        self.ui.currentParentLocationBox.setText(parentLoc)

    def confirmation(self):
        confirm = QtWidgets.QMessageBox()
        confirm.setIcon(QtWidgets.QMessageBox.Question)
        confirm.setWindowTitle("Confirmation")
        confirm.setInformativeText("Are you sure you want to save?")
        confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        cnfrm = confirm.exec_()
        if cnfrm == QtWidgets.QMessageBox.Ok:
            self.update()
        else:
            pass

    def update(self):
        userInput = OrderedDict()

        userInput["date"] = time.strftime('%Y-%m-%d %H:%M:%S')
        userInput["location"] = str(self.ui.locationBox.currentText().strip())
        userInput["old_parent_location"] = str(self.ui.currentParentLocationBox.text().strip())
        userInput["new_parent_location"] = str(self.ui.newParentLocationBox.currentText().strip())
        userInput["user"] = os.environ['USER']

        loc = self.ui.locationBox.currentText().strip()
        if loc:
            newPLoc = self.ui.newParentLocationBox.currentText().strip()
            if newPLoc:
                query = "UPDATE LOCATION SET parent_location = '%s' WHERE location = '%s'" %(newPLoc, loc)

                # self.updated = self.db.update(query)
                updated = self.db.execute(query)
                debug.info(updated)
                if (updated==1):
                    values = []
                    for key in userInput.keys():
                        values.append(userInput[key])
                    columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'location_update_log' \
                                   AND COLUMN_NAME NOT IN ('no')"
                    column = self.db.execute(columnQuery,dictionary=True)
                    self.theColumn = [x['COLUMN_NAME'] for x in column]
                    updateLogQuery = "INSERT INTO location_update_log (" + ','.join(self.theColumn) + ") VALUES %r" %(tuple(values),)
                    logUpdated = self.db.execute(updateLogQuery)
                    if (logUpdated == 1):
                        self.message("Update Successful")
                else:
                    self.message(updated)
            else:
                self.message("Please Select a Parent Location")
        else:
            self.message("Please Select a Location")


    def message(self,msg1, msg2=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText(msg1+"\n"+msg2)
        msg.exec_()

    def clearAll(self):
        self.ui.locationBox.setCurrentIndex(0)
        self.ui.newParentLocationBox.setCurrentIndex(0)

    def closeEvent(self):
        self.ui.close()

if __name__ == '__main__':
    setproctitle.setproctitle("MODIFY_LOCATION")
    app = QtWidgets.QApplication(sys.argv)
    window = modifyWidget()
    sys.exit(app.exec_())

