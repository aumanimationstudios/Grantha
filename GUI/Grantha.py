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
import re

# Filepaths and directories
filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")
fileDir = os.path.join(projDir, "GUI")
mapPath = os.path.join(imageDir, "map.svg")
imagePicsDir = "/blueprod/STOR2/stor2/grantha/share/pics/"

sys.path.append(uiDir)
sys.path.append(imageDir)
sys.path.append(fileDir)

# Path of side panel button scripts
Manage_Items = os.path.join(fileDir, "Manage_Items.py")
Rfid_Tools = os.path.join(fileDir, "Rfid_Tools.py")
Modify = os.path.join(fileDir, "Modify_Location.py")
Repair = os.path.join(fileDir, "Repair.py")
Log = os.path.join(fileDir, "Log.py")
# Find_Tag = os.path.join(fileDir, "Find_Tag.py")

# Constants an Variables
user = os.environ['USER']
context = zmq.Context()
processes = []

authUsers = None
LOCS = None
locs = None
pLocs = None
theColumn = None

slList = None
itList = None
locList = None
usrList = None
descList = None
makeList = None
modelList = None

sn = None
blues = []

repairItmlist = None

os.environ['QT_LOGGING_RULES'] = "qt5ct.debug=false"

hiddenColumns = ["serial_no","model","price","purchased_on","warranty_valid_till","user"]
# hiddenColumns = ["serial_no","item_type","description","make","model","price","purchased_on","warranty_valid_till","location","user","image"]

class mainWindow():
    global processes

    # Database query execution function
    db = dbGrantha.dbGrantha()

    def __init__(self):

        global theColumn

        self.rfidMultiCount = 0
        self.rfidMultiUniqSlno = {}

        # Load ui file and set icon and title
        # self.ui = uic.loadUi(os.path.join(uiDir,"Grantha.ui"))
        self.ui = uic.loadUi(os.path.join(projDir,"Test","Grantha_test.ui"))
        self.ui.setWindowTitle('GRANTHA')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))

        self.reloadVars()
        self.allBtnClick()
        self.loadNotifications()

        # Set filter checkboxes and their states
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
            butt.clicked.connect(lambda x, butt=butt: self.showHideColumns(butt))
            self.showHideColumns(butt)

        # Functions of ui button click
        self.ui.mapButton.clicked.connect(self.viewMap)
        self.ui.allButton.clicked.connect(self.allBtnClick)
        self.ui.serialNoButton.clicked.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.clicked.connect(self.itBtnClick)
        self.ui.locationButton.clicked.connect(self.locBtnClick)
        self.ui.userButton.clicked.connect(self.usrBtnClick)
        self.ui.reloadButton.clicked.connect(self.reloadBtnClick)
        self.ui.relaunchButton.clicked.connect(self.relaunch)

        self.ui.comboBox.currentIndexChanged.connect(self.search)

        self.ui.tableWidget.customContextMenuRequested.connect(self.ItemPopUp)

        if user in authUsers:
            self.ui.manageItemsButton.clicked.connect(self.manageItems)
            self.ui.rfidToolsButton.clicked.connect(self.rfidTools)
            self.ui.modifyButton.clicked.connect(self.modify)
            self.ui.repairButton.clicked.connect(self.repair)
            self.ui.logButton.clicked.connect(self.log)
            self.ui.findTagButton.clicked.connect(self.findTag)
            self.ui.readSingleButton.clicked.connect(self.readFromRfidTag)
            self.ui.readMultiButton.clicked.connect(self.readMultiFromRfidTag)
            self.ui.stopReadButton.setEnabled(False)
            self.ui.stopReadButton.clicked.connect(self.stopRead)




        self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.tableSplitter.setSizes([800, 50])
        self.ui.notificationSplitter.setSizes([800, 50])

        self.center()
        self.ui.showMaximized()

        # Set Stylesheet
        Themes = ["dark", "light", "default"]
        self.ui.themeBox.addItems(Themes)
        self.changeStyleSheet()
        self.ui.themeBox.currentIndexChanged.connect(self.changeStyleSheet)

    def changeStyleSheet(self):
        '''
        Sets Stylesheet to the ui
        :return: theme
        '''
        ui = self.ui
        theme = self.ui.themeBox.currentText().strip()
        setStyleSheet(ui, theme)
        os.environ['GRANTHA_THEME'] = theme


    def showHideColumns(self,butt):
        '''
        :param button:
        :return true or false states of column corresponding to button:
        '''
        global theColumn
        if butt.isChecked() == True:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headerText = self.ui.tableWidget.horizontalHeaderItem(x).text()
                if headerText == buttText:
                    self.ui.tableWidget.setColumnHidden(x, False)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()
        else:
            buttText = butt.text()
            for x in range(0, len(theColumn)):
                headerText = self.ui.tableWidget.horizontalHeaderItem(x).text()
                if headerText == buttText:
                    self.ui.tableWidget.setColumnHidden(x, True)
            self.ui.tableWidget.resizeRowsToContents()
            self.ui.tableWidget.resizeColumnsToContents()

        if self.ui.locationButton.isChecked():
            self.search()


    def reloadVars(self):
        '''
        Loads values of all variables needed
        :return:
        '''
        global authUsers
        global LOCS
        global locs
        global pLocs
        global theColumn
        global slList
        global itList
        global locList
        global usrList
        global descList
        global makeList
        global modelList
        global sn
        global blues
        global repairItmlist

        self.loadNotifications()

        # List Authorized users to access modify functions
        getAuthUsers = "SELECT * FROM AUTH_USERS"
        aU = self.db.execute(getAuthUsers, dictionary=True)
        authUsers = [x['auth_users'] for x in aU]

        queryCol = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"
        column = self.db.execute(queryCol, dictionary=True)
        theColumn = [x['COLUMN_NAME'] for x in column]

        completer = "SELECT * FROM ITEMS"
        theList = self.db.execute(completer, dictionary=True)
        slList = [x['serial_no'] for x in theList]
        itList = list(set([x['item_type'] for x in theList]))
        locList = list(set([x['location'] for x in theList]))
        usrList = list(set([x['user'] for x in theList]))
        descList = list(set([x['description'] for x in theList]))
        makeList = list(set([x['make'] for x in theList]))
        modelList = list(set([x['model'] for x in theList]))

        getSN = "SELECT * FROM SERIAL_NO"
        sn = self.db.execute(getSN, dictionary=True)

        getLOC = "SELECT * FROM LOCATION"
        LOCS = self.db.execute(getLOC, dictionary=True)
        locs = [x['location'] for x in LOCS]
        pLocs = [x['parent_location'] for x in LOCS]

        for pl in pLocs:
            if pl != None:
                # bloc = next(x['location'] for x in LOCS if x['parent_location'] == pl)
                for x in LOCS:
                    if x['parent_location'] == pl:
                        bloc = x['location']
                        blues.append(bloc)
        # debug.info(blues)
        blues = list(set(blues))
        blues.sort()
        # debug.info(blues)

        getRepairItems = "SELECT * FROM repairs"
        REP_ITEMS = self.db.execute(getRepairItems, dictionary=True)
        if REP_ITEMS == 0:
            pass
        else:
            repairItmlist = [x['item'] for x in REP_ITEMS]

    def loadMap(self):
        '''
        loads the location values to svg
        :return:
        '''
        global LOCS
        global locs
        global pLocs

        doc = xml.dom.minidom.parse(mapPath)
        name = doc.getElementsByTagName('tspan')
        ids = []
        for t in name:
            id = str(t.attributes['id'].value)
            ids.append(id)

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

    def viewMap(self):
        '''
        Loads map image from svg
        :return:
        '''
        self.reloadVars()
        self.loadMap()
        imageWidgetClicked(mapPath)

    def loadNotifications(self):
        '''
        Loads notifications to the ui
        :return:
        '''
        # Get the Column names from repairs table
        columnQuery = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'repairs' AND \
                       COLUMN_NAME NOT IN ('no')"
        column = self.db.execute(columnQuery, dictionary=True)
        theColumn = [x['COLUMN_NAME'] for x in column]

        # Get all entries from the repairs table
        query = "SELECT " + ','.join(theColumn) + " FROM repairs "
        rows = self.db.execute(query, dictionary=True)

        # List for storing all notifications
        notifications = []

        # For each row in the result from repairs table, prepare a notification string
        currDate = time.strftime('%Y-%m-%d')
        debug.info(currDate)

        for x in rows:
            itemType = ""
            item =(x['item'])
            query = "SELECT item_type from ITEMS WHERE serial_no='{0}'".format(item)
            res = self.db.execute(query,dictionary=True)
            if res!=0:
                itemType = (res[0]['item_type'])
            symptom = (x['symptoms'])
            repairer = (x['repairer'])
            dueDate = str((x['expected_completion_date']).strftime("%a %b %d %Y"))
            if itemType:
                item = itemType+"("+item+")"
            notification = item +" with "+ symptom +" at "+ repairer +" is due on "+ dueDate
            debug.info(notification)

            DueDate = str((x['expected_completion_date']).strftime('%Y-%m-%d'))
            debug.info(DueDate)

            label = QtWidgets.QLabel()
            label.setWordWrap(True)
            if currDate >= DueDate:
                label.setStyleSheet("color: %s" % 'red')
            label.setText(notification)

            notifications.append(label)

        # Populate the ui with notifications
        self.ui.listWidgetNotifications.clear()
        # self.ui.listWidgetNotifications.setStyleSheet("color: %s" % 'red')
        for i in notifications:
            # label = QtWidgets.QLabel()
            # label.setWordWrap(True)
            # label.setStyleSheet("color: %s" % 'red')
            # picName = str(imPath.split(os.sep)[-1:][0])
            # size = getFileSize(os.path.getsize(imPath))
            # # timeModified = str(time.ctime(os.path.getmtime(imageName)))
            # timeModified = datetime.datetime.fromtimestamp(os.path.getmtime(imPath)).strftime('%d-%m-%Y %H:%M:%S')

            # label.setText(i)

            itemWidget = QtWidgets.QWidget()
            hl = QtWidgets.QHBoxLayout()
            itemWidget.setLayout(hl)
            # hl.addWidget(checkbox)
            # hl.addWidget(imageThumb)
            hl.addWidget(i)

            item = QListWidgetItemSort()
            item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
            # self.ui.listWidget.addItem(item)
            self.ui.listWidgetNotifications.addItem(item)
            self.ui.listWidgetNotifications.setItemWidget(item, itemWidget)
            # item = QtWidgets.QListWidgetItem(i)


    def repairPopUp(self,butt,buttText,pos):
        debug.info("repair pop up")
        debug.info(buttText)
        menu = QtWidgets.QMenu()
        theme = os.environ['GRANTHA_THEME']
        setStyleSheet(menu, theme)

        modifyRepairAction = menu.addAction("Modify Repair")

        action = menu.exec_(butt.mapToGlobal(pos))

        try:
            if (action == modifyRepairAction):
                self.repair(buttText, "2")
        except:
            debug.info(str(sys.exc_info()))

    def ItemPopUp(self,pos):
        # debug.info("pop up!")
        '''
        The context menu for items on table.
        :param pos:
        :return:
        '''

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
                                if selectedText in repairItmlist:
                                    modifyRepairAction = menu.addAction("Modify Repair")
                                else:
                                    repairAction = menu.addAction("Repair")

                            action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

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
                            try:
                                if (action == repairAction):
                                    self.repair(selectedText,"0")
                            except:
                                pass
                            try:
                                if (action == modifyRepairAction):
                                    # debug.info("Modify Repair!!!")
                                    self.repair(selectedText,"2")
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
                            self.messages('white','')
                            if user in authUsers:
                                manageItemAction = menu.addAction("Manage Item")
                                if selectedText in repairItmlist:
                                    modifyRepairAction = menu.addAction("Modify Repair")
                                else:
                                    repairAction = menu.addAction("Repair")
                            action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

                            try:
                                if (action == manageItemAction):
                                    self.manageItems(selectedText)
                            except:
                                pass
                            try:
                                if (action == repairAction):
                                    self.repair(selectedText,"0")
                            except:
                                pass
                            try:
                                if (action == modifyRepairAction):
                                    # debug.info("Modify Repair!!!")
                                    self.repair(selectedText,"2")
                            except:
                                pass
                        else:
                            self.messages('white','')
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

        numRows = self.ui.tableWidget.rowCount()
        debug.info(numRows)
        if numRows:
            for row in range(numRows):
                imgCell = self.ui.tableWidget.item(row, 10)
                if imgCell:
                    self.ui.tableWidget.takeItem(row, 10)
                    path = str(imgCell.text())
                    if path:

                        imageButton = QtWidgets.QPushButton()
                        imageButton.setText("Image")
                        imageButton.clicked.connect(lambda x,path=path, button=imageButton: self.loadImageThumbs(path, button))
                        self.ui.tableWidget.setCellWidget(row, 10, imageButton)


        # self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.resizeColumnsToContents()
        debug.info("Loaded list of all items.")

        # image = "/home/sanath.shetty/loading01.gif"
        # pixmap = QtGui.QMovie(image)
        # self.ui.messages.setMovie(pixmap)
        # pixmap.start()

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


    def search(self):
        global theColumn
        self.ui.tableWidget.setSortingEnabled(False)
        self.ui.tableWidget.setRowCount(0)

        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        currTxt = self.ui.comboBox.currentText().strip()
        # debug.info currTxt

        if self.ui.allButton.isChecked():
            # self.allBtnClick()
            txt = str(self.ui.comboBox.currentText().strip()).replace(" ","_")
            debug.info(txt)
            r = re.compile(".*"+txt, re.IGNORECASE)
            txtList = list(filter(r.match, slList+itList+locList+usrList+descList+makeList+modelList))
            debug.info(txtList)
            # txtTup = tuple(txtList)
            # debug.info(len(txtTup))
            # searchColumns = theColumn
            # debug.info(searchColumns)
            searchColumns = ['serial_no','item_type','location','user', 'description', 'make', 'model']

            # qTags = "SELECT * FROM ITEMS WHERE " + (' OR '.join([l+"='{0}'" for l in searchColumns])).format(txtList[0])
            # debug.info(qTags)
            # qTags = "SELECT * FROM ITEMS WHERE " + (' OR '.join([l+" IN '{0}'" for l in searchColumns])).format(txtList[0])
            # debug.info(qTags)

            # query = "SELECT * FROM ITEMS WHERE " + qTags
            # debug.info(query)
            query = ""
            if (len(txtList) == 0):
                return
            elif (len(txtList) ==1):
                # query = "SELECT * FROM ITEMS WHERE serial_no='%s' OR item_type='%s' OR location='%s' OR user='%s'" %(txtList[0],txtList[0],txtList[0],txtList[0])
                query = "SELECT * FROM ITEMS WHERE " + (' OR '.join([l+"='{0}'" for l in searchColumns])).format(txtList[0])
            else:
                # query = "SELECT * FROM ITEMS WHERE serial_no IN %s OR item_type IN %s OR location IN %s OR user IN %s " %(tuple(txtList),tuple(txtList),tuple(txtList),tuple(txtList),)
                query = "SELECT * FROM ITEMS WHERE " + (' OR '.join([l+" IN {0}" for l in searchColumns])).format(tuple(txtList),)

            debug.info(query)
            rows = self.db.execute(query, dictionary=True)
            # debug.info(rows)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable(rows)


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
                        if (currTxt=="REPAIR"):
                            # self.butts["blueButt"+str(n)].customContextMenuRequested.connect(self.repairPopUp)
                            self.butts["blueButt" + str(n)].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                            butt = self.butts["blueButt" + str(n)]
                            self.butts["blueButt" + str(n)].customContextMenuRequested.connect(lambda x, butt=butt, buttText=bl: self.repairPopUp(butt,buttText,x))
                        # if (currTxt == "REPAIR"):
                        #     menu = QtWidgets.QMenu()
                        #     theme = os.environ['GRANTHA_THEME']
                        #     setStyleSheet(menu, theme)
                        #     modifyRepairAction = menu.addAction("Modify Repair")
                        #     action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))
                        #     if (action == viewParentAction):
                        #         self.viewParent()

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
                self.ui.tableWidget.resizeColumnsToContents()
                self.ui.tableWidget.resizeRowsToContents()
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
        global theColumn
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

    def repair(self,item="",index="1"):
        debug.info(item)
        debug.info("Opening Repair Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        if item:
            p.start(sys.executable + " " + Repair + " --item " + item + " --index " + index)
        else:
            p.start(sys.executable + " " + Repair + " --index " + index)

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
        self.messages('white','Connecting...')
        messagebox = TimerMessageBox(1, plceMsg)
        messagebox.exec_()


    def closePlaceTagMessage(self, tagId):
        if (tagId =="Connection Timeout"):
            self.messages('red','<b>Connection Timeout</b>')
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)
            return
        else:
            pass

        global sn
        global theColumn
        # try:
        #     debug.info("Message Closed")
        # except:
        #     debug.info (str(sys.exc_info()))
        #     pass

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

            self.messages('white',' ')
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
        rmT.waiting.connect(self.msg)
        rmT.tagIdReceived.connect(self.updateTable)

        # rmrT.start()
        rmT.start()

        # else:
        #     pass

    def updateTable(self, tagId):
        if (tagId == "MULTI_READ_STARTED"):
            pass

        elif (tagId =="Connection Timeout"):
            self.messages('red','<b>Connection Timeout</b>')
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)
            self.ui.stopReadButton.setEnabled(False)
            return

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
        self.waiting.emit("Connecting...")

        
        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
            # debug.info("connected.")
        except:
            debug.info (str(sys.exc_info()))
        self.socket.send("READ")

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo

        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        try:
            if poller.poll(5 * 1000):  # 10s timeout in milliseconds
                try:
                    debug.info("connected")
                    tagId = self.socket.recv()
                    debug.info("Received Tag Id :" + tagId)
                    self.tagIdReceived.emit(tagId)
                except:
                    debug.info(str(sys.exc_info()))
            else:
                raise IOError("Timeout processing auth request")
        except:
            debug.info(str(sys.exc_info()))
            self.tagIdReceived.emit("Connection Timeout")

        self.socket.close()
        
        if (self.socket.closed == True):
            debug.info( "read Single Socket closed.")


class readMultiThread(QThread):
    waiting = pyqtSignal(str)
    tagIdReceived = pyqtSignal(str)

    def __init__(self, parent):
        super(readMultiThread, self).__init__(parent)
        # self.to = to

    def run(self):
        self.waiting.emit("Connecting...")

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
        except:
            debug.info(str(sys.exc_info()))
        # self.socket.send("READ")
        # self.socket = context.socket(zmq.REQ)
        # self.socket.connect("tcp://192.168.1.183:4689")
        # debug.info("connected.")
        self.socket.send_multipart(["READ_MULTI",ip])

        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        try:
            if poller.poll(5 * 1000):  # 10s timeout in milliseconds
                try:
                    debug.info("connected")
                    # tagId = self.socket.recv()
                    rep = self.socket.recv_multipart()
                    debug.info(rep)
                    # debug.info("Received Tag Id :" + tagId)
                    # self.tagIdReceived.emit(tagId)
                except:
                    debug.info(str(sys.exc_info()))
            else:
                raise IOError("Timeout processing auth request")
        except:
            debug.info(str(sys.exc_info()))
            self.tagIdReceived.emit("Connection Timeout")
            return

        # rep = self.socket.recv_multipart()
        # debug.info (rep)
        # self.socket.close()
        #
        # if (context.closed == True) and (self.socket.closed == True):
        #     debug.info "Socket and Context closed."
        #####################################
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (ip, 4695)
        try:
            sock.bind(server_address)
            debug.info("bind successful")
        except:
            debug.info(str(sys.exc_info()))
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
        self.socket.setsockopt(zmq.LINGER, 0)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
        except:
            debug.info(str(sys.exc_info()))
        # self.socket = context.socket(zmq.REQ)
        # self.socket.connect("tcp://192.168.1.183:4689")
        # debug.info("connected.")

        self.socket.send("STOP")

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        try:
            if poller.poll(5 * 1000):  # 10s timeout in milliseconds
                try:
                    debug.info("connected")
                    ack = self.socket.recv()
                    debug.info(ack)
                    self.ackReceived.emit(ack)
                except:
                    debug.info(str(sys.exc_info()))
            else:
                raise IOError("Timeout processing auth request")
        except:
            debug.info(str(sys.exc_info()))
            self.ackReceived.emit("Connection Timeout")
        # ack = self.socket.recv()
        # debug.info (ack)
        # self.ackReceived.emit(ack)
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

