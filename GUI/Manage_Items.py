#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
import database
import dbGrantha
import string
import random
from collections import OrderedDict
import zmq
import debug

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

context = zmq.Context()

class addWidget():
    # db = database.DataBase()
    db = dbGrantha.dbGrantha()

    getSN = "SELECT * FROM SERIAL_NO"
    getIT = "SELECT * FROM ITEM_TYPE"
    getDESC = "SELECT * FROM DESCRIPTION"
    getMK = "SELECT * FROM MAKE"
    getMDL = "SELECT * FROM MODEL"
    getLOC = "SELECT location FROM LOCATION"
    getUSR = "SELECT * FROM USER"

    # sn = db.listOfSerialNo()
    sn = db.execute(getSN,dictionary=True)
    slNoList = [x['serial_no'] for x in sn]
    # it = db.listOfItemType()
    it = db.execute(getIT,dictionary=True)
    itemTypeList = [x['item_type'] for x in it]
    # desc = db.listOfDescription()
    desc = db.execute(getDESC,dictionary=True)
    descriptionList = [x['description'] for x in desc]
    # mk = db.listOfMake()
    mk = db.execute(getMK,dictionary=True)
    makeList = [x['make'] for x in mk]
    # mdl = db.listOfModel()
    mdl = db.execute(getMDL,dictionary=True)
    modelList = [x['model'] for x in mdl]
    # loc = db.listOfLocation()
    loc = db.execute(getLOC,dictionary=True)
    locationList = [x['location'] for x in loc]
    # usr = db.listOfUser()
    usr = db.execute(getUSR,dictionary=True)
    userList = [x['user'] for x in usr]

    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Manage_Items.ui'))

        # self.db = database.DataBase()

        self.load()
        self.ui.serialNoBox.setCurrentText(" ")
        self.ui.itemTypeBox.setCurrentText(" ")
        self.ui.priceBox.setText('0.00')

        if self.ui.addButton.isChecked():
            self.disableCheckboxes()

        if self.ui.updateButton.isChecked():
            self.enableCheckBoxes()

        self.ui.addButton.pressed.connect(self.disableCheckboxes)
        self.ui.updateButton.pressed.connect(self.enableCheckBoxes)
        self.ui.updateTagButton.pressed.connect(self.disableCheckboxesAndBoxes)


        self.ui.serialNoCheckBox.clicked.connect(self.enableSerialNoBox)
        self.ui.tagIdCheckBox.clicked.connect(self.enableTagIdBox)
        self.ui.itemTypeCheckBox.clicked.connect(self.enableItemTypeBox)
        self.ui.descriptionCheckBox.clicked.connect(self.enableDescriptionBox)
        self.ui.makeCheckBox.clicked.connect(self.enableMakeBox)
        self.ui.modelCheckBox.clicked.connect(self.enableModelBox)
        self.ui.priceCheckBox.clicked.connect(self.enablePriceBox)
        self.ui.purchaseCheckBox.clicked.connect(self.enablePurchaseBox)
        self.ui.validCheckBox.clicked.connect(self.enableValidBox)
        self.ui.locationCheckBox.clicked.connect(self.enableLocationBox)
        self.ui.userCheckBox.clicked.connect(self.enableUserBox)

        self.ui.serialNoBox.currentIndexChanged.connect(self.loadDetails)
        self.ui.generateButton.clicked.connect(self.slNoGen)
        self.ui.readButton.clicked.connect(self.readFromRfidTag)
        self.ui.purchaseCal.clicked.connect(self.showPurchaseCal)
        self.ui.validCal.clicked.connect(self.showValidCal)
        self.ui.purchaseNoneButton.clicked.connect(self.purchaseNone)
        self.ui.validNoneButton.clicked.connect(self.validNone)
        self.ui.locationNoneButton.clicked.connect(self.locationNone)
        self.ui.userNoneButton.clicked.connect(self.userNone)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.saveButton.clicked.connect(self.confirmation)

        self.ui.setWindowTitle('Manage Items')
        self.ui.purchaseCal.setIcon(QtGui.QIcon(os.path.join(imgFilePath, 'cal.png')))
        self.ui.validCal.setIcon(QtGui.QIcon(os.path.join(imgFilePath, 'cal.png')))
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.closeEvent)


    def enableCheckBoxes(self):
        self.ui.serialNoCheckBox.setEnabled(True)
        self.ui.tagIdCheckBox.setEnabled(True)
        self.ui.itemTypeCheckBox.setEnabled(True)
        self.ui.descriptionCheckBox.setEnabled(True)
        self.ui.makeCheckBox.setEnabled(True)
        self.ui.modelCheckBox.setEnabled(True)
        self.ui.priceCheckBox.setEnabled(True)
        self.ui.purchaseCheckBox.setEnabled(True)
        self.ui.validCheckBox.setEnabled(True)
        self.ui.locationCheckBox.setEnabled(True)
        self.ui.userCheckBox.setEnabled(True)

        self.ui.serialNoBox.setEnabled(False)
        self.ui.tagIdBox.setEnabled(False)
        self.ui.readButton.setEnabled(False)
        self.disableItToUsrBoxes()

    def disableItToUsrBoxes(self):
        self.ui.itemTypeBox.setEnabled(False)
        self.ui.descriptionBox.setEnabled(False)
        self.ui.makeBox.setEnabled(False)
        self.ui.modelBox.setEnabled(False)
        self.ui.priceBox.setEnabled(False)
        self.ui.purchaseBox.setEnabled(False)
        self.ui.validBox.setEnabled(False)
        self.ui.locationBox.setEnabled(False)
        self.ui.userBox.setEnabled(False)
        self.ui.generateButton.setEnabled(False)
        self.ui.purchaseCal.setEnabled(False)
        self.ui.validCal.setEnabled(False)
        self.ui.purchaseNoneButton.setEnabled(False)
        self.ui.validNoneButton.setEnabled(False)
        self.ui.locationNoneButton.setEnabled(False)
        self.ui.userNoneButton.setEnabled(False)


    def disableCheckboxes(self):
        self.ui.serialNoCheckBox.setEnabled(False)
        self.ui.serialNoCheckBox.setChecked(False)
        self.ui.tagIdCheckBox.setEnabled(False)
        self.ui.tagIdCheckBox.setChecked(False)
        self.ui.itemTypeCheckBox.setEnabled(False)
        self.ui.itemTypeCheckBox.setChecked(False)
        self.ui.descriptionCheckBox.setEnabled(False)
        self.ui.descriptionCheckBox.setChecked(False)
        self.ui.makeCheckBox.setEnabled(False)
        self.ui.makeCheckBox.setChecked(False)
        self.ui.modelCheckBox.setEnabled(False)
        self.ui.modelCheckBox.setChecked(False)
        self.ui.priceCheckBox.setEnabled(False)
        self.ui.priceCheckBox.setChecked(False)
        self.ui.purchaseCheckBox.setEnabled(False)
        self.ui.purchaseCheckBox.setChecked(False)
        self.ui.validCheckBox.setEnabled(False)
        self.ui.validCheckBox.setChecked(False)
        self.ui.locationCheckBox.setEnabled(False)
        self.ui.locationCheckBox.setChecked(False)
        self.ui.userCheckBox.setEnabled(False)
        self.ui.userCheckBox.setChecked(False)

        self.ui.serialNoBox.setEnabled(True)
        self.ui.tagIdBox.setEnabled(True)
        self.ui.itemTypeBox.setEnabled(True)
        self.ui.descriptionBox.setEnabled(True)
        self.ui.makeBox.setEnabled(True)
        self.ui.modelBox.setEnabled(True)
        self.ui.priceBox.setEnabled(True)
        self.ui.purchaseBox.setEnabled(True)
        self.ui.validBox.setEnabled(True)
        self.ui.locationBox.setEnabled(True)
        self.ui.userBox.setEnabled(True)
        self.ui.generateButton.setEnabled(True)
        self.ui.readButton.setEnabled(True)
        self.ui.purchaseCal.setEnabled(True)
        self.ui.validCal.setEnabled(True)
        self.ui.purchaseNoneButton.setEnabled(True)
        self.ui.validNoneButton.setEnabled(True)
        self.ui.locationNoneButton.setEnabled(True)
        self.ui.userNoneButton.setEnabled(True)

    def disableCheckboxesAndBoxes(self):
        self.disableCheckboxes()
        self.disableItToUsrBoxes()

    def enableSerialNoBox(self):
        if (self.ui.serialNoCheckBox.isChecked()):
            self.ui.serialNoBox.setEnabled(True)
            # self.ui.generateButton.setEnabled(True)
        else:
            self.ui.serialNoBox.setEnabled(False)
            # self.ui.generateButton.setEnabled(False)

    def enableTagIdBox(self):
        if (self.ui.tagIdCheckBox.isChecked()):
            self.ui.tagIdBox.setEnabled(True)
            self.ui.readButton.setEnabled(True)
        else:
            self.ui.tagIdBox.setEnabled(False)
            self.ui.readButton.setEnabled(False)

    def enableItemTypeBox(self):
        if (self.ui.itemTypeCheckBox.isChecked()):
            self.ui.itemTypeBox.setEnabled(True)
        else:
            self.ui.itemTypeBox.setEnabled(False)

    def enableDescriptionBox(self):
        if (self.ui.descriptionCheckBox.isChecked()):
            self.ui.descriptionBox.setEnabled(True)
        else:
            self.ui.descriptionBox.setEnabled(False)

    def enableMakeBox(self):
        if (self.ui.makeCheckBox.isChecked()):
            self.ui.makeBox.setEnabled(True)
        else:
            self.ui.makeBox.setEnabled(False)

    def enableModelBox(self):
        if (self.ui.modelCheckBox.isChecked()):
            self.ui.modelBox.setEnabled(True)
        else:
            self.ui.modelBox.setEnabled(False)

    def enablePriceBox(self):
        if (self.ui.priceCheckBox.isChecked()):
            self.ui.priceBox.setEnabled(True)
        else:
            self.ui.priceBox.setEnabled(False)

    def enablePurchaseBox(self):
        if (self.ui.purchaseCheckBox.isChecked()):
            self.ui.purchaseBox.setEnabled(True)
            self.ui.purchaseCal.setEnabled(True)
            self.ui.purchaseNoneButton.setEnabled(True)
        else:
            self.ui.purchaseBox.setEnabled(False)
            self.ui.purchaseCal.setEnabled(False)
            self.ui.purchaseNoneButton.setEnabled(False)

    def enableValidBox(self):
        if (self.ui.validCheckBox.isChecked()):
            self.ui.validBox.setEnabled(True)
            self.ui.validCal.setEnabled(True)
            self.ui.validNoneButton.setEnabled(True)
        else:
            self.ui.validBox.setEnabled(False)
            self.ui.validCal.setEnabled(False)
            self.ui.validNoneButton.setEnabled(False)

    def enableLocationBox(self):
        if (self.ui.locationCheckBox.isChecked()):
            self.ui.locationBox.setEnabled(True)
            self.ui.locationNoneButton.setEnabled(True)
        else:
            self.ui.locationBox.setEnabled(False)
            self.ui.locationNoneButton.setEnabled(False)

    def enableUserBox(self):
        if (self.ui.userCheckBox.isChecked()):
            self.ui.userBox.setEnabled(True)
            self.ui.userNoneButton.setEnabled(True)
        else:
            self.ui.userBox.setEnabled(False)
            self.ui.userNoneButton.setEnabled(False)

    def load(self):
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(self.slNoList)

        self.ui.itemTypeBox.clear()
        self.ui.itemTypeBox.addItems(self.itemTypeList)

        self.ui.descriptionBox.clear()
        self.ui.descriptionBox.addItems(self.descriptionList)

        self.ui.makeBox.clear()
        self.ui.makeBox.addItems(self.makeList)

        self.ui.modelBox.clear()
        self.ui.modelBox.addItems(self.modelList)

        self.ui.locationBox.clear()
        self.ui.locationBox.addItems(self.locationList)

        self.ui.userBox.clear()
        self.ui.userBox.addItems(self.userList)

        self.ui.priceBox.setText('0.00')

    def loadDetails(self):
        if self.ui.updateTagButton.isChecked():
            pass
        else:
            slNo = self.ui.serialNoBox.currentText()
            # print slNo

            if slNo in self.slNoList:
                getTidFrmSl = "SELECT tag_id FROM SERIAL_NO WHERE serial_no=\"{}\" ".format(slNo)
                # tagid = self.db.getTidFrmSl(slNo)
                tagid = self.db.execute(getTidFrmSl,dictionary=True)
                tagid = tagid[0]
                tagId = tagid['tag_id']
                self.ui.tagIdBox.setText(tagId)
                self.fillDetails()
            else:
                self.clearAll()

    def slNoGen(self):
        slNo = self.slNoGenerator()

        if slNo in self.slNoList:
            self.slNoGen()
        else:
            self.ui.serialNoBox.setCurrentText(slNo)


    def slNoGenerator(self, size=10, chars=string.ascii_uppercase + string.digits):
        slNo = ''.join(random.SystemRandom().choice(chars) for n in range(size))
        return slNo


    def readFromRfidTag(self):
        rT = readThread(app)
        rT.waiting.connect(self.openPlaceTagMessage)
        rT.tagIdReceived.connect(self.closePlaceTagMessage)
        rT.start()

    def openPlaceTagMessage(self):
        self.plcMsg = QtWidgets.QMessageBox()
        self.plcMsg.setIcon(QtWidgets.QMessageBox.Information)
        self.plcMsg.setWindowTitle("Message")
        self.plcMsg.setText("Place your Tag...")
        self.plcMsg.show()

    def closePlaceTagMessage(self, tagId):
        try:
            self.plcMsg.close()
        except:
            pass
        self.clearAll()
        self.ui.tagIdBox.setText(tagId)
        # ti = self.db.listOfSerialNo()
        # TI = [x['tag_id'] for x in ti]
        TI = [x['tag_id'] for x in self.sn]
        if tagId in TI:
            getSlFrmTid = "SELECT serial_no FROM SERIAL_NO WHERE tag_id=\"{}\" ".format(tagId)
            # slno = self.db.getSlFrmTid(tagId)
            slno = self.db.execute(getSlFrmTid,dictionary=True)
            slno = slno[0]
            slNo = slno['serial_no']
            self.ui.serialNoBox.setCurrentText(slNo)
            self.fillDetails()
        else:
            pass



    def fillDetails(self):
        slNo = self.ui.serialNoBox.currentText()
        getDetails = "SELECT * FROM ITEMS WHERE serial_no='%s' " % (slNo)
        # details = self.db.getDetails(query)
        details = self.db.execute(getDetails,dictionary=True)
        details = details[0]
        debug.info (details)
        iT = details["item_type"]
        dSC = details["description"]
        mK = details["make"]
        mDL = details["model"]
        pR = str(details["price"])
        pD = str(details["purchased_on"])
        wD = str(details["warranty_valid_till"])
        lOC = details["location"]
        uSR = details["user"]

        self.ui.itemTypeBox.setCurrentText(iT)
        self.ui.descriptionBox.setCurrentText(dSC)
        self.ui.makeBox.setCurrentText(mK)
        self.ui.modelBox.setCurrentText(mDL)
        self.ui.priceBox.setText(pR)
        self.ui.purchaseBox.setText(pD)
        self.ui.validBox.setText(wD)
        self.ui.locationBox.setCurrentText(lOC)
        self.ui.userBox.setCurrentText(uSR)


    def purchaseNone(self):
        self.ui.purchaseBox.setText("0000-00-00")

    def validNone(self):
        self.ui.validBox.setText("0000-00-00")

    def locationNone(self):
        self.ui.locationBox.setCurrentIndex(0)

    def userNone(self):
        self.ui.userBox.setCurrentIndex(0)

    def clearAll(self):
        self.ui.serialNoBox.setCurrentText(" ")
        # self.ui.serialNoBox.setCurrentIndex(0)
        self.ui.tagIdBox.clear()
        self.ui.itemTypeBox.setCurrentText(" ")
        # self.ui.itemTypeBox.setCurrentIndex(0)
        self.ui.descriptionBox.setCurrentIndex(0)
        self.ui.makeBox.setCurrentIndex(0)
        self.ui.modelBox.setCurrentIndex(0)
        self.ui.priceBox.setText('0.00')
        self.purchaseNone()
        self.validNone()
        self.locationNone()
        self.userNone()
        # self.load()

    def showPurchaseCal(self):
        self.cal = QtWidgets.QCalendarWidget()
        self.cal.clicked.connect(self.updatePurchaseDate)
        self.cal.show()

    def showValidCal(self):
        self.cal = QtWidgets.QCalendarWidget()
        self.cal.clicked.connect(self.updateValidDate)
        self.cal.show()

    def updatePurchaseDate(self):
        date = self.cal.selectedDate().toString(QtCore.Qt.ISODate)
        self.ui.purchaseBox.setText(date)
        self.cal.close()

    def updateValidDate(self):
        date = self.cal.selectedDate().toString(QtCore.Qt.ISODate)
        self.ui.validBox.setText(date)
        self.cal.close()

    def confirmation(self):
        if (self.ui.addButton.isChecked()):
            confirm = QtWidgets.QMessageBox()
            confirm.setIcon(QtWidgets.QMessageBox.Question)
            confirm.setWindowTitle("Confirmation")
            confirm.setInformativeText("<b>Are you sure you want to add item?</b>")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            selection = confirm.exec_()
            if (selection == QtWidgets.QMessageBox.Ok):
                self.addNew()

        if (self.ui.updateButton.isChecked()):
            confirm = QtWidgets.QMessageBox()
            confirm.setIcon(QtWidgets.QMessageBox.Question)
            confirm.setWindowTitle("Confirmation")
            confirm.setInformativeText("<b>Are you sure you want to update item?</b>")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            selection = confirm.exec_()
            if (selection == QtWidgets.QMessageBox.Ok):
                self.update()

        if (self.ui.updateTagButton.isChecked()):
            confirm = QtWidgets.QMessageBox()
            confirm.setIcon(QtWidgets.QMessageBox.Question)
            confirm.setWindowTitle("Confirmation")
            confirm.setInformativeText("<b>Are you sure you want to update Tag?</b>")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            selection = confirm.exec_()
            if (selection == QtWidgets.QMessageBox.Ok):
                self.updateTag()


    def addNew(self):
        debug.info("add new")
        userInput = OrderedDict()

        userInput["serial_no"] = str(self.ui.serialNoBox.currentText().strip())
        userInput["item_type"] = str(self.ui.itemTypeBox.currentText())
        userInput["description"] = str(self.ui.descriptionBox.currentText())
        userInput["make"] = str(self.ui.makeBox.currentText())
        userInput["model"] = str(self.ui.modelBox.currentText())
        userInput["price"] = str(self.ui.priceBox.text())
        userInput["purchased_on"] = str(self.ui.purchaseBox.text())
        userInput["warranty_valid_till"] = str(self.ui.validBox.text())
        userInput["location"] = str(self.ui.locationBox.currentText())
        userInput["user"] = str(self.ui.userBox.currentText())

        keys = []
        values = []
        for key in userInput.keys():
            keys.append(key)
            values.append(userInput[key])
        # debug.info(keys)
        # debug.info(values)
        # column = self.db.getColumns()
        # theColumn = [x['COLUMN_NAME'] for x in column]
        # debug.info(theColumn)
        queryAddItem = "INSERT INTO ITEMS (" + ','.join(keys) + ") VALUES %r" %(tuple(values),)
        # debug.info(query)
        # queryAddItem = "INSERT INTO ITEMS (" + ','.join(theColumn) + ") VALUES %r" %(tuple(values),)
        debug.info(queryAddItem)
        slNo = userInput["serial_no"]
        if slNo:
            tagId = str(self.ui.tagIdBox.text())
            if tagId:
                queryAddSlNo = "INSERT INTO SERIAL_NO (serial_no, tag_id) VALUES (\"{0}\",\"{1}\") ".format(slNo,tagId)
            else:
                queryAddSlNo = "INSERT INTO SERIAL_NO (serial_no) VALUES (\"{0}\") ".format(slNo)
            debug.info(queryAddSlNo)
            # self.addItem = self.db.insertItem(queryAddItem)
            # self.db.insertSerialNo(queryAddSlNo)
            # print self.addItem
            # self.writeToTag = self.writeToRfidTag()

            # addItem = self.db.insertItem(queryAddItem)
            # addSlNo =self.db.insertSerialNo(queryAddSlNo)
            addSlNo = self.db.execute(queryAddSlNo)
            debug.info(addSlNo)

            if (addSlNo == 1):
                # addItem = self.db.insertItem(queryAddItem)
                addItem = self.db.execute(queryAddItem)
                if (addItem == 1):
                    self.message("Item Added Successfully", "Serial No added successfully")
                else:
                    queryRemoveSlNo = "DELETE FROM SERIAL_NO WHERE serial_no=\"{0}\"".format(slNo)
                    debug.info(queryRemoveSlNo)
                    deleteSlNo = self.db.execute(queryRemoveSlNo)
                    if (deleteSlNo == 1):
                        self.message("<b>Item Not Added.</b>", addItem)
            else:
                self.message("<b>Item Not Added.</b>",addSlNo)
        else:
            self.message("<b>Input a Serial Number</b>")

    def update(self):
        debug.info("update")
        userInput = {}

        # if (self.ui.serialNoCheckBox.isChecked()):
        slNo =  str(self.ui.serialNoBox.currentText())
        debug.info(slNo)

        if (self.ui.itemTypeCheckBox.isChecked()):
            userInput["item_type"] = str(self.ui.itemTypeBox.currentText())

        if (self.ui.descriptionCheckBox.isChecked()):
            userInput["description"] = str(self.ui.descriptionBox.currentText())
        if (self.ui.makeCheckBox.isChecked()):
            userInput["make"] = str(self.ui.makeBox.currentText())
        if (self.ui.modelCheckBox.isChecked()):
            userInput["model"] = str(self.ui.modelBox.currentText())
        if (self.ui.priceCheckBox.isChecked()):
            userInput["price"] = str(self.ui.priceBox.text())
        if (self.ui.purchaseCheckBox.isChecked()):
            userInput["purchased_on"] = str(self.ui.purchaseBox.text())
        if (self.ui.validCheckBox.isChecked()):
            userInput["warranty_valid_till"] = str(self.ui.validBox.text())
        if (self.ui.locationCheckBox.isChecked()):
            userInput["location"] = str(self.ui.locationBox.currentText())
        if (self.ui.userCheckBox.isChecked()):
            userInput["user"] = str(self.ui.userBox.currentText())

        # keys = []
        # values = []
        dbvalues = []
        for key in userInput:
            # keys.append(key)
            # values.append(userInput[key])
            dbvalues.append(str(key) +"=\""+ str(userInput[key]) +"\"")
        debug.info(dbvalues)
        if dbvalues:
            query = "UPDATE ITEMS SET " + ",".join(dbvalues) + " WHERE serial_no =\"" + slNo + "\""
            debug.info(query)
            # updated = self.db.update(query)
            updated = self.db.execute(query)
            debug.info(updated)
            if (updated == 1):
                self.message("Updated Successfully")
            else:
                self.message("<b>Update failed</b>")
        if not dbvalues:
            self.message("<b>Update failed</b>","Select fields to update")
        # debug.info(keys)
        # debug.info(values)
        # debug.info(query)

    def updateTag(self):
        slNo = str(self.ui.serialNoBox.currentText().strip())
        if slNo:
            tagId = str(self.ui.tagIdBox.text().strip())
            if tagId:
                query = "UPDATE SERIAL_NO SET tag_id=\"" + tagId +"\"  WHERE serial_no =\"" + slNo + "\""
                debug.info(query)
                # updated = self.db.update(query)
                updated = self.db.execute(query)
                debug.info(updated)
                if (updated == 1):
                    self.message("Updated Successfully")
                else:
                    self.message("<b>Update failed</b>",updated)
            else:
                self.message("<b>Update failed</b>","Scan a tag and proceed")
        else:
            self.message("<b>Update failed</b>","Select a serial number and proceed")

    def message(self,msg1, msg2=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText(msg1+"\n"+msg2)
        msg.exec_()

    # def writeToRfidTag(self):
    #     idText = self.ui.serialNoBox.text()
    #     wT = writeThread(app, idText)
    #     # wT.waiting.connect(self.openplaceTagMessage)
    #     # wT.confirmation.connect(self.closePlaceTagMessage)
    #     wT.start()

    # def insertMessage(self):
    #     insMsg = QtWidgets.QMessageBox()
    #     insMsg.setIcon(QtWidgets.QMessageBox.Information)
    #     insMsg.setWindowTitle("Message")
    #     insMsg.setText(self.addItem )#+" \n"+ self.writeToTag)
    #     insMsg.show()
        # msg.resize(0,0)
        # msg.about(msg,"Message", self.addItem)
    # def openplaceTagMessage(self):
    #     self.plcMsg = QtWidgets.QMessageBox()
    #     # self.plcMsg.setStandardButtons(self, 0)
    #     self.plcMsg.setIcon(QtWidgets.QMessageBox.Information)
    #     self.plcMsg.setWindowTitle("Message")
    #     self.plcMsg.setText("Place your Tag...")
    #     self.plcMsg.show()
    #
    # def closePlaceTagMessage(self, msg):
    #     # self.plcMsg.close()
    #     # self.insertMessage()
    #     self.plcMsg.setText(self.addItem + " \n"+ msg )
    #     self.load()

    def closeEvent(self):
        self.ui.close()

    # def okMessage(self):
    #     msgBox = QtWidgets.QMessageBox()
    #     msgBox.resize(0,0)
    #     msgBox.about(msgBox,"Confirmation","Item Added. \nSl.No: "+ self.ui.serialNoBox.text())


class readThread(QThread):
    waiting = pyqtSignal()
    tagIdReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(readThread, self).__init__(parent)

    def run(self):
        self.waiting.emit()

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
            debug.info("connected.")
        except:
            debug.info(str(sys.exc_info()))
        self.socket.send("READ")

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        try:
            tagId = self.socket.recv()
            debug.info("Received Tag Id :" + tagId)
            self.tagIdReceived.emit(tagId)
        except:
            debug.info(str(sys.exc_info()))

        self.socket.close()

        if (self.socket.closed == True):
            debug.info("read Single Socket closed.")



# class writeThread(QtCore.QThread):
#     # initiateWrite = QtCore.pyqtSignal()
#     # inputForWrite = QtCore.pyqtSignal()
#     waiting = QtCore.pyqtSignal()
#     confirmation = QtCore.pyqtSignal(str)
#
#     def __init__(self, parent, idText):
#         super(writeThread, self).__init__(parent)
#         self.idText = idText
#     def run(self):
#         self.waiting.emit()
#
#         self.context = zmq.Context()
#         debug.info("connecting to rfidScanServer...")
#         self.socket = self.context.socket(zmq.REQ)
#         self.socket.connect("tcp://192.168.1.183:4689")
#
#         self.socket.send("WRITE")
#
#         msgFrmServ = self.socket.recv()
#
#         if (msgFrmServ == "INPUT"):
#             text = str(self.idText)
#             self.socket.send(text)
#
#             msgFrmServ = self.socket.recv()
#             debug.info (msgFrmServ)
#             self.confirmation.emit(msgFrmServ)
#             # return msgFrmServ
        # print "Message from Server :" + msgFrmServ
        # self.socket.close()

    # def closeEvent(self):
    #     self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = addWidget()
    sys.exit(app.exec_())

