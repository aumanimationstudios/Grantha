#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,QtCore,uic
import database
import zmq

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
uiFilePath = os.path.join(progPath,"GUI","uiFiles")
imgFilePath = os.path.join(progPath, "GUI","imageFiles")

sys.path.append(uiFilePath)
sys.path.append(imgFilePath)


class updateTagWidget():
    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiFilePath, 'Update_Tag.ui'))

        self.db = database.DataBase()

        self.load()
        self.ui.clearButton.clicked.connect(self.clear)
        self.ui.saveButton.clicked.connect(self.confirmation)

        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imgFilePath, 'granthaLogo.png')))
        self.ui.show()
        self.ui.cancelButton.clicked.connect(self.ui.close)


    def load(self):
        sn = self.db.listOfSerialNo()
        SN = [x['serial_no'] for x in sn]
        self.ui.serialNoBox.clear()
        self.ui.serialNoBox.addItems(SN)

    def clear(self):
        self.load()

    def confirmation(self):
            confirm = QtWidgets.QMessageBox()
            confirm.setIcon(QtWidgets.QMessageBox.Question)
            confirm.setWindowTitle("Confirmation")
            confirm.setInformativeText("<b>Are you sure you want to save?</b>")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            cnfrm = confirm.exec_()

            if cnfrm == QtWidgets.QMessageBox.Ok:
                self.updateTag()
            else:
                pass

    def updateTag(self):
        self.writeToTag = self.writeToRfidTag()

    def writeToRfidTag(self):
        idText = self.ui.serialNoBox.currentText()
        wT = writeThread(app, idText)
        wT.waiting.connect(self.openplaceTagMessage)
        wT.confirmation.connect(self.closePlaceTagMessage)
        wT.start()

    def openplaceTagMessage(self):
        self.plcMsg = QtWidgets.QMessageBox()
        self.plcMsg.setIcon(QtWidgets.QMessageBox.Information)
        self.plcMsg.setWindowTitle("Message")
        self.plcMsg.setText("Place your Tag...")
        self.plcMsg.show()

    def closePlaceTagMessage(self, msg):
        self.plcMsg.setText(msg )
        self.load()

class writeThread(QtCore.QThread):

    waiting = QtCore.pyqtSignal()
    confirmation = QtCore.pyqtSignal(str)

    def __init__(self, parent, idText):
        super(writeThread, self).__init__(parent)
        self.idText = idText

    def run(self):
        self.waiting.emit()

        self.context = zmq.Context()
        print("connecting to rfidScanServer...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://192.168.1.183:4689")

        self.socket.send("WRITE_TAG")

        msgFrmServ = self.socket.recv()

        if (msgFrmServ == "INPUT"):
            text = str(self.idText)
            self.socket.send(text)

            msgFrmServ = self.socket.recv()
            print msgFrmServ
            self.confirmation.emit(msgFrmServ)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = updateTagWidget()
    sys.exit(app.exec_())

