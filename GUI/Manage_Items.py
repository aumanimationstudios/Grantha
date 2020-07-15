#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import dbGrantha
import string
import random
from collections import OrderedDict
import zmq
import debug
import subprocess
from Utils_Gui import *
import glob
import json
import setproctitle
import time
import argparse

filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")

sys.path.append(uiDir)
sys.path.append(imageDir)

context = zmq.Context()

imagePicsDir = "/blueprod/STOR2/stor2/grantha/share/pics/"
imageTempDir = "/blueprod/STOR2/stor2/grantha/share/temp/"

# vLayImages = QtWidgets.QVBoxLayout()
# hLayImages = QtWidgets.QHBoxLayout()
imageNames = {}

parser = argparse.ArgumentParser(description="Utility to manage items")
parser.add_argument("-s","--serialno",dest="serialno",help="serial number")
args = parser.parse_args()


class manageItemsWidget():
    # db = database.DataBase()
    db = dbGrantha.dbGrantha()

    getSN = "SELECT * FROM SERIAL_NO"
    getIT = "SELECT * FROM ITEM_TYPE"
    getDESC = "SELECT * FROM DESCRIPTION"
    getMK = "SELECT * FROM MAKE"
    getMDL = "SELECT * FROM MODEL"
    getLOC = "SELECT location FROM LOCATION WHERE location NOT LIKE 'REPAIR' "
    getUSR = "SELECT * FROM USER"

    sn = db.execute(getSN,dictionary=True)
    slNoList = [x['serial_no'] for x in sn]

    # getSN = "SELECT * FROM SERIAL_NO"
    # self.sn = self.db.execute(getSN, dictionary=True)
    # self.slNoList = [x['serial_no'] for x in self.sn]
    #
    it = db.execute(getIT,dictionary=True)
    itemTypeList = [x['item_type'] for x in it]

    desc = db.execute(getDESC,dictionary=True)
    descriptionList = [x['description'] for x in desc]

    mk = db.execute(getMK,dictionary=True)
    makeList = [x['make'] for x in mk]

    mdl = db.execute(getMDL,dictionary=True)
    modelList = [x['model'] for x in mdl]

    loc = db.execute(getLOC,dictionary=True)
    locationList = [x['location'] for x in loc]

    usr = db.execute(getUSR,dictionary=True)
    userList = [x['user'] for x in usr]

    # layout = QVBoxLayout()


    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiDir, 'Manage_Items.ui'))
        # self.ui = uic.loadUi(os.path.join(projDir, "Test", 'Manage_Items_Test.ui'))

        # self.db = database.DataBase()
        self.ui.hideButton.hide()
        # self.ui.imagesFrame.hide()
        self.ui.listWidget.hide()


        # self.ui.frame.setLayout(self.layout)
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


        self.ui.imageCheckBox.clicked.connect(self.enableImageBox)
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

        self.ui.captureButton.clicked.connect(self.captureImage)
        self.ui.loadButton.clicked.connect(self.loadImage)
        self.ui.hideButton.clicked.connect(self.hideImage)
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

        if args.serialno:
            self.ui.serialNoBox.setEditText(str(args.serialno))
            self.loadDetails()

        self.ui.setWindowTitle('Manage Items')
        self.ui.purchaseCal.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.validCal.setIcon(QtGui.QIcon(os.path.join(imageDir, 'cal.png')))
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))
        self.center()
        self.ui.show()
        # self.ui.resize(656,500)
        self._contract()
        self.ui.cancelButton.clicked.connect(self.closeEvent)

        try:
            theme = os.environ['GRANTHA_THEME']
            debug.info(theme)
            setStyleSheet(self.ui, theme)
        except:
            pass

    def enableCheckBoxes(self):
        self.hideImage()
        self.loadDetails()
        self.ui.imageCheckBox.setEnabled(True)
        self.ui.serialNoCheckBox.setEnabled(True)
        # self.ui.tagIdCheckBox.setEnabled(True)
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
        # self.ui.frame.setEnabled(False)
        self.ui.imageBox.setEnabled(False)
        self.ui.captureButton.setEnabled(False)
        self.ui.loadButton.setEnabled(False)
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
        self.hideImage()
        self.loadDetails()
        self.ui.imageCheckBox.setEnabled(False)
        # self.ui.frame.setEnabled(True)
        self.ui.imageCheckBox.setEnabled(False)
        self.ui.imageCheckBox.setChecked(False)
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

        self.ui.imageBox.setEnabled(True)
        self.ui.captureButton.setEnabled(True)
        self.ui.loadButton.setEnabled(True)
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
        self.hideImage()
        self.disableCheckboxes()
        self.disableItToUsrBoxes()

    def enableImageBox(self):
        if (self.ui.imageCheckBox.isChecked()):
            self.ui.imageBox.setEnabled(True)
            self.ui.captureButton.setEnabled(True)
            self.ui.loadButton.setEnabled(True)
            self.ui.hideButton.setEnabled(True)
        else:
            self.ui.imageBox.setEnabled(False)
            self.ui.captureButton.setEnabled(False)
            self.ui.loadButton.setEnabled(False)
            self.ui.hideButton.setEnabled(False)

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

    def center(self):
        qr = self.ui.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        debug.info(cp)
        # qr.moveCenter(cp)
        qr.moveCenter(QtCore.QPoint(cp.x(), 250))
        self.ui.move(qr.topLeft())

    def load(self):
        # getSN = "SELECT * FROM SERIAL_NO"
        # self.sn = self.db.execute(getSN, dictionary=True)
        # self.slNoList = [x['serial_no'] for x in self.sn]
        self.slNoList.sort()
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

        self.clearAll()

    def convert_keys_to_string(self,dictionary):
        """Recursively converts dictionary keys to strings."""
        if not isinstance(dictionary, dict):
            return dictionary
        return dict((str(k), str(v))
            for k, v in dictionary.items())

    def loadImage(self):
        global imageNames
        slNo = str((self.ui.serialNoBox.currentText()).strip())
        # slNoDir = ""
        if slNo:
            slNoDir = imagePicsDir + slNo
        else:
            return
        if (self.ui.addButton.isChecked()):
            # self.ui.imageBox.clear()
            if imageNames:
                debug.info(imageNames)
                imageNames.clear()
            else:
                debug.info("no image names")


            # if slNo in self.slNoList:
            #     slNoDir = imagePicsDir + slNo
            # else:
            #     self.ui.imageBox.clear()
            #     slNoDir = imageTempDir + slNo

        elif (self.ui.updateButton.isChecked()):
            if slNo in self.slNoList:
            # slNoDir = imageTempDir + slNo
            # slNo = self.ui.serialNoBox.currentText().strip()
                getImages = "SELECT image FROM ITEMS WHERE serial_no='%s' " % (slNo)
                # details = self.db.getDetails(query)
                im = self.db.execute(getImages, dictionary=True)
                imFDb = [x['image'] for x in im][0].replace("\'", "\"")
                debug.info(imFDb)
                imageFrmDb = {}
                try:
                    imageFrmDb = json.loads(imFDb)
                except:
                    debug.info(str(sys.exc_info()))
                debug.info(imageFrmDb)
                debug.info(self.convert_keys_to_string(imageFrmDb))
                # imageNames = imageFrmDb
                imageNames = self.convert_keys_to_string(imageFrmDb)
        # self.ui.resize(656,800)

        # self.widget = QtWidgets.QWidget()
        # vLay = QtWidgets.QVBoxLayout()
        # self.widget.setLayout(vLay)

        # imageListUi = uic.loadUi(os.path.join(projDir,"Test", "imageList.ui"))
        # slNo = str((self.ui.serialNoBox.currentText()).strip())
        # slNoDir = imageTempDir + slNo
        # formats = ("jpg","png")
        images = []
        # for format in formats:
        #     images.extend(glob.glob(slNoDir.rstrip(os.sep) + os.sep + "*.%s" % format))
        # (_, _, filenames) = next(os.walk(slNoDir))
        if os.path.exists(slNoDir):
            (dirpath, dirnames, filenames) = next(os.walk(slNoDir))
            images.extend(os.path.join(dirpath, filename) for filename in filenames)
            images.sort()

        debug.info(images)
        # vLayImages = QtWidgets.QVBoxLayout()
        # self.ui.imagesFrame.setLayout(vLayImages)
        # for i in reversed(range(hLayImages.count())):
        #     hLayImages.itemAt(i).widget().setParent(None)
        if images:
            self._expand()
            self.ui.listWidget.show()
            self.ui.listWidget.clear()
            for i in images:
                label = (i.split(os.sep)[-1:][0]).split('.')[0]
                debug.info(label)
                checkbox = QtWidgets.QCheckBox(i)
                checkbox.setText(label)
                if label in imageNames.keys():
                    # checkbox.setEnabled(False)
                    checkbox.setChecked(True)
                # checkbox.clicked.connect(self.addImageNames)
                checkbox.clicked.connect(lambda x, button=checkbox,image=i: self.addImageNames(button,image))

                # imageListUi.verticalLayout.addWidget(checkbox)
                # vLay.addWidget(checkbox)
                # vLayImages.addWidget(checkbox)

                imageThumb = ImageWidget(i, 32)
                imageThumb.clicked.connect(lambda x, imagePath=i: imageWidgetClicked(imagePath))

                itemWidget = QtWidgets.QWidget()
                hl = QtWidgets.QHBoxLayout()
                itemWidget.setLayout(hl)
                hl.addWidget(checkbox)
                hl.addWidget(imageThumb)

                item = QListWidgetItemSort()
                item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
                self.ui.listWidget.addItem(item)
                self.ui.listWidget.setItemWidget(item,itemWidget)
            # textBox = QtWidgets.QTextEdit()
            # vLay.addWidget(textBox)
            # self.widget.resize(250,200)
            # self.widget.show()
            # setStyleSheet(self.widget)

            self.ui.loadButton.hide()
            self.ui.hideButton.show()
        # self.ui.imagesFrame.show()

        # self.widget = QWidget()
        # hLay = QHBoxLayout()
        # self.widget.setLayout(hLay)
        # treeView = QTreeView()
        # hLay.addWidget(treeView)
        # # imageDir = "/blueprod/STOR2/stor2/grantha/share/temp/"
        # self.dirModel = QFileSystemModel()
        # # self.dirModel.setRootPath(imageTempDir)
        # self.dirModel.setRootPath(slNoDir)
        # self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        # treeView.setModel(self.dirModel)
        # # treeView.setRootIndex(self.dirModel.index(imageTempDir))
        # treeView.setRootIndex(self.dirModel.index(slNoDir))
        # treeView.hideColumn(1)
        # treeView.hideColumn(2)
        # treeView.hideColumn(3)
        # treeView.clicked.connect(self.fileClicked)
        # self.widget.resize(250,400)
        # self.widget.show()

    def hideImage(self):
        self._contract()
        # self.ui.resize(656,500)
        self.ui.hideButton.hide()
        # self.ui.imagesFrame.hide()
        self.ui.loadButton.show()
        self.ui.listWidget.hide()

    def addImageNames(self, button,image):
        if button.isChecked():
            imageNames[str(button.text())] = str(image)
            debug.info(imageNames)
            # imageNames.append(str(button.text()))
            # imNStr = "  :  ".join(x.split('.')[0] for x in imageNames)
            imNStr = "  :  ".join((x) for x in imageNames.keys())
            # for iL in imageNames.keys():
            #     self.ui.imageBox.setText(iL)
            self.ui.imageBox.setText(imNStr)

        else:
            try:
                del imageNames[str(button.text())]
            except:
                (debug.info(str(sys.exc_info())))
            debug.info(imageNames)
            imNStr = "  :  ".join((x) for x in imageNames.keys())
            # for iL in imageNames.keys():
            #     self.ui.imageBox.setText(iL)
            self.ui.imageBox.setText(imNStr)
            # imageNames.remove(str(button.text()))
            # # imNStr = ",".join(imageNames)
            # imNStr = "  :  ".join(x.split('.')[0] for x in imageNames)
            # self.ui.imageBox.setText(imNStr)
            pass

    def _expand(self):
        self.ui.resize(656, 786)

    def _contract(self):
        self.ui.resize(656, 500)

    # def fileClicked(self, index):
    #     path = (self.dirModel.fileInfo(index).absoluteFilePath()).strip()
    #     debug.info(path)
    #     imageName = str(path.split(os.sep)[-1:][0])
    #     finalPath = imagePicsDir+imageName
    #     debug.info(finalPath)
    #     self.ui.imageBox.clear()
    #     self.ui.imageBox.setText(finalPath)
    #
    #     self.widget.close()
    #     self.setImageThumb(path,clickable=True)
    #     # for i in reversed(range(self.layout.count())):
    #     #     self.layout.itemAt(i).widget().setParent(None)
    #     # imageThumb = ImageWidget(path, 32)
    #     # imageThumb.clicked.connect(lambda x, imagePath = path: imageWidgetClicked(imagePath))
    #     # self.layout.addWidget(imageThumb)


    def captureImage(self):
        slNo = str((self.ui.serialNoBox.currentText()).strip())
        if not slNo:
            try:
                messageBox("Please Provide a Serial No")
            except:
                debug.info(str(sys.exc_info()))
        else:
            # subprocess.Popen(["python", "Pi_Camera_Preview.py", slNo])
            cT = captureThread(app)
            # cT.waiting.connect(self.openPlaceTagMessage)
            cT.ackReceived.connect(self.showTimerMsg)
            cT.start()

    def showTimerMsg(self, msg):
        messagebox = TimerMessageBox(1, msg)
        messagebox.exec_()
        slNo = str((self.ui.serialNoBox.currentText()).strip())
        # slNoDir = imageTempDir+slNo
        slNoDir = imagePicsDir+slNo
        cmd = "mkdir "+ slNoDir
        debug.info(cmd)
        if os.path.exists(slNoDir):
            debug.info("Folder exists " + slNoDir)
        else:
            try:
                os.system(cmd)
            except:
                debug.info(str(sys.exc_info()))
        subprocess.Popen(["python", os.path.join(projDir, "GUI", "Pi_Camera_Preview.py"), slNo])

    def loadDetails(self):
        if self.ui.updateTagButton.isChecked():
            pass
        else:
            slNo = self.ui.serialNoBox.currentText().strip()
            # print slNo
            self.hideImage()

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
            self.ui.imageBox.clear()


    def slNoGenerator(self, size=10, chars=string.ascii_uppercase + string.digits):
        slNo = ''.join(random.SystemRandom().choice(chars) for n in range(size))
        return slNo


    def readFromRfidTag(self):
        rT = readThread(app)
        rT.waiting.connect(self.msg)
        rT.tagIdReceived.connect(self.closePlaceTagMessage)
        rT.start()

    def msg(self, plceMsg):
        messagebox = TimerMessageBox(1, plceMsg)
        messagebox.exec_()


    def closePlaceTagMessage(self, tagId):
        try:
            debug.info("Message Closed")
            # self.plcMsg.close()
        except:
            debug.info(str(sys.exc_info()))
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
        slNo = self.ui.serialNoBox.currentText().strip()
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

        imagePaths = {}
        try:
            imagePaths = json.loads(details["image"].replace("\'", "\""))
        except:
            debug.info(str(sys.exc_info()))
        debug.info(imagePaths)

        self.ui.imageBox.clear()
        self.ui.imageBox.setText("  :  ".join((str(x)) for x in imagePaths.keys()))
        # debug.info(path)

        # for i in reversed(range(self.layout.count())):
        #     self.layout.itemAt(i).widget().setParent(None)
        # if path:
        #     self.setImageThumb(path,clickable=True)
        #     # imageThumb = ImageWidget(path, 32)
        #     # imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
        #     # self.layout.addWidget(imageThumb)
        # else:
        #     path = os.path.join(imageDir, "image.png")
        #     self.setImageThumb(path)
            # imageThumb = ImageWidget(path, 32)
            # self.layout.addWidget(imageThumb)

    def purchaseNone(self):
        self.ui.purchaseBox.setText("0000-00-00")

    def validNone(self):
        self.ui.validBox.setText("0000-00-00")

    def locationNone(self):
        self.ui.locationBox.setCurrentIndex(0)

    def userNone(self):
        self.ui.userBox.setCurrentIndex(0)

    def clearAll(self):
        # path = os.path.join(imageDir, "image.png")
        # self.setImageThumb(path)
        # for i in reversed(range(self.layout.count())):
        #     self.layout.itemAt(i).widget().setParent(None)
        # imageThumb = ImageWidget(path, 32)
        # # imageThumb.clicked.connect(lambda x, imagePath = path: imageWidgetClicked(imagePath))
        # self.layout.addWidget(imageThumb)
        imageNames.clear()
        self.hideImage()
        self.ui.imageBox.clear()
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
            setStyleSheet(confirm)
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
        userInput["item_type"] = str(self.ui.itemTypeBox.currentText().strip())
        userInput["description"] = str(self.ui.descriptionBox.currentText().strip())
        userInput["make"] = str(self.ui.makeBox.currentText().strip())
        userInput["model"] = str(self.ui.modelBox.currentText().strip())
        userInput["price"] = str(self.ui.priceBox.text().strip())
        userInput["purchased_on"] = str(self.ui.purchaseBox.text().strip())
        userInput["warranty_valid_till"] = str(self.ui.validBox.text().strip())
        userInput["location"] = str(self.ui.locationBox.currentText().strip())
        userInput["user"] = str(self.ui.userBox.currentText().strip())
        userInput["image"] = str(imageNames)

        keys = []
        values = []
        for key in userInput.keys():
            keys.append(key)
            values.append(userInput[key])

        slNo = userInput["serial_no"]
        # imagePath = userInput["image"]

        queryAddItem = "INSERT INTO ITEMS (" + ','.join(keys) + ") VALUES %r" %(tuple(values),)

        debug.info(queryAddItem)
        if slNo:
            if slNo in self.slNoList:
                messageBox("Sl No exists!!!")
                return

            tagId = str(self.ui.tagIdBox.text().strip())
            if tagId:
                queryAddSlNo = "INSERT INTO SERIAL_NO (serial_no, tag_id) VALUES (\"{0}\",\"{1}\") ".format(slNo,tagId)
            else:
                queryAddSlNo = "INSERT INTO SERIAL_NO (serial_no) VALUES (\"{0}\") ".format(slNo)
            debug.info(queryAddSlNo)

            addSlNo = self.db.execute(queryAddSlNo)
            debug.info(addSlNo)

            if (addSlNo == 1):
                # addItem = self.db.insertItem(queryAddItem)
                addItem = self.db.execute(queryAddItem)
                if (addItem == 1):
                    logAdded = self.addUpdateLog("Add", ",".join(str(key) +"=\""+ str(userInput[key]) +"\"" for key in userInput.keys()))
                    if (logAdded == 1):
                    # slNoDir = imagePicsDir + slNo
                    # mkSlDirCmd = "mkdir " + slNoDir
                    # debug.info(mkSlDirCmd)
                    # if os.path.exists(slNoDir):
                    #     debug.info("Folder exists " + slNoDir)
                    # else:
                    #     try:
                    #         os.system(mkSlDirCmd)
                    #     except:
                    #         debug.info(str(sys.exc_info()))

                    # if imageNames:
                    #     debug.info(imageNames)
                    #     for i in imageNames.values():
                    #         mvCmd = "rsync -av " + i + " " + slNoDir + os.sep
                    #         if os.path.exists(i) and os.path.exists(slNoDir):
                    #             debug.info(mvCmd)
                    #             os.system(mvCmd)
                    # else:
                    #     pass
                        messageBox("Item Added Successfully", "Serial No added successfully")
                        self.load()
                    else:
                        messageBox("Log add failed")
                else:
                    queryRemoveSlNo = "DELETE FROM SERIAL_NO WHERE serial_no=\"{0}\"".format(slNo)
                    debug.info(queryRemoveSlNo)
                    deleteSlNo = self.db.execute(queryRemoveSlNo)
                    if (deleteSlNo == 1):
                        messageBox("<b>Item Not Added.</b>", addItem)
            else:
                messageBox("<b>Item Not Added.</b>",addSlNo)
        else:
            messageBox("<b>Input a Serial Number</b>")

    def update(self):
        debug.info("update")
        userInput = {}

        # if (self.ui.serialNoCheckBox.isChecked()):
        slNo =  str(self.ui.serialNoBox.currentText().strip())
        debug.info(slNo)

        if (self.ui.imageCheckBox.isChecked()):
            # userInput["image"] = str(self.ui.imageBox.text().strip())
            userInput["image"] = str(imageNames)
        if (self.ui.itemTypeCheckBox.isChecked()):
            userInput["item_type"] = str(self.ui.itemTypeBox.currentText().strip())
        if (self.ui.descriptionCheckBox.isChecked()):
            userInput["description"] = str(self.ui.descriptionBox.currentText().strip())
        if (self.ui.makeCheckBox.isChecked()):
            userInput["make"] = str(self.ui.makeBox.currentText().strip())
        if (self.ui.modelCheckBox.isChecked()):
            userInput["model"] = str(self.ui.modelBox.currentText().strip())
        if (self.ui.priceCheckBox.isChecked()):
            userInput["price"] = str(self.ui.priceBox.text().strip())
        if (self.ui.purchaseCheckBox.isChecked()):
            userInput["purchased_on"] = str(self.ui.purchaseBox.text().strip())
        if (self.ui.validCheckBox.isChecked()):
            userInput["warranty_valid_till"] = str(self.ui.validBox.text().strip())
        if (self.ui.locationCheckBox.isChecked()):
            userInput["location"] = str(self.ui.locationBox.currentText().strip())
        if (self.ui.userCheckBox.isChecked()):
            userInput["user"] = str(self.ui.userBox.currentText().strip())

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
                logUpdated = self.addUpdateLog("Update",",".join(dbvalues))
                if (logUpdated == 1):
                # slNoDir = imagePicsDir + slNo
                # mkSlDirCmd = "mkdir " + slNoDir
                # debug.info(mkSlDirCmd)
                # if os.path.exists(slNoDir):
                #     debug.info("Folder exists " + slNoDir)
                # else:
                #     try:
                #         os.system(mkSlDirCmd)
                #     except:
                #         debug.info(str(sys.exc_info()))
                #
                # if imageNames:
                #     debug.info(imageNames)
                #     for i in imageNames.values():
                #         mvCmd = "rsync -av " + i + " " + slNoDir + os.sep
                #         if os.path.exists(i) and os.path.exists(slNoDir):
                #             debug.info(mvCmd)
                #             os.system(mvCmd)
                # if imageNames:
                #     debug.info(imageNames)
                #     slNoTempDir = imageTempDir + slNo
                #     for i in imageNames:
                #         mvCmd = "rsync -av " + slNoTempDir + os.sep + i + " " + slNoDir + os.sep
                #         if os.path.exists(slNoTempDir) and os.path.exists(slNoDir):
                #             debug.info(mvCmd)
                #             os.system(mvCmd)
                # else:
                #     pass
                    messageBox("Updated Successfully")
                else:
                    messageBox("Log Update Failed")
            else:
                messageBox("<b>Update failed</b>")
        if not dbvalues:
            messageBox("<b>Update failed</b>","Select fields to update")
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
                    logTagUpdated = self.addUpdateLog("Update_Tag", "tag_id" +"=\""+ tagId +"\"")
                    if (logTagUpdated == 1):
                        messageBox("Updated Successfully")
                        self.load()
                    else:
                        messageBox("Log Update failed")
                else:
                    messageBox("<b>Update failed</b>",updated)
            else:
                messageBox("<b>Update failed</b>","Scan a tag and proceed")
        else:
            messageBox("<b>Update failed</b>","Select a serial number and proceed")

    def addUpdateLog(self,action,details):
        log = OrderedDict()

        log["date"] = time.strftime('%Y-%m-%d %H:%M:%S')
        log["serial_no"] = str(self.ui.serialNoBox.currentText().strip())
        log["user"] = os.environ['USER']
        log["action"] = action + ": " + details

        # debug.info(log["action"])

        logValues = []
        for key in log.keys():
            logValues.append(log[key])
        columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'add_update_log' \
                       AND COLUMN_NAME NOT IN ('no')"
        column = self.db.execute(columnQuery, dictionary=True)
        self.logColumn = [x['COLUMN_NAME'] for x in column]
        LogQuery = "INSERT INTO add_update_log (" + ','.join(self.logColumn) + ") VALUES %r" % (tuple(logValues),)
        logAddUpdate = self.db.execute(LogQuery)
        return logAddUpdate

    # def setImageThumb(self,path,clickable=False):
    #     for i in reversed(range(self.layout.count())):
    #         self.layout.itemAt(i).widget().setParent(None)
    #     imageThumb = ImageWidget(path, 32)
    #     if clickable:
    #         imageThumb.clicked.connect(lambda x, imagePath = path: imageWidgetClicked(imagePath))
    #     self.layout.addWidget(imageThumb)

    def closeEvent(self):
        self.ui.close()



class readThread(QThread):
    waiting = pyqtSignal(str)
    tagIdReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(readThread, self).__init__(parent)

    def run(self):
        self.waiting.emit("Place your tag...")

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


class captureThread(QThread):
    # waiting = pyqtSignal()
    ackReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(captureThread, self).__init__(parent)
        # self.slNo = slNo

    def run(self):
        # self.waiting.emit()

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
            debug.info("connected.")
        except:
            debug.info(str(sys.exc_info()))
        self.socket.send_multipart(["START_CAMERA_PREVIEW"])

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        try:
            ack = self.socket.recv()
            debug.info(ack)
            self.ackReceived.emit(ack)
        except:
            debug.info(str(sys.exc_info()))

        self.socket.close()

        if (self.socket.closed == True):
            debug.info("Capture Socket closed.")

class QListWidgetItemSort(QtWidgets.QListWidgetItem):

  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)

if __name__ == '__main__':
    setproctitle.setproctitle("MANAGE_ITEMS")
    app = QtWidgets.QApplication(sys.argv)
    window = manageItemsWidget()
    sys.exit(app.exec_())

