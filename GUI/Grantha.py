#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtWidgets import QDesktopWidget
import database
import zmq

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)

Add = "Add.py"
Update = "Update.py"
Log = "Log.py"
Modify = "Modify.py"

aU = database.DataBase().getAuthUsers()
authUsers = [x['auth_users'] for x in aU]

user = os.environ['USER']

class mainWindow():
    def __init__(self):
        # super(myWindow, self).__init__()
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Grantha.ui'))

        self.ui.allButton.pressed.connect(self.allBtnClick)
        self.ui.serialNoButton.pressed.connect(self.slNoBtnClick)
        self.ui.itemTypeButton.pressed.connect(self.itBtnClick)
        self.ui.locationButton.pressed.connect(self.locBtnClick)
        self.ui.userButton.pressed.connect(self.usrBtnClick)

        # self.ui.searchButton.clicked.connect(self.search)
        self.ui.comboBox.currentIndexChanged.connect(self.search)

        if user in authUsers:
            self.ui.addButton.clicked.connect(self.add)
            self.ui.updateButton.clicked.connect(self.update)
            self.ui.modifyButton.clicked.connect(self.modify)
            self.ui.logButton.clicked.connect(self.log)
            self.ui.fromTagButton.clicked.connect(self.readFromRfidTag)

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
        column = self.db.getColumns()
        self.theColumn = [x['COLUMN_NAME'] for x in column]

        self.ui.tableWidget.setColumnCount(len(self.theColumn))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)

        if self.ui.serialNoButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(self.ui.comboBox.currentText())
            rows = self.db.getRows(self.query)
            # print rows
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.itemTypeButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE item_type='%s' " %(self.ui.comboBox.currentText())
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.locationButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE location='%s' " %(self.ui.comboBox.currentText())
            rows = self.db.getRows(self.query)
            self.ui.tableWidget.setRowCount(len(rows))
            self.fillTable()

        if self.ui.userButton.isChecked():
            self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE user='%s' " %(self.ui.comboBox.currentText())
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

    def modify(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Modify.split())

    def log(self):
        p = QtCore.QProcess(parent=self.ui)
        p.start(sys.executable, Log.split())

    def readFromRfidTag(self):
        rT = readThread(app)
        rT.waiting.connect(self.openplaceTagMessage)
        rT.slNoReceived.connect(self.closePlaceTagMessage)
        rT.start()

    def openplaceTagMessage(self):
        self.plcMsg = QtWidgets.QMessageBox()
        self.plcMsg.setIcon(QtWidgets.QMessageBox.Information)
        self.plcMsg.setWindowTitle("Message")
        self.plcMsg.setText("Place your Tag...")
        self.plcMsg.show()

    def closePlaceTagMessage(self, slNo):
        self.plcMsg.close()

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

class readThread(QtCore.QThread):
    waiting = QtCore.pyqtSignal()
    slNoReceived = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(readThread, self).__init__(parent)

    def run(self):
        self.waiting.emit()

        self.context = zmq.Context()
        print("connecting to rfidScanServer...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.206:4689")

        self.socket.send("READ")

        slNo = self.socket.recv()

        self.slNoReceived.emit(slNo)

        # self.ui.serialNoBox.clear()
        # self.ui.comboBox.setEditText(slNo)


        # column = self.db.getColumns()
        # self.theColumn = [x['COLUMN_NAME'] for x in column]
        #
        # self.ui.tableWidget.setColumnCount(len(self.theColumn))
        # self.ui.tableWidget.setHorizontalHeaderLabels(self.theColumn)
        #
        # currTxt = self.ui.comboBox.currentText()
        #
        # self.query = "SELECT " + ','.join(self.theColumn) + " FROM ITEMS WHERE serial_no='%s' " %(currTxt)
        # rows = self.db.getRows(self.query)
        # self.ui.tableWidget.setRowCount(len(rows))
        # self.fillTable()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

