#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

### rfidUhfServer Script Should be running in machine connected to RFID Reader Module to use rfid options###

import os
import sys
import psutil
from PyQt5 import QtGui, QtWidgets, uic, QtCore, QtSvg
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
import dbGrantha
import zmq
import socket
import debug
import subprocess
from Utils_Gui import *
import time
import setproctitle
import tempfile
import xml.dom.minidom
import glob
import datetime
import json

filePath = os.path.abspath(__file__)
# debug.info(filePath)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")
fileDir = os.path.join(projDir, "GUI")

sys.path.append(uiDir)
sys.path.append(imageDir)
sys.path.append(fileDir)

# Path of side panel button scripts
Manage_Items = os.path.join(fileDir, "Manage_Items.py")
Rfid_Tools = os.path.join(fileDir, "Rfid_Tools.py")
# Update = "Update.py"
# Update_Tag = "Update_Tag.py"
Modify = os.path.join(fileDir, "Modify_Location.py")
Repair = os.path.join(fileDir, "Repair.py")
Log = os.path.join(fileDir, "Log.py")
Find_Tag = os.path.join(fileDir, "Find_Tag.py")

user = os.environ['USER']
context = zmq.Context()
processes = []
# tempDir = tempfile.gettempdir()
mapPath = os.path.join(imageDir, "map.svg")

authUsers = None
LOCS = None
locs = None
pLocs = None
theColumn = None
slList = None
itList = None
# locList = None
usrList = None
sn = None
blues = []

imagePicsDir = "/blueprod/STOR2/stor2/grantha/share/pics/"
# imageFormats = ("jpg", "png")

os.environ['QT_LOGGING_RULES'] = "qt5ct.debug=false"

hiddenColumns = ["serial_no","model","price","purchased_on","warranty_valid_till","user"]
# hiddenColumns = ["serial_no","item_type","description","make","model","price","purchased_on","warranty_valid_till","location","user","image"]

class mainWindow():
    global processes

    # Database query execution function
    db = dbGrantha.dbGrantha()

    def __init__(self):
        # super(myWindow, self).__init__()
        self.reloadVars()

        self.rfidMultiCount = 0
        self.rfidMultiUniqSlno = {}
        self.ui = uic.loadUi(os.path.join(uiDir,"Grantha.ui"))

        self.allBtnClick()
        # self.ui.mainSplitter.setSizes([50, 50])

        # lay = QtWidgets.QHBoxLayout()
        # self.ui.moreButtFrame.setLayout(lay)
        # horizontalSpacer = QtWidgets.QSpacerItem(400, 20)
        # lay.addItem(horizontalSpacer)
        #
        # for header in theColumn:
        #     butt = QtWidgets.QCheckBox(header)
        #     butt.setText(header)
        #     lay.addWidget(butt)
        #     if header not in hiddenColumns:
        #         butt.setChecked(True)
        #     else:
        #         butt.setChecked(False)
        #     butt.pressed.connect(lambda butt=butt: self.showHideColumns(butt))
        #     self.showHideColumnsInit(butt)
        #
        # lay.addItem(horizontalSpacer)
        #
        # self.ui.moreButtFrame.hide()


        layV = QtWidgets.QVBoxLayout()
        self.ui.filterFrame.setLayout(layV)
        filtLabel = QtWidgets.QLabel()
        filtLabel.setText("Filter:")
        layV.addWidget(filtLabel)
        for header in theColumn:
            butt = QtWidgets.QCheckBox(header)
            butt.setText(header)
            layV.addWidget(butt)
            if header not in hiddenColumns:
                butt.setChecked(True)
            else:
                butt.setChecked(False)
            butt.pressed.connect(lambda butt=butt: self.showHideColumns(butt))
            self.showHideColumnsInit(butt)
        # verticalSpacer = QtWidgets.QSpacerItem(20, 600)
        # layV.addItem(verticalSpacer)


        self.ui.mapButton.clicked.connect(self.viewMap)
        self.ui.moreButton.clicked.connect(self.moreView)
        self.ui.allButton.clicked.connect(self.allBtnClick)
        self.ui.serialNoButton.clicked.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.clicked.connect(self.itBtnClick)
        self.ui.locationButton.clicked.connect(self.locBtnClick)
        self.ui.userButton.clicked.connect(self.usrBtnClick)
        self.ui.reloadButton.clicked.connect(self.reloadBtnClick)
        self.ui.relaunchButton.clicked.connect(self.relaunch)

        self.ui.comboBox.currentIndexChanged.connect(self.search)

        if user in authUsers:
            self.ui.manageItemsButton.clicked.connect(self.manageItems)
            self.ui.rfidToolsButton.clicked.connect(self.rfidTools)
            # self.ui.updateButton.clicked.connect(self.update)
            # self.ui.updateTagButton.clicked.connect(self.updateTag)
            self.ui.modifyButton.clicked.connect(self.modify)
            self.ui.repairButton.clicked.connect(self.repair)
            self.ui.logButton.clicked.connect(self.log)
            self.ui.findTagButton.clicked.connect(self.findTag)
            self.ui.readSingleButton.clicked.connect(self.readFromRfidTag)
            self.ui.readMultiButton.clicked.connect(self.readMultiFromRfidTag)
            self.ui.stopReadButton.setEnabled(False)
            self.ui.stopReadButton.clicked.connect(self.stopRead)

        self.ui.setWindowTitle('GRANTHA')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))

        self.ui.tableWidget.customContextMenuRequested.connect(self.ItemPopUp)
        self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # self.ui.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        # self.ui.splitter.setStretchFactor(2,0.25)
        # self.ui.splitter.setSizes([900, 50])
        self.ui.tableSplitter.setSizes([800, 50])

        # self.ui.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # header = self.ui.tableWidget.horizontalHeader()
        # self.ui.tableWidget.setMaximumWidth(header.length())
        # self.ui.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setMap()
        self.center()
        self.ui.showMaximized()

        # setStyleSheet(self.ui)
        Themes = ["dark", "light", "default"]
        self.ui.themeBox.addItems(Themes)
        self.changeStyleSheet()
        self.ui.themeBox.currentIndexChanged.connect(self.changeStyleSheet)

    def changeStyleSheet(self):
        ui = self.ui
        theme = self.ui.themeBox.currentText().strip()
        setStyleSheet(ui, theme)
        os.environ['GRANTHA_THEME'] = theme

    def moreView(self):
        # if self.ui.moreButtFrame.isHidden() == True:
        #     self.ui.moreButtFrame.setHidden(False)
        # else:
        #     self.ui.moreButtFrame.setHidden(True)
        pass

    def showHideColumnsInit(self,butt):
        if butt.isChecked() == True:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headertext = self.ui.tableWidget.horizontalHeaderItem(x).text()
                # debug.info(headertext)
                if headertext == buttText:
                    self.ui.tableWidget.setColumnHidden(x, False)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()
        else:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headertext = self.ui.tableWidget.horizontalHeaderItem(x).text()
                # debug.info(headertext)
                if headertext == buttText:
                    self.ui.tableWidget.setColumnHidden(x, True)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()

    def showHideColumns(self,butt):
        if butt.isChecked() == False:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headertext = self.ui.tableWidget.horizontalHeaderItem(x).text()
                # debug.info(headertext)
                if headertext == buttText:
                    self.ui.tableWidget.setColumnHidden(x, False)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()
        else:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headertext = self.ui.tableWidget.horizontalHeaderItem(x).text()
                # debug.info(headertext)
                if headertext == buttText:
                    self.ui.tableWidget.setColumnHidden(x, True)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()
        self.search()
        # header = self.ui.tableWidget.horizontalHeader()
        # self.ui.tableWidget.setMaximumWidth(header.length())


    def reloadVars(self):
        global authUsers
        global LOCS
        global locs
        global pLocs
        global theColumn
        global slList
        global itList
        # global locList
        global usrList
        global sn
        global blues
        # List Authorized users to access modify functions
        getAuthUsers = "SELECT * FROM AUTH_USERS"
        aU = self.db.execute(getAuthUsers, dictionary=True)
        authUsers = [x['auth_users'] for x in aU]

        # getLOC = "SELECT location FROM LOCATION"
        # loc = self.db.execute(getLOC, dictionary=True)
        # LOC = [x['location'] for x in loc]

        queryCol = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"
        column = self.db.execute(queryCol, dictionary=True)
        theColumn = [x['COLUMN_NAME'] for x in column]

        completer = "SELECT serial_no,item_type,location,user FROM ITEMS"
        theList = self.db.execute(completer, dictionary=True)
        slList = [x['serial_no'] for x in theList]
        itList = list(set([x['item_type'] for x in theList]))
        usrList = list(set([x['user'] for x in theList]))

        # getLocs = "SELECT location FROM LOCATION"
        # locs = self.db.execute(getLocs, dictionary=True)
        # locList = list(set([x['location'] for x in locs]))

        getSN = "SELECT * FROM SERIAL_NO"
        sn = self.db.execute(getSN, dictionary=True)
        # slNoList = [x['serial_no'] for x in sn]
        # getParentLocs = "SELECT parent_location FROM LOCATION "
        # pL = self.db.execute(getParentLocs, dictionary=True)
        # pLocs = list(set([x['parent_location'] for x in pL]))
        # debug.info(pLL)

        getLOC = "SELECT * FROM LOCATION"
        LOCS = self.db.execute(getLOC, dictionary=True)
        locs = [x['location'] for x in LOCS]
        pLocs = [x['parent_location'] for x in LOCS]

        for pl in pLocs:
            if pl != None:
                bloc = next(x['location'] for x in LOCS if x['parent_location'] == pl)
                # for x in LOCS:
                #     if x['parent_location'] == pl:
                #         bloc = x['location']
                blues.append(bloc)
        # debug.info(blues)
        blues = list(set(blues))
        blues.sort()
        # debug.info(blues)

    def loadMap(self):
        global LOCS
        global locs
        global pLocs

        doc = xml.dom.minidom.parse(mapPath)
        name = doc.getElementsByTagName('tspan')
        ids = []
        for t in name:
            id = str(t.attributes['id'].value)
            ids.append(id)

        # getLOC = "SELECT * FROM LOCATION"
        # LOC = self.db.execute(getLOC, dictionary=True)
        # pLoc = [x['parent_location'] for x in LOC]
        # loc = [x['location'] for x in LOC]

        for lc in locs:
            if lc in ids:
                for x in LOCS:
                    if x['location'] == lc:
                        nloc = x['parent_location']
                        for t in name:
                            if (t.attributes['id'].value == lc):
                                t.childNodes[0].nodeValue = nloc

        for pl in pLocs:
            if pl in ids:
                for x in LOCS:
                    if x['parent_location'] == pl:
                        bloc = x['location']
                        for t in name:
                            if (t.attributes['id'].value == pl):
                                t.childNodes[0].nodeValue = bloc

        f = open(mapPath, "w")
        f.write(doc.toxml())
        f.close()


    # def setMap(self):
    #     self.loadMap()
    #     layout = QtWidgets.QVBoxLayout()
    #     self.ui.frame.setLayout(layout)
    #     for i in reversed(range(layout.count())):
    #         layout.itemAt(i).widget().setParent(None)
    #     imageThumbMap = ImageWidget(mapPath, 32)
    #     # imageThumbMap.clicked.connect(lambda x, imagePath = mapPath: imageWidgetClicked(imagePath))
    #     imageThumbMap.clicked.connect(self.showMap)
    #     layout.addWidget(imageThumbMap)

    def viewMap(self):
        self.reloadVars()
        self.loadMap()
        imageWidgetClicked(mapPath)


    def ItemPopUp(self,pos):

        selectedCellIndex = self.ui.tableWidget.selectedIndexes()
        for index in selectedCellIndex:
            selectedColumnIndex = index.column()

            selectedColumnLabel = self.ui.tableWidget.horizontalHeaderItem(selectedColumnIndex).text()
            # debug.info (selectedColumnLabel)

            if (selectedColumnLabel == "location"):
                menu = QtWidgets.QMenu()
                theme = os.environ['GRANTHA_THEME']
                setStyleSheet(menu, theme)

                try:
                    selected = self.ui.tableWidget.selectedItems()
                except:
                    selected = None

                if(selected):
                    selectedText = ""
                    try:
                        selectedText = str(self.ui.tableWidget.currentItem().text().strip())
                    except:
                        pass
                    if selectedText:
                        # debug.info(selectedText)
                        if selectedText in blues:
                            self.messages('white','')
                            viewParentAction = menu.addAction("View Parent Location")
                            if user in authUsers:
                                modifyLocationAction = menu.addAction("Modify Location")

                            action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

                            # if(selected):
                            #     selectedText = str(self.ui.tableWidget.currentItem().text().strip())
                            try:
                                if (action == viewParentAction):
                                    self.viewParent()
                            except:
                                pass
                            try:
                                if (action == modifyLocationAction):
                                    self.modify(selectedText)
                            except:
                                pass
                        else:
                            self.messages('white','')

            elif (selectedColumnLabel == "serial_no"):
                menu = QtWidgets.QMenu()
                theme = os.environ['GRANTHA_THEME']
                setStyleSheet(menu, theme)

                try:
                    selected = self.ui.tableWidget.selectedItems()
                except:
                    selected = None

                if (selected):
                    selectedText = ""
                    try:
                        selectedText = str(self.ui.tableWidget.currentItem().text().strip())
                    except:
                        pass
                    if selectedText:
                        # debug.info(selectedText)
                        if selectedText in slList:
                            self.messages('white', '')
                            if user in authUsers:
                                manageItemAction = menu.addAction("Manage Item")

                            action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

                            try:
                                if (action == manageItemAction):
                                    self.manageItems(selectedText)
                            except:
                                pass
                        else:
                            self.messages('white', '')
            else:
                pass


    def viewParent(self):
        selectedText = self.ui.tableWidget.currentItem().text()
        # debug.info selectedText

        if selectedText in locs:
            getParentLocation = "SELECT parent_location FROM LOCATION WHERE location='%s' " %(selectedText)
            # pL = self.db.getParentLocation(query)
            pL = self.db.execute(getParentLocation,dictionary=True)
            debug.info(pL)
            pL = pL[0]
            self.parentLocation = pL['parent_location']
            # debug.info self.parentLocation
            if self.parentLocation == None:
                parentMessage = "No Parent Location"
            else:
                parentMessage = self.parentLocation
            # messageBox(parentMessage,path=os.path.join(imageDir, "info-icon-1.png"))
            theme = os.environ['GRANTHA_THEME']
            if theme == "dark":
                self.messages('yellow',parentMessage)
            else:
                self.messages('blue',parentMessage)
            # self.viewParentMessage()
        else:
            debug.info ("not valid location")


    def center(self):
        qr = self.ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())


    def allBtnClick(self):
        global theColumn
        self.messages('white','Loading')
        self.ui.tableWidget.setSortingEnabled(False)
        # self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.setRowCount(0)

        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()

        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        # for x in range(0, len(theColumn)):
        #     headertext = self.ui.tableWidget.horizontalHeaderItem(x).text()
        #     debug.info(headertext)
        #     if headertext in hiddenColumns:
        #         self.ui.tableWidget.setColumnHidden(x, True)

        queryAll = "SELECT * FROM ITEMS ORDER BY item_type"
        theRows = self.db.execute(queryAll,dictionary=True)
        # debug.info(len(theRows))
        self.ui.tableWidget.setRowCount(len(theRows))

        row = 0
        while True:
            if (row == len(theRows)):
                break
            primaryResult = theRows[row]
            col = 0
            for n in theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        # numRows = self.ui.tableWidget.rowCount()
        # paths = {}
        # for row in range(numRows):
        #     path = str(self.ui.tableWidget.item(row, 10).text())
        #     paths[row]=path
        #
        # if paths:
        #     for x in paths.keys():
        #         if paths[x]:
        #             # debug.info(paths[x])
        #             self.ui.tableWidget.takeItem(x, 10)
        #             slNo = self.ui.tableWidget.item(x, 0).text()
        #             # imageThumb = ImageWidget(paths[x], 32)
        #             imageThumb = ImageWidget(os.path.join(imageDir, "image.png"), 32)
        #             # imageThumb.clicked.connect(lambda x, imagePath=paths[x]: imageWidgetClicked(imagePath))
        #             imageThumb.clicked.connect(lambda x, slNo=slNo, rowId=x: self.loadImageThumbs(slNo,rowId))
        #             self.ui.tableWidget.setCellWidget(x, 10, imageThumb)
        #         else:
        #             pass

        numRows = self.ui.tableWidget.rowCount()
        debug.info(numRows)
        if numRows:
            for row in range(numRows):
                imgCell = self.ui.tableWidget.item(row, 10)
                if imgCell:
                    self.ui.tableWidget.takeItem(row, 10)
                    path = str(imgCell.text())
                    if path:
                        # slNo = self.ui.tableWidget.item(row, 0).text()
                        # imageThumb = ImageWidget(path, 32)
                        imageButton = QtWidgets.QPushButton()
                        imageButton.setText("Image")

                        # imageThumb = ImageWidget(os.path.join(imageDir, "image.png"), 32)
                        # # imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                        # imageThumb.clicked.connect(lambda x,path=path, rowId=row: self.loadImageThumbs(path, rowId))
                        # index = QtCore.QPersistentModelIndex(self.ui.tableWidget.model().index(row, 10))
                        imageButton.clicked.connect(lambda x,path=path, button=imageButton: self.loadImageThumbs(path, button))
                        # self.ui.tableWidget.setCellWidget(row, 10, imageThumb)
                        self.ui.tableWidget.setCellWidget(row, 10, imageButton)


        # self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.resizeColumnsToContents()
        debug.info("Loaded list of all items.")
        self.messages('white','Loaded list of all items')
        # self.ui.messages.setStyleSheet('color: white')
        # self.ui.messages.setText("Loaded list of all items.")
        self.ui.tableWidget.setSortingEnabled(True)

    def loadImageThumbs(self,path, button):
        # debug.info(slNo)
        # debug.info(rowId)
        # buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(button.pos())
        debug.info(index.row())
        self.ui.tableWidget.selectRow(index.row())

        self.ui.listWidget.clear()
        imageNames = {}
        try:
            imageNames = json.loads(str(path).replace("\'", "\""))
        except:
            debug.info(str(sys.exc_info()))
        debug.info(imageNames)
        if imageNames:
            for keys in imageNames:
                imPath = str(imageNames[keys])
                debug.info(imPath)

                imageThumb = ImageWidget(imPath, 64)
                imageThumb.clicked.connect(lambda x, imagePath=imPath: imageWidgetClicked(imagePath))

                label = QtWidgets.QLabel()

                picName = str(imPath.split(os.sep)[-1:][0])
                size = getFileSize(os.path.getsize(imPath))
                # timeModified = str(time.ctime(os.path.getmtime(imageName)))
                timeModified = datetime.datetime.fromtimestamp(os.path.getmtime(imPath)).strftime('%d-%m-%Y %H:%M:%S')

                label.setText("<b>Name: </b>" + picName + "<br />" + "<b>Size: </b>" + size + "<br />" + "<b>Modified: </b>" + timeModified)

                itemWidget = QtWidgets.QWidget()
                hl = QtWidgets.QHBoxLayout()
                itemWidget.setLayout(hl)
                # hl.addWidget(checkbox)
                hl.addWidget(imageThumb)
                hl.addWidget(label)

                item = QListWidgetItemSort()
                item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
                self.ui.listWidget.addItem(item)
                self.ui.listWidget.setItemWidget(item, itemWidget)
            # self.ui.messages.setText("Loaded images")
            self.messages('white','Loaded images')
        else:
            # self.ui.messages.setText("No images")
            self.messages('red','No images')

        # slNoDir = imagePicsDir + slNo
        # # formats = ("jpg", "png")
        # images = []
        # for format in imageFormats:
        #     images.extend(glob.glob(slNoDir.rstrip(os.sep) + os.sep + "*.%s" % format))
        # images.sort()
        # debug.info(images)
        # if images:
        #     for i in images:
        #         imageName = str(i)
        #
        #         imageThumb = ImageWidget(i, 64)
        #         imageThumb.clicked.connect(lambda x, imagePath=imageName: imageWidgetClicked(imagePath))
        #
        #         label = QtWidgets.QLabel()
        #
        #         picName = imageName.split(os.sep)[-1:][0]
        #         size = getFileSize(os.path.getsize(imageName))
        #         # timeModified = str(time.ctime(os.path.getmtime(imageName)))
        #         timeModified = datetime.datetime.fromtimestamp(os.path.getmtime(imageName)).strftime('%d-%m-%Y %H:%M:%S')
        #
        #         label.setText("Name: "+picName+"\n"+"Size: "+size+"\n"+"Modified: "+timeModified)
        #
        #         itemWidget = QtWidgets.QWidget()
        #         hl = QtWidgets.QHBoxLayout()
        #         itemWidget.setLayout(hl)
        #         # hl.addWidget(checkbox)
        #         hl.addWidget(imageThumb)
        #         hl.addWidget(label)
        #
        #         item = QListWidgetItemSort()
        #         item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
        #         self.ui.listWidget.addItem(item)
        #         self.ui.listWidget.setItemWidget(item,itemWidget)

    def search(self):
        global theColumn
        self.ui.tableWidget.setSortingEnabled(False)
        self.ui.tableWidget.setRowCount(0)

        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        currTxt = self.ui.comboBox.currentText().strip()
        # debug.info currTxt

        if self.ui.allButton.isChecked():
            self.allBtnClick()

        if self.ui.serialNoButton.isChecked():
            if (currTxt in slList):
                getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                # debug.info rows
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass

        if self.ui.itemTypeButton.isChecked():
            if (currTxt in itList):
                getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE item_type='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass

        if self.ui.locationButton.isChecked():
            if (currTxt in locs):
                getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE location='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                # debug.info(rows)
                if rows != 0:
                    self.ui.tableWidget.setRowCount(len(rows))
                    self.fillTable(rows)

                if currTxt in pLocs:
                    getLocation = "SELECT location FROM LOCATION WHERE parent_location='%s' " % (currTxt)
                    bL = self.db.execute(getLocation, dictionary=True)
                    # debug.info(bPL)
                    self.butts = {}
                    self.buttsLoc = {}
                    try:
                        rowCount = len(rows)
                    except:
                        rowCount = 0
                    n = 0
                    for loc in bL:
                        self.ui.tableWidget.insertRow(rowCount+n)
                        bl = str(loc["location"])

                        self.butts["blueButt"+str(n)] = QtWidgets.QPushButton()
                        self.butts["blueButt"+str(n)].setText(bl)

                        # debug.info(bpL)
                        # blueBtn = QtWidgets.QPushButton()
                        # blueBtn.setText(bl)
                        # BL = str(blueBtn.text()).strip()
                        # blueBtn.clicked.connect(lambda x, rows=rows: self.extraTable(BL))
                        # butts["blueButt" + str(n)].clicked.connect(lambda x, rows=rows: self.extraTable(bl))
                        # self.blueBtnNoPressed = 0
                        colIndex = 0
                        for x in range(0, len(theColumn)):
                            if self.ui.tableWidget.isColumnHidden(colIndex) == True:
                                colIndex+=1
                        self.ui.tableWidget.setCellWidget(rowCount+n, colIndex, self.butts["blueButt"+str(n)])
                        self.buttsLoc["blueButt"+str(n)] = rowCount+n
                        n+=1
                    debug.info(self.butts)
                    debug.info(self.buttsLoc)

                    self.buttsPress = {}
                    for butt in self.butts.keys():
                        debug.info(self.butts[butt].text())
                        # bl = self.butts[butt].text()
                        self.butts[butt].clicked.connect(lambda x, BL=butt: self.extraTable(BL))
                        self.buttsPress[butt] = 0
                        # self.blueBtnNoPressed = 0
                    debug.info(self.buttsPress)
            else:
                pass

        if self.ui.userButton.isChecked():
            if (currTxt in usrList):
                getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE user='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass


    def extraTable(self,BL):
        debug.info(BL)
        bl = self.butts[BL].text()
        getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE location='%s' " % (bl)
        rows = self.db.execute(getRows, dictionary=True)

        rowLoc = self.buttsLoc[BL]
        debug.info(rowLoc)

        buttNo = int(BL[8:])
        debug.info(buttNo)
        totalButts = len(self.butts)
        debug.info(totalButts)

        if rows!=0:
            # self.blueBtnNoPressed +=1
            # debug.info(self.blueBtnNoPressed)
            debug.info(rowLoc)
            debug.info(self.buttsPress[BL])
            self.buttsPress[BL] +=1
            if (self.buttsPress[BL]%2) == 0:
                for n in range(0,len(rows)):
                    # rowLoc = self.buttsLoc[BL]
                    # rowCount = self.ui.tableWidget.rowCount()
                    # self.ui.tableWidget.removeRow(rowCount-1)
                    self.ui.tableWidget.removeRow(rowLoc+1)

                for n in range(buttNo+1,totalButts):
                    currLoc = self.buttsLoc["blueButt"+str(n)]
                    self.buttsLoc["blueButt"+str(n)] = currLoc-len(rows)

            else:
                # rowLoc = self.buttsLoc[BL]
                debug.info(rowLoc)

                row = 0

                while True:
                    if (row == len(rows)):
                        break
                    primaryResult = rows[row]
                    # debug.info(primaryResult)

                    # rowCount = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(rowLoc+row+1)

                    col = 0
                    for n in theColumn:
                        result = primaryResult[n]
                        self.ui.tableWidget.setItem(rowLoc+row+1, col, QtWidgets.QTableWidgetItem(str(result)))
                        imgCell = self.ui.tableWidget.item(rowLoc+row+1, 10)
                        path = ""
                        try:
                            path = str(imgCell.text())
                        except:
                            pass
                        if path:
                            # slNo = self.ui.tableWidget.item(rowLoc+row+1, 0).text()
                            self.ui.tableWidget.takeItem(rowLoc+row+1, 10)
                            # imageThumb = ImageWidget(path, 32)
                            # imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                            # imageThumb = ImageWidget(os.path.join(imageDir, "image.png"), 32)
                            # # imageThumb.clicked.connect(lambda x, slNo=slNo, rowId=rowLoc+row+1: self.loadImageThumbs(slNo, rowId))
                            # imageThumb.clicked.connect(lambda x, path=path, rowId=rowLoc+row+1: self.loadImageThumbs(path, rowId))
                            # self.ui.tableWidget.setCellWidget(rowLoc+row+1, 10, imageThumb)

                            imageButton = QtWidgets.QPushButton()
                            imageButton.setText("Image")
                            imageButton.clicked.connect(lambda x, path=path, button=imageButton: self.loadImageThumbs(path, button))
                            self.ui.tableWidget.setCellWidget(rowLoc+row+1, 10, imageButton)

                        col += 1
                    row += 1

                # numRows = self.ui.tableWidget.rowCount()
                # for row in range(numRows):
                #     imgCell = self.ui.tableWidget.item(row, 10)
                #     if imgCell:
                #         path = str(imgCell.text())
                #         # debug.info(path)
                #         self.ui.tableWidget.takeItem(row, 10)
                #         imageThumb = ImageWidget(path, 32)
                #         imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                #         self.ui.tableWidget.setCellWidget(row, 10, imageThumb)

                for n in range(buttNo+1,totalButts):
                    currLoc = self.buttsLoc["blueButt"+str(n)]
                    self.buttsLoc["blueButt"+str(n)] = currLoc+len(rows)



        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def fillTable(self,rows):
        row = 0
        while True:
            if (row == len(rows)):
                break
            primaryResult = rows[row]
            col = 0
            for n in theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                col += 1
            row += 1

        # self.ui.tableWidget.resizeColumnsToContents()

        numRows = self.ui.tableWidget.rowCount()
        debug.info(numRows)
        if numRows:
            for row in range(numRows):
                imgCell = self.ui.tableWidget.item(row, 10)
                if imgCell:
                    self.ui.tableWidget.takeItem(row, 10)
                    path = str(imgCell.text())
                    if path:
                        # slNo = self.ui.tableWidget.item(row,0).text()
                        # imageThumb = ImageWidget(path, 32)
                        # imageThumb = ImageWidget(os.path.join(imageDir, "image.png"), 32)
                        # # imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                        # # imageThumb.clicked.connect(lambda x, slNo=slNo, rowId=row: self.loadImageThumbs(slNo,rowId))
                        # imageThumb.clicked.connect(lambda x, path=path, rowId=row: self.loadImageThumbs(path, rowId))
                        # self.ui.tableWidget.setCellWidget(row, 10, imageThumb)

                        imageButton = QtWidgets.QPushButton()
                        imageButton.setText("Image")
                        imageButton.clicked.connect(lambda x, path=path, button=imageButton: self.loadImageThumbs(path, button))
                        self.ui.tableWidget.setCellWidget(row, 10, imageButton)

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def slNoBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        # completer = "SELECT serial_no,item_type,location,user FROM ITEMS"
        # # theList = self.db.Completer()
        # theList = self.db.execute(completer,dictionary=True)
        # slList = [x['serial_no'] for x in theList]
        slList.sort()
        self.ui.comboBox.addItems(slList)
        self.search()
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(slList)
        # self.completer()

    def itBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        itList.sort()
        self.ui.comboBox.addItems(itList)
        self.search()


    def locBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        locs.sort()
        self.ui.comboBox.addItems(locs)
        self.search()


    def usrBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        usrList.sort()
        self.ui.comboBox.addItems(usrList)
        self.search()


    def reloadBtnClick(self):
        self.reloadVars()

    # Processes to start when respective buttons are clicked
    def manageItems(self,serialno=""):
        debug.info(serialno)
        debug.info("Opening manage items Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        # p.setStandardOutputFile(tempDir + os.sep + "Grantha_ManageItems_" + user + ".log")
        # p.setStandardErrorFile(tempDir + os.sep + "Grantha_ManageItems_" + user + ".err")
        p.finished.connect(self.enableButtons)
        if serialno:
            p.start(sys.executable + " " + Manage_Items + " --serialno " + serialno)
        else:
            p.start(sys.executable + " " + Manage_Items)

    def rfidTools(self):
        debug.info("Opening Rfid Tools Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        p.start(sys.executable, Rfid_Tools.split())



    # def update(self):
    #     p = QProcess(parent=self.ui)
    #     p.start(sys.executable, Update.split())
    #
    # def updateTag(self):
    #     p = QProcess(parent=self.ui)
    #     p.start(sys.executable, Update_Tag.split())

    def modify(self,loc=""):
        debug.info(loc)
        debug.info("Opening Modify Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        if loc:
            p.start(sys.executable + " " + Modify + " --name " + loc)
        else:
            p.start(sys.executable + " " + Modify)

    def repair(self):
        debug.info("Opening Repair Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        p.start(sys.executable, Repair.split())

    def log(self):
        debug.info("Opening Logs")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        p.start(sys.executable, Log.split())

    def findTag(self,process):
        pass
        # p = QProcess(parent=self.ui)
        # p.start(sys.executable, Find_Tag.split())

    def read_out(self):
        if processes:
            for process in processes:
                print ('stdout:', str(process.readAllStandardOutput()).strip())

    def read_err(self):
        if processes:
            for process in processes:
                print ('stderr:', str(process.readAllStandardError()).strip())


    def disableButtons(self):
        self.ui.readSingleButton.setEnabled(False)
        self.ui.readMultiButton.setEnabled(False)
        self.ui.manageItemsButton.setEnabled(False)
        self.ui.rfidToolsButton.setEnabled(False)
        self.ui.modifyButton.setEnabled(False)
        self.ui.repairButton.setEnabled(False)
        self.ui.logButton.setEnabled(False)
        self.ui.findTagButton.setEnabled(False)


    def enableButtons(self):
        self.ui.readSingleButton.setEnabled(True)
        self.ui.readMultiButton.setEnabled(True)
        self.ui.manageItemsButton.setEnabled(True)
        self.ui.rfidToolsButton.setEnabled(True)
        self.ui.modifyButton.setEnabled(True)
        self.ui.repairButton.setEnabled(True)
        self.ui.logButton.setEnabled(True)
        self.ui.findTagButton.setEnabled(True)
        del processes[:]
        debug.info(processes)



    def readFromRfidTag(self):
        self.ui.readSingleButton.setEnabled(False)
        self.ui.readMultiButton.setEnabled(False)
        self.ui.tableWidget.setRowCount(0)
        rT = readThread(app)
        # self.msg = messageBox("Place Your Tag")
        rT.waiting.connect(self.msg)
        # widgets.append(self.msg)
        rT.tagIdReceived.connect(self.closePlaceTagMessage)
        rT.start()

    def msg(self, plceMsg):
        messagebox = TimerMessageBox(1, plceMsg)
        messagebox.exec_()


    def closePlaceTagMessage(self, tagId):
        try:
            debug.info("Message Closed")
        except:
            debug.info (str(sys.exc_info()))
            pass

        TI = [x['tag_id'] for x in sn]
        # debug.info  (TI)
        if tagId in TI:
            # slno = self.db.getSlFrmTid(tagId)
            getSlFrmTid = "SELECT serial_no FROM SERIAL_NO WHERE tag_id=\"{}\" ".format(tagId)
            slno = self.db.execute(getSlFrmTid, dictionary=True)
            slno = slno[0]
            slNo = slno['serial_no']
            # debug.info slno
            debug.info ("received sl.no: "+slNo)
            self.ui.comboBox.setEditText(slNo)

            self.ui.tableWidget.setColumnCount(len(theColumn))
            self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

            currTxt = self.ui.comboBox.currentText().strip()

            getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE serial_no='%s' " % (currTxt)
            rows = self.db.execute(getRows, dictionary=True)

            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable(rows)
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)

        else:
            # messageBox("<b>This Serial No. does not exists in Database</b> \n And/Or \n <b>Tag was not scanned properly!</b>","",os.path.join(imageDir,"oh.png"))
            # self.ui.messages.setText("<b>This Serial No. does not exists in Database</b> \n And/Or \n <b>Tag was not scanned properly!</b>")
            self.messages('red','<b>This Serial No. does not exists in Database</b> \n And/Or \n <b>Tag was not scanned properly!</b>')
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)
            # self.wrongTagMessage()


    def readMultiFromRfidTag(self):
        self.ui.tableWidget.setRowCount(0)
        # timeout = str(self.ui.spinBox.value())

        # if self.ui.readMultipleButton.isChecked():
        self.ui.readMultiButton.setEnabled(False)
        self.ui.readSingleButton.setEnabled(False)
        self.ui.stopReadButton.setEnabled(True)

        self.rfidMultiUniqSlno.clear()
        self.rfidMultiCount = 0

        # rmrT = readMultiReplyThread(app)
        rmT = readMultiThread(app)

        # rmrT.slNoReceived.connect(self.updateTable)
        # rmrT.finished.connect(self.readButtonEnable)
        rmT.tagIdReceived.connect(self.updateTable)

        # rmrT.start()
        rmT.start()

        # else:
        #     pass

    def updateTable(self, tagId):
        if (tagId == "MULTI_READ_STARTED"):
            pass

        else:

            TI = [x['tag_id'] for x in sn]
            if tagId in TI:
                # slno = self.db.getSlFrmTid(tagId)
                getSlFrmTid = "SELECT serial_no FROM SERIAL_NO WHERE tag_id=\"{}\" ".format(tagId)
                slno = self.db.execute(getSlFrmTid, dictionary=True)
                slno = slno[0]
                slNo = slno['serial_no']
                debug.info ("received sl.no: "+slNo)

                if (self.rfidMultiUniqSlno.has_key(slNo)):
                    return

                self.rfidMultiUniqSlno[slNo] = 1
                debug.info (self.rfidMultiUniqSlno)

                self.rfidMultiCount += 1
                self.ui.comboBox.setEditText(slNo)

                # column = self.db.getColumns()
                # theColumn = [x['COLUMN_NAME'] for x in column]

                self.ui.tableWidget.setColumnCount(len(theColumn))
                self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

                self.ui.tableWidget.setRowCount(self.rfidMultiCount)

                currTxt = self.ui.comboBox.currentText()
                getRows = "SELECT " + ','.join(theColumn) + " FROM ITEMS WHERE serial_no='%s' " % (currTxt)
                rows = self.db.execute(getRows, dictionary=True)
                # debug.info(rows)
                # rows = self.db.getRows(self.query)
                # self.ui.tableWidget.setRowCount(len(rows))

                if rows:
                    rowCount = self.ui.tableWidget.rowCount()


                    row = rowCount -1
                    while True:
                        try:
                            primaryResult = rows[0]
                        except:
                            break
                        # debug.info(primaryResult)
                        col = 0
                        for n in theColumn:
                            result = primaryResult[n]
                            self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                            col += 1
                        row += 1
                        break

                    numRow = self.rfidMultiCount -1
                    imgCell = self.ui.tableWidget.item(numRow, 10)
                    if imgCell:
                        path = str(imgCell.text())
                        if path:
                            # debug.info(path)
                            self.ui.tableWidget.takeItem(numRow, 10)
                            # imageThumb = ImageWidget(path, 32)
                            # imageThumb = ImageWidget(os.path.join(imageDir, "image.png"), 32)
                            # imageThumb.clicked.connect(lambda x, path=path, rowId=row: self.loadImageThumbs(path, rowId))
                            # # imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                            # self.ui.tableWidget.setCellWidget(numRow, 10, imageThumb)
                            imageButton = QtWidgets.QPushButton()
                            imageButton.setText("Image")
                            imageButton.clicked.connect(
                                lambda x, path=path, button=imageButton: self.loadImageThumbs(path, button))
                            self.ui.tableWidget.setCellWidget(numRow, 10, imageButton)

                    self.ui.tableWidget.resizeRowsToContents()
                    self.ui.tableWidget.resizeColumnsToContents()
                else:
                    pass
            else:
                pass


    def stopRead(self):
        # self.ui.readMultiButton.setEnabled(True)
        # self.ui.readSingleButton.setEnabled(True)
        self.ui.stopReadButton.setEnabled(False)

        srT = stopReadThread(app)
        srT.ackReceived.connect(self.readButtonsEnable)
        srT.start()

    def readButtonsEnable(self, ack):
        if (ack == "STOPPING"):
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)

    def messages(self, color, msg):
        self.ui.messages.setStyleSheet("color: %s" % color)
        self.ui.messages.setText("%s" % msg)

    def relaunch(self):
        try:
            p = psutil.Process(os.getpid())
            for handler in p.open_files() + p.connections():
                os.close(handler.fd)
        except:
            debug.info(str(sys.exc_info()))

        python = sys.executable
        os.execl(python, python, *sys.argv)



# class ImageWidget(QtWidgets.QPushButton):
#     def __init__(self, imagePath, imageSize, parent=None):
#         super(ImageWidget, self).__init__(parent)
#         self.imagePath = imagePath
#         self.picture = QtGui.QPixmap(imagePath)
#         # debug.info (self.imagePath)
#         self.picture  = self.picture.scaledToHeight(imageSize,0)
#
#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         painter.setPen(QtCore.Qt.NoPen)
#         painter.drawPixmap(0, 0, self.picture)
#
#     def sizeHint(self):
#         return(self.picture.size())





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
            debug.info (str(sys.exc_info()))
        self.socket.send("READ")

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        try:
            tagId = self.socket.recv()
            debug.info( "Received Tag Id :" + tagId)
            self.tagIdReceived.emit(tagId)
        except:
            debug.info (str(sys.exc_info()))

        self.socket.close()
        
        if (self.socket.closed == True):
            debug.info( "read Single Socket closed.")


class readMultiThread(QThread):
    # waiting = pyqtSignal()
    tagIdReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(readMultiThread, self).__init__(parent)
        # self.to = to

    def run(self):
        # self.waiting.emit()

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")
        debug.info("connected.")
        self.socket.send_multipart(["READ_MULTI",ip])
        rep = self.socket.recv_multipart()
        debug.info (rep)
        # self.socket.close()
        #
        # if (context.closed == True) and (self.socket.closed == True):
        #     debug.info "Socket and Context closed."
        #####################################
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (ip, 4695)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()
        #####################################
        while(True):
            tagId = connection.recv(1024)
            debug.info (tagId)
            # debug.info type(rep)
            if(tagId == "MULTI_STOP"):
                connection.close()
                # sock.shutdown(1)
                sock.close()
                break
            else:
                self.tagIdReceived.emit(tagId)
        # sock.close()
        self.socket.close()
        
        if (self.socket.closed == True):
            debug.info( "read Multi Socket closed.")

class stopReadThread(QThread):
    # waiting = pyqtSignal()
    ackReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(stopReadThread, self).__init__(parent)

    def run(self):
        # self.waiting.emit()

        
        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")
        debug.info("connected.")

        self.socket.send("STOP")

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        ack = self.socket.recv()
        debug.info (ack)
        self.ackReceived.emit(ack)
        self.socket.close()
        
        if (self.socket.closed == True):
            debug.info( "stop Read Socket closed.")

class QListWidgetItemSort(QtWidgets.QListWidgetItem):

  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)

if __name__ == '__main__':
    setproctitle.setproctitle("GRANTHA")

    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

