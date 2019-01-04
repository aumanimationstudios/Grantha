#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
import database
import zmq
import time

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

Add = "Add.py"
Update = "Update.py"
Update_Tag = "Update_Tag.py"
Log = "Log.py"
Modify = "Modify.py"

aU = database.DataBase().getAuthUsers()
authUsers = [x['auth_users'] for x in aU]

user = os.environ['USER']

class mainWindow():
    def __init__(self):
        # super(myWindow, self).__init__()
        self.rfidMultiCount = 0
        self.rfidMultiUniqSlno = {}
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Grantha.ui'))

        self.ui.allButton.pressed.connect(self.allBtnClick)
        self.ui.serialNoButton.pressed.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.pressed.connect(self.itBtnClick)
        self.ui.locationButton.pressed.connect(self.locBtnClick)
        self.ui.userButton.pressed.connect(self.usrBtnClick)

        self.ui.comboBox.currentIndexChanged.connect(self.search)

        if user in authUsers:
            self.ui.addButton.clicked.connect(self.add)
            self.ui.updateButton.clicked.connect(self.update)
            self.ui.updateTagButton.clicked.connect(self.updateTag)
            self.ui.modifyButton.clicked.connect(self.modify)
            self.ui.logButton.clicked.connect(self.log)
            self.ui.readSingleButton.clicked.connect(self.readFromRfidTag)
            self.ui.readMultiButton.clicked.connect(self.readMultiFromRfidTag)

        self.ui.setWindowTitle('GRANTHA')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))

        self.ui.tableWidget.customContextMenuRequested.connect(self.viewParentPopUp)

        self.center()
        self.ui.show()

        self.db = database.DataBase()

    def viewParentPopUp(self,pos):
        # a = self.ui.tableWidget.horizontalHeaderItem(8).text()
        #
        # print a

        selectedCellIndex = self.ui.tableWidget.selectedIndexes()
        for index in selectedCellIndex:
            selectedColumnIndex = index.column()

            selectedColumnLabel = self.ui.tableWidget.horizontalHeaderItem(selectedColumnIndex).text()
            # print selectedColumnLabel

            if (selectedColumnLabel == "location"):
                menu = QtWidgets.QMenu()
                # view = QtWidgets.QMenu()
                # view.setTitle("view parent location")
                # menu.addMenu(view)
                try:
                    selected = self.ui.tableWidget.selectedItems()
                except:
                    selected = None

                if(selected):
                    viewParentAction = menu.addAction("View Parent Location")
                    if user in authUsers:
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
        # print selectedText
        loc = self.db.listOfLocation()
        LOC = [x['location'] for x in loc]
        # print LOC
        if selectedText in LOC:
            query = "SELECT parent_location FROM LOCATION WHERE location='%s' " %(selectedText)
            pL = self.db.getParentLocation(query)
            self.parentLocation = pL['parent_location']
            # print self.parentLocation
            if self.parentLocation == None:
                self.parentMessage = "No Parent Location"
            else:
                self.parentMessage = self.parentLocation

            self.viewParentMessage()
        else:
            print "not valid location"

    def viewParentMessage(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText(self.parentMessage)
        msg.exec_()

    def center(self):
        qr = self.ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())


    def allBtnClick(self):
        # self.ui.tableWidget.setSortingEnabled(False)
        # self.ui.tableWidget.resizeColumnsToContents()
        #db = database.DataBase()
        self.ui.tableWidget.setRowCount(0)

        self.ui.comboBox.clearEditText()
        column = self.db.getColumns()
        theColumn = [x['COLUMN_NAME'] for x in column]
        self.ui.tableWidget.setColumnCount(len(theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(theColumn)

        theRows = self.db.getAllRows()
        self.ui.tableWidget.setRowCount(len(theRows))

        row = 0
        self.db.getAllValues(init=True)
        while True:
            primaryResult = self.db.getAllValues()
            # print primaryResult
            if (not primaryResult):
                break
            col = 0
            for n in theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        self.ui.tableWidget.resizeColumnsToContents()
        print "Loaded list of all items."
        # self.ui.tableWidget.setSortingEnabled(True)

    # def readFromRfidTag(self):
    #     self.context = zmq.Context()
    #     print("connecting to rfidScanServer...")
    #     self.socket = self.context.socket(zmq.REQ)
    #     self.socket.connect("tcp://192.168.1.206:4689")
    #
    #     self.socket.send("READ")
    #
    #     slNo = self.socket.recv()
    #
    #     # self.ui.serialNoBox.clear()
    #     self.ui.comboBox.setEditText(slNo)
    #
    #     column = self.db.getColumns()
    #     self.theColumn = [x['COLUMN_NAME'] for x in column]
    #
    #     self.ui.tableWidget.setColumnCount(len(self.theColumn))
    #     self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)
    #
    #     currTxt = self.ui.comboBox.currentText()
    #
    #     self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
    #     rows = self.db.getRows(self.query)
    #     self.ui.tableWidget.setRowCount(len(rows))
    #     self.fillTable()


    def search(self):
        self.ui.tableWidget.setRowCount(0)

        column = self.db.getColumns()
        self.theColumn = [x['COLUMN_NAME'] for x in column]

        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        currTxt = self.ui.comboBox.currentText()
        # print currTxt

        if self.ui.serialNoButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
            rows = self.db.getRows(self.query)
            # print rows
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.itemTypeButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE item_type='%s' " %(currTxt)
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.locationButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE location='%s' " %(currTxt)
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.userButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE user='%s' " %(currTxt)
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        # else:
        #     self.message()

    def fillTable(self):
        row = 0
        self.db.getValues(self.query,init=True)
        while True:
            primaryResult = self.db.getValues(self.query)
            # print primaryResult
            if (not primaryResult):
                break
            col = 0
            for n in self.theColumn:
                result = primaryResult[n]
                self.ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(result)))
                col +=1
            row +=1

        self.ui.tableWidget.resizeColumnsToContents()




    def slNoBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        theList = self.db.Completer()
        slList = [x['serial_no'] for x in theList]
        slList.sort()
        self.ui.comboBox.addItems(slList)
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(slList)
        # self.completer()

    def itBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        theList = self.db.Completer()
        itList = list(set([x['item_type'] for x in theList]))
        itList.sort()
        self.ui.comboBox.addItems(itList)
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(itList)
        # self.completer()

    def locBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        theList = self.db.Completer()
        locList = list(set([x['location'] for x in theList]))
        locList.sort()
        self.ui.comboBox.addItems(locList)
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(locList)
        # self.completer()

    def usrBtnClick(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.clearEditText()
        theList = self.db.Completer()
        usrList = list(set([x['user'] for x in theList]))
        usrList.sort()
        self.ui.comboBox.addItems(usrList)
        # self.model = QtCore.QStringListModel()
        # self.model.setStringList(usrList)
        # self.completer()

    # def completer(self):
    #     completer = QtWidgets.QCompleter()
    #     completer.setModel(self.model)
    #     completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    #     self.ui.comboBox.setCompleter(completer)

    # def message(self):
    #     QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(),"Error!","Please Check Input.")

    def add(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Add.split())

    def update(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Update.split())

    def updateTag(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Update_Tag.split())

    def modify(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Modify.split())

    def log(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Log.split())



    def readFromRfidTag(self):
        rT = readThread(app)
        rT.waiting.connect(self.openPlaceTagMessage)
        rT.slNoReceived.connect(self.closePlaceTagMessage)
        rT.start()

    def openPlaceTagMessage(self):
        self.plcMsg = QtWidgets.QMessageBox()
        self.plcMsg.setIcon(QtWidgets.QMessageBox.Information)
        self.plcMsg.setWindowTitle("Message")
        self.plcMsg.setText("Place your Tag...")
        self.plcMsg.show()

    def closePlaceTagMessage(self, slNo):
        try:
            self.plcMsg.close()
        except:
            pass

        sn = self.db.listOfSerialNo()
        SN = [x['serial_no'] for x in sn]
        if slNo in SN:
            # print "received sl.no: "+slNo
            self.ui.comboBox.setEditText(slNo)

            column = self.db.getColumns()
            self.theColumn = [x['COLUMN_NAME'] for x in column]

            self.ui.tableWidget.setColumnCount(len(self.theColumn))
            self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

            currTxt = self.ui.comboBox.currentText()

            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()
        else:
            self.wrongTagMessage()

    def wrongTagMessage(self):
            self.Msg = QtWidgets.QMessageBox()
            self.Msg.setIcon(QtWidgets.QMessageBox.Information)
            self.Msg.setWindowTitle("Wrong Tag")
            self.Msg.setText("This Serial No. does not exists in Database \n And/Or \n Tag was not scanned properly!")
            self.Msg.show()



    def readMultiFromRfidTag(self):
        self.ui.tableWidget.setRowCount(0)
        timeout = str(self.ui.spinBox.value())

        if self.ui.readMultipleButton.isChecked():
            self.ui.readMultiButton.setEnabled(False)
            self.rfidMultiUniqSlno.clear()
            self.rfidMultiCount = 0

            rmrT = readMultiReplyThread(app)
            rmT = readMultiThread(timeout, app)

            rmrT.slNoReceived.connect(self.updateTable)
            rmrT.finished.connect(self.readButtonEnable)
            rmT.ackReceived.connect(self.showTimeout)

            rmrT.start()
            rmT.start()

        else:
            pass

    def updateTable(self, slNo):
        sn = self.db.listOfSerialNo()
        SN = [x['serial_no'] for x in sn]

        if slNo in SN:
            if (self.rfidMultiUniqSlno.has_key(slNo)):
                return

            self.rfidMultiUniqSlno[slNo] = 1
            print self.rfidMultiUniqSlno

            self.rfidMultiCount += 1
            self.ui.comboBox.setEditText(slNo)

            column = self.db.getColumns()
            self.theColumn = [x['COLUMN_NAME'] for x in column]

            self.ui.tableWidget.setColumnCount(len(self.theColumn))
            self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

            self.ui.tableWidget.setRowCount(self.rfidMultiCount)

            currTxt = self.ui.comboBox.currentText()

            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " % (currTxt)

            # rows = self.db.getRows(self.query)
            # self.ui.tableWidget.setRowCount(len(rows))

            rowCount = self.ui.tableWidget.rowCount()

            row = rowCount-1

            self.db.getValues(self.query, init=True)
            while True:
                primaryResult = self.db.getValues(self.query)
                # print primaryResult
                if (not primaryResult):
                    break
                col = 0
                for n in self.theColumn:
                    result = primaryResult[n]
                    self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
                    col += 1
                row += 1

            self.ui.tableWidget.resizeColumnsToContents()

            # self.ui.readMultiButton.setEnabled(True)

        else:
            self.wrongTagMessage()

    def readButtonEnable(self):
        self.ui.readMultiButton.setEnabled(True)

    def showTimeout(self):
        timeout = self.ui.spinBox.value()
        print "timeout: " + str(timeout) + "sec"

        ui = uic.loadUi(os.path.join(uiFilePath,'timer.ui'))

        ui.progressBar.setMaximum(timeout)
        ui.progressBar.setMinimum(0)


        svT = setValueToTimerThread(timeout, app)
        svT.sending.connect(lambda n , uiObj=ui: self.setValue(n, uiObj))
        svT.finished.connect(lambda uiObj=ui: self.closeTimer(uiObj))
        svT.start()

        ui.show()

    def setValue(self, n, uiObj):
        uiObj.progressBar.setValue(n)
        uiObj.progressBar.setFormat(str(n)+' sec')

    def closeTimer(self, uiObj):
        uiObj.deleteLater()






class readThread(QtCore.QThread):
    waiting = QtCore.pyqtSignal()
    slNoReceived = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(readThread, self).__init__(parent)

    def run(self):
        self.waiting.emit()

        self.context = zmq.Context()
        print("connecting to rfid Scanner Server...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")

        self.socket.send("READ")

        slNo = self.socket.recv()
        print "received sl.No: " + slNo

        self.slNoReceived.emit(slNo)


class readMultiThread(QtCore.QThread):
    waiting = QtCore.pyqtSignal()
    ackReceived = QtCore.pyqtSignal(str)

    def __init__(self, to, parent):
        super(readMultiThread, self).__init__(parent)
        self.to = to

    def run(self):
        self.waiting.emit()

        self.context = zmq.Context()
        print("connecting to rfid Scanner Server...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")

        self.socket.send("READ_MULTI")

        rep = self.socket.recv()

        if (rep == "GIVE_TIMEOUT"):
            self.socket.send(self.to)

        ack = self.socket.recv()

        if (ack == "ackPass"):
            self.ackReceived.emit(ack)
        else:
            pass


class readMultiReplyThread(QtCore.QThread):
    slNoReceived = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(readMultiReplyThread, self).__init__(parent)

    def run(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://192.168.1.39:4690")

        while True:
            slNo = self.socket.recv()
            self.socket.send("received")
            print "received sl.No: " + slNo

            if(slNo == "FUCKINGDONE"):
                print "exiting"
                self.socket.close()
                self.context.term()
                break


            self.slNoReceived.emit(slNo)


class setValueToTimerThread(QtCore.QThread):
    sending = QtCore.pyqtSignal(int)

    def __init__(self, to, parent):
        QtCore.QThread.__init__(self,parent)
        self.to = to

    def run(self):
        for n in range(0, self.to+1):
            self.sending.emit(n)
            time.sleep(1)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

