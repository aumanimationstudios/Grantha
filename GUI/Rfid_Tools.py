#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
from PyQt5 import QtGui,QtWidgets,uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import dbGrantha
import random
import zmq
import debug
from Utils_Gui import *
import setproctitle

filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-2])
uiDir = os.path.join(projDir,"GUI","uiFiles")
imageDir = os.path.join(projDir, "GUI","imageFiles")

sys.path.append(uiDir)
sys.path.append(imageDir)

context = zmq.Context()

class rfidToolsWidget():
    db = dbGrantha.dbGrantha()

    getSN = "SELECT * FROM SERIAL_NO"
    sn = db.execute(getSN,dictionary=True)


    def __init__(self):
        self.ui = uic.loadUi(os.path.join(uiDir, 'Rfid_Tools.ui'))
        # self.db = database.DataBase()
        self.ui.readButton.clicked.connect(self.readFromRfidTag)
        self.ui.randomHexButton.clicked.connect(self.randomHexGen)
        self.ui.writeButton.clicked.connect(self.writeToRfidTag)

        self.ui.statusBox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.statusBox.customContextMenuRequested.connect(self.setStatus)


        self.ui.setWindowTitle('Rfid Tools')
        self.ui.setWindowIcon(QtGui.QIcon(os.path.join(imageDir, 'granthaLogo.png')))
        self.ui.show()

        # setStyleSheet(self.ui)
        try:
            theme = os.environ['GRANTHA_THEME']
            debug.info(theme)
            setStyleSheet(self.ui, theme)
        except:
            pass

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
        # self.clearAll()
        self.ui.tagIdBox.clear()
        self.ui.serialNoBox.clear()
        self.ui.statusBox.clear()
        self.ui.tagIdBox.setText(tagId)
        # ti = self.db.listOfSerialNo()
        TI = [x['tag_id'] for x in self.sn]

        # tagIdList = self.db.getTagIdList()
        getTagId = "SELECT * FROM TAG_ID"
        tagIdList = self.db.execute(getTagId, dictionary=True)

        TIL = {x['id']:x['status'] for x in tagIdList}
        debug.info(tagIdList)
        debug.info(TIL)
        self.enableWriteButtons()
        if tagId in TIL:
            tagIdStatus = TIL[tagId]
            debug.info(tagIdStatus)

            if (tagIdStatus == 1):
                self.disableWriteButtons()
                self.ui.statusBox.setText("ACTIVE")
                if tagId in TI:
                    getSlFrmTid = "SELECT serial_no FROM SERIAL_NO WHERE tag_id=\"{}\" ".format(tagId)
                    # slno = self.db.getSlFrmTid(tagId)
                    slno = self.db.execute(getSlFrmTid, dictionary=True)
                    slno = slno[0]
                    slNo = slno['serial_no']
                    self.ui.serialNoBox.setText(slNo)
                    # self.fillDetails()
            if (tagIdStatus == 0):
                self.ui.statusBox.setText("INACTIVE")
        elif (tagId=="NO CARD"):
            self.ui.statusBox.setText("NO CARD")
        else:
            self.ui.statusBox.setText("NEW CARD")

    def enableWriteButtons(self):
        self.ui.randomHexBox.setEnabled(True)
        self.ui.randomHexButton.setEnabled(True)
        self.ui.writeButton.setEnabled(True)

    def disableWriteButtons(self):
        self.ui.randomHexBox.setEnabled(False)
        self.ui.randomHexButton.setEnabled(False)
        self.ui.writeButton.setEnabled(False)


    def setStatus(self,pos):
        menu = QtWidgets.QMenu()

        activateAction = menu.addAction("Activate")
        deactivateAction = menu.addAction("Deactivate")
        if (self.ui.statusBox.text()=="INACTIVE"):
            activateAction.setEnabled(True)
            deactivateAction.setEnabled(False)
        if (self.ui.statusBox.text()=="ACTIVE"):
            activateAction.setEnabled(False)
            deactivateAction.setEnabled(True)
        if (self.ui.statusBox.text()=="NEW CARD"):
            activateAction.setEnabled(False)
            deactivateAction.setEnabled(False)
        if (self.ui.statusBox.text()==""):
            activateAction.setEnabled(False)
            deactivateAction.setEnabled(False)

        action = menu.exec_(self.ui.statusBox.mapToGlobal(pos))

        try:
            if (action==activateAction):
                self.activateTag()
            if (action==deactivateAction):
                self.deactivateTag()
        except:
            debug.info(str(sys.exc_info()))

    def activateTag(self):
        debug.info("Activating")
        tagId = self.ui.tagIdBox.text()
        if tagId:
            query = "UPDATE TAG_ID SET status=\"1\" WHERE id =\"" + tagId + "\""
            debug.info(query)
            # updated = self.db.update(query)
            updated = self.db.execute(query)
            debug.info(updated)
            # if (updated=="Updated Successfully"):
            if (updated==1):
                self.ui.statusBox.setText("ACTIVE")
                self.ui.textEdit.append("Activated")

    def deactivateTag(self):
        debug.info("Deactivating")
        tagId = self.ui.tagIdBox.text()
        if tagId:
            query = "UPDATE TAG_ID SET status=\"0\" WHERE id =\"" + tagId + "\""
            debug.info(query)
            # updated = self.db.update(query)
            updated = self.db.execute(query)
            debug.info(updated)
            # if (updated=="Updated Successfully"):
            if (updated==1):
                self.ui.statusBox.setText("INACTIVE")
                self.ui.textEdit.append("Deactivated")


    def randomHexGen(self):
        randomHex = ""
        for i in range(0, 8):
            randomHex = randomHex + str(random.choice("0123456789ABCDEF"))
        debug.info(randomHex)

        getTagId = "SELECT id FROM TAG_ID"
        tagIdList = self.db.execute(getTagId, dictionary=True)
        TIL = [x['id'] for x in tagIdList]

        if randomHex in TIL:
            self.randomHexGen()
        else:
            self.ui.randomHexBox.setText(randomHex)


    def writeToRfidTag(self):
        print("writing")
        tagId = str(self.ui.randomHexBox.text())
        if tagId:
            wT = writeThread(tagId, app)
            wT.waiting.connect(self.writeStarting)
            wT.ackReceived.connect(self.writeDone)
            wT.start()
        else:
            self.ui.textEdit.append("No Tag Id to Write")

    def writeStarting(self):
        self.ui.textEdit.append("Writing")

    def writeDone(self,ack):
        if (ack=="ack_pass"):
            self.ui.textEdit.append("Writing Done")
            self.addTagIdToDb()
        else:
            self.ui.textEdit.append(ack)

    def addTagIdToDb(self):
        tagId = str(self.ui.randomHexBox.text())
        query = "INSERT INTO TAG_ID (id) VALUES (\"{0}\") ".format(tagId)
        debug.info(query)
        # addTagId = self.db.insertTagId(query)
        addTagId = self.db.execute(query)
        debug.info(addTagId)
        if (addTagId==1):
            self.ui.textEdit.append("Tag Id Added Successfully")
        else:
            self.ui.textEdit.append(addTagId)



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
        self.socket.send_multipart(["READ"])

        # slNo = self.socket.recv()
        # debug.info "Received sl.No: " + slNo
        try:
            tagId = self.socket.recv_multipart()
            debug.info("Received Tag Id :" + tagId[0])
            self.tagIdReceived.emit(tagId[0])
        except:
            debug.info(str(sys.exc_info()))

        self.socket.close()

        if (self.socket.closed == True):
            debug.info("read Single Socket closed.")


class writeThread(QThread):
    waiting = pyqtSignal()
    ackReceived = pyqtSignal(str)

    def __init__(self,tagId, parent):
        super(writeThread, self).__init__(parent)
        self.tagId = tagId

    def run(self):
        self.waiting.emit()

        debug.info("connecting to rfid Scanner Server...")
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.connect("tcp://192.168.1.183:4689")
            debug.info("connected")
        except:
            debug.info(str(sys.exc_info()))
        self.socket.send_multipart(["WRITE",self.tagId])
        try:
            ack = self.socket.recv_multipart()
            debug.info(ack)
            # if (ack[0]=="ack_pass"):
            self.ackReceived.emit(ack[0])
            # else:
                # self.ackReceived.emit("ack_fail")
        except:
            debug.info(str(sys.exc_info()))

        self.socket.close()

        if (self.socket.closed == True):
            debug.info("write socket closed")




if __name__ == '__main__':
    setproctitle.setproctitle("RFID_TOOLS")
    app = QtWidgets.QApplication(sys.argv)
    window = rfidToolsWidget()
    sys.exit(app.exec_())




