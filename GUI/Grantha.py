#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

### rfidUhfServer Script Should be running in machine connected to RFID Reader Module to use rfid options###

import os
import sys
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
Modify = os.path.join(fileDir, "Modify.py")
Log = os.path.join(fileDir, "Log.py")
Find_Tag = os.path.join(fileDir, "Find_Tag.py")

user = os.environ['USER']
context = zmq.Context()
processes = []
# tempDir = tempfile.gettempdir()
mapPath = os.path.join(imageDir, "map.svg")


class mainWindow():
    global processes

    # Database query execution function
    db = dbGrantha.dbGrantha()

    # List Authorized users to access modify functions
    getAuthUsers = "SELECT * FROM AUTH_USERS"
    aU = db.execute(getAuthUsers,dictionary=True)
    authUsers = [x['auth_users'] for x in aU]

    getLOC = "SELECT location FROM LOCATION"
    loc = db.execute(getLOC, dictionary=True)
    LOC = [x['location'] for x in loc]

    queryCol = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"
    column = db.execute(queryCol, dictionary=True)
    theColumn = [x['COLUMN_NAME'] for x in column]

    completer = "SELECT serial_no,item_type,location,user FROM ITEMS"
    theList = db.execute(completer, dictionary=True)
    slList = [x['serial_no'] for x in theList]
    itList = list(set([x['item_type'] for x in theList]))
    locList = list(set([x['location'] for x in theList]))
    usrList = list(set([x['user'] for x in theList]))

    getSN = "SELECT * FROM SERIAL_NO"
    sn = db.execute(getSN, dictionary=True)
    # slNoList = [x['serial_no'] for x in sn]

    def __init__(self):
        # super(myWindow, self).__init__()
        self.rfidMultiCount = 0
        self.rfidMultiUniqSlno = {}
        self.ui = uic.loadUi(os.path.join(uiDir, 'Grantha.ui'))

        self.ui.allButton.pressed.connect(self.allBtnClick)
        self.ui.serialNoButton.pressed.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.pressed.connect(self.itBtnClick)
        self.ui.locationButton.pressed.connect(self.locBtnClick)
        self.ui.userButton.pressed.connect(self.usrBtnClick)

        self.ui.comboBox.currentIndexChanged.connect(self.search)

        if user in self.authUsers:
            self.ui.manageItemsButton.clicked.connect(self.manageItems)
            self.ui.rfidToolsButton.clicked.connect(self.rfidTools)
            # self.ui.updateButton.clicked.connect(self.update)
            # self.ui.updateTagButton.clicked.connect(self.updateTag)
            self.ui.modifyButton.clicked.connect(self.modify)
            self.ui.findTagButton.clicked.connect(self.findTag)
            self.ui.logButton.clicked.connect(self.log)
            self.ui.readSingleButton.clicked.connect(self.readFromRfidTag)
            self.ui.readMultiButton.clicked.connect(self.readMultiFromRfidTag)
            self.ui.stopReadButton.setEnabled(False)
            self.ui.stopReadButton.clicked.connect(self.stopRead)

        self.ui.setWindowTitle('GRANTHA')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))

        self.ui.tableWidget.customContextMenuRequested.connect(self.viewParentPopUp)

        self.setMap()

        self.center()
        self.ui.showMaximized()

        setStyleSheet(self.ui)

    def loadMap(self):
        doc = xml.dom.minidom.parse(mapPath)
        name = doc.getElementsByTagName('tspan')
        ids = []
        for t in name:
            id = str(t.attributes['id'].value)
            ids.append(id)

        getLOC = "SELECT * FROM LOCATION"
        LOC = self.db.execute(getLOC, dictionary=True)
        pLoc = [x['parent_location'] for x in LOC]
        loc = [x['location'] for x in LOC]

        for lc in loc:
            if lc in ids:
                for x in LOC:
                    if x['location'] == lc:
                        nloc = x['parent_location']
                        for t in name:
                            if (t.attributes['id'].value == lc):
                                t.childNodes[0].nodeValue = nloc

        for pl in pLoc:
            if pl in ids:
                for x in LOC:
                    if x['parent_location'] == pl:
                        bloc = x['location']
                        for t in name:
                            if (t.attributes['id'].value == pl):
                                t.childNodes[0].nodeValue = bloc

        f = open(mapPath, "w")
        f.write(doc.toxml())
        f.close()


    def setMap(self):
        self.loadMap()
        layout = QtWidgets.QVBoxLayout()
        self.ui.frame.setLayout(layout)
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        imageThumbMap = ImageWidget(mapPath, 32)
        # imageThumbMap.clicked.connect(lambda x, imagePath = mapPath: imageWidgetClicked(imagePath))
        imageThumbMap.clicked.connect(self.showMap)
        layout.addWidget(imageThumbMap)

    def showMap(self):
        self.loadMap()
        imageWidgetClicked(mapPath)


    def viewParentPopUp(self,pos):

        selectedCellIndex = self.ui.tableWidget.selectedIndexes()
        for index in selectedCellIndex:
            selectedColumnIndex = index.column()

            selectedColumnLabel = self.ui.tableWidget.horizontalHeaderItem(selectedColumnIndex).text()
            # debug.info selectedColumnLabel

            if (selectedColumnLabel == "location"):
                menu = QtWidgets.QMenu()

                try:
                    selected = self.ui.tableWidget.selectedItems()
                except:
                    selected = None

                if(selected):
                    viewParentAction = menu.addAction("View Parent Location")
                    if user in self.authUsers:
                        modifyLocationAction = menu.addAction("Modify Location")

                action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

                if(selected):
                    if (action == viewParentAction):
                        self.viewParent()
                    try:
                        if (action == modifyLocationAction):
                            self.modify()
                    except:
                        pass
            else:
                pass


    def viewParent(self):
        selectedText = self.ui.tableWidget.currentItem().text()
        # debug.info selectedText

        if selectedText in self.LOC:
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
            messageBox(parentMessage)
            # self.viewParentMessage()
        else:
            debug.info ("not valid location")


    def center(self):
        qr = self.ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())


    def allBtnClick(self):
        self.ui.tableWidget.setSortingEnabled(False)
        # self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.setRowCount(0)

        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()

        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

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
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        numRows = self.ui.tableWidget.rowCount()
        paths = {}
        for row in range(numRows):
            path = str(self.ui.tableWidget.item(row, 10).text())
            paths[row]=path

        if paths:
            for x in paths.keys():
                if paths[x]:
                    # debug.info(paths[x])
                    self.ui.tableWidget.takeItem(x, 10)
                    imageThumb = ImageWidget(paths[x], 32)
                    imageThumb.clicked.connect(lambda x, imagePath=paths[x]: imageWidgetClicked(imagePath))
                    self.ui.tableWidget.setCellWidget(x, 10, imageThumb)
                else:
                    pass
        # self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.resizeColumnsToContents()
        debug.info( "Loaded list of all items.")
        self.ui.tableWidget.setSortingEnabled(True)


    def search(self):
        self.ui.tableWidget.setRowCount(0)

        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        currTxt = self.ui.comboBox.currentText().strip()
        # debug.info currTxt

        if self.ui.serialNoButton.isChecked():
            if (currTxt in self.slList):
                getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                # debug.info rows
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass

        if self.ui.itemTypeButton.isChecked():
            if (currTxt in self.itList):
                getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE item_type='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass

        if self.ui.locationButton.isChecked():
            if (currTxt in self.locList):
                getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE location='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass

        if self.ui.userButton.isChecked():
            if (currTxt in self.usrList):
                getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE user='%s' " %(currTxt)
                # rows = self.db.getRows(self.query)
                rows = self.db.execute(getRows, dictionary=True)
                self.ui.tableWidget.setRowCount(len(rows))
                self.fillTable(rows)
            else:
                pass


    def fillTable(self,rows):
        row = 0
        while True:
            if (row == len(rows)):
                break
            primaryResult = rows[row]
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                col += 1
            row += 1

        # self.ui.tableWidget.resizeColumnsToContents()

        numRows = self.ui.tableWidget.rowCount()
        for row in range(numRows):
            path = str(self.ui.tableWidget.item(row, 10).text())
            if path:
                # debug.info(path)
                self.ui.tableWidget.takeItem(row, 10)
                imageThumb = ImageWidget(path, 32)
                imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                self.ui.tableWidget.setCellWidget(row, 10, imageThumb)

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def slNoBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        # completer = "SELECT serial_no,item_type,location,user FROM ITEMS"
        # # theList = self.db.Completer()
        # theList = self.db.execute(completer,dictionary=True)
        # slList = [x['serial_no'] for x in theList]
        self.slList.sort()
        self.ui.comboBox.addItems(self.slList)
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(slList)
        # self.completer()

    def itBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        self.itList.sort()
        self.ui.comboBox.addItems(self.itList)

    def locBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        self.locList.sort()
        self.ui.comboBox.addItems(self.locList)

    def usrBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        self.usrList.sort()
        self.ui.comboBox.addItems(self.usrList)


    # Processes to start when respective buttons are clicked

    def manageItems(self):
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
        p.start(sys.executable, Manage_Items.split())

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

    def modify(self):
        debug.info("Opening Modify Menu")
        p = QProcess(parent=self.ui)
        processes.append(p)
        debug.info(processes)
        p.started.connect(self.disableButtons)
        p.readyReadStandardOutput.connect(self.read_out)
        p.readyReadStandardError.connect(self.read_err)
        p.finished.connect(self.enableButtons)
        p.start(sys.executable, Modify.split())

    def log(self):
        pass
        # p = QProcess(parent=self.ui)
        # p.start(sys.executable, Log.split())

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
        self.ui.logButton.setEnabled(False)
        self.ui.findTagButton.setEnabled(False)


    def enableButtons(self):
        self.ui.readSingleButton.setEnabled(True)
        self.ui.readMultiButton.setEnabled(True)
        self.ui.manageItemsButton.setEnabled(True)
        self.ui.rfidToolsButton.setEnabled(True)
        self.ui.modifyButton.setEnabled(True)
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

        TI = [x['tag_id'] for x in self.sn]
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

            self.ui.tableWidget.setColumnCount(len(self.theColumn))
            self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

            currTxt = self.ui.comboBox.currentText().strip()

            getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " % (currTxt)
            rows = self.db.execute(getRows, dictionary=True)

            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable(rows)
            self.ui.readSingleButton.setEnabled(True)
            self.ui.readMultiButton.setEnabled(True)

        else:
            messageBox("<b>This Serial No. does not exists in Database</b> \n And/Or \n <b>Tag was not scanned properly!</b>","",os.path.join(imageDir,"oh.png"))
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

            TI = [x['tag_id'] for x in self.sn]
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
                # self.theColumn = [x['COLUMN_NAME'] for x in column]

                self.ui.tableWidget.setColumnCount(len(self.theColumn))
                self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

                self.ui.tableWidget.setRowCount(self.rfidMultiCount)

                currTxt = self.ui.comboBox.currentText()
                getRows = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " % (currTxt)
                rows = self.db.execute(getRows, dictionary=True)
                # debug.info(rows)
                # rows = self.db.getRows(self.query)
                # self.ui.tableWidget.setRowCount(len(rows))

                rowCount = self.ui.tableWidget.rowCount()


                row = rowCount -1
                while True:
                    primaryResult = rows[0]
                    # debug.info(primaryResult)
                    col = 0
                    for n in self.theColumn:
                        result = primaryResult[n]
                        self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                        col += 1
                    row += 1
                    break

                numRow = self.rfidMultiCount -1
                path = str(self.ui.tableWidget.item(numRow, 10).text())
                if path:
                    # debug.info(path)
                    self.ui.tableWidget.takeItem(numRow, 10)
                    imageThumb = ImageWidget(path, 32)
                    imageThumb.clicked.connect(lambda x, imagePath=path: imageWidgetClicked(imagePath))
                    self.ui.tableWidget.setCellWidget(numRow, 10, imageThumb)

                self.ui.tableWidget.resizeRowsToContents()
                self.ui.tableWidget.resizeColumnsToContents()

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
        rep = self.socket.recv()
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



if __name__ == '__main__':
    setproctitle.setproctitle("GRANTHA")

    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

