#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
import subprocess
from PyQt5 import QtGui,QtWidgets,QtCore,uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt
import MySQLdb
import MySQLdb.cursors

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
# uiFilePath = os.path.join(progPath,"GUI","uiFiles")
# imgFilePath = os.path.join(progPath, "GUI","imageFiles")
databasePath = os.path.join(progPath, "GUI")
# sys.path.append(uiFilePath)
# sys.path.append(imgFilePath)
sys.path.append(databasePath)

import database
import dbGrantha
import debug

# db = database.DataBase()
db = dbGrantha.dbGrantha()

# class ImageWidget(QLabel):
#     def __init__(self, imagePath, parent=None):
#         super(ImageWidget, self).__init__(parent)
#         pic = QPixmap(imagePath)
#         # smallerPic = pic.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
#         self.setPixmap(pic)

class ImageWidget(QtWidgets.QPushButton):
  def __init__(self, imagePath, imageSize, parent=None):
    super(ImageWidget, self).__init__(parent)
    self.imagePath = imagePath
    self.picture = QtGui.QPixmap(imagePath)
    # debug.info (self.imagePath)
    self.picture  = self.picture.scaledToHeight(imageSize,0)

  def paintEvent(self, event):
    painter = QtGui.QPainter(self)
    painter.setPen(QtCore.Qt.NoPen)
    painter.drawPixmap(0, 0, self.picture)

  def sizeHint(self):
    return(self.picture.size())



def openFile():
    fileName = QFileDialog.getOpenFileName(ui, 'Open file', '/crap/crap.server/', '*.png *.jpg *.jpeg')
    debug.info (fileName)
    ui.lineEdit.clear()
    ui.lineEdit.setText(fileName[0])
    # ui.tableWidget.setCellWidget(0, 1, ImgWidget(fileName[0]))
    # pic = QPixmap(fileName[0])
    # smallerPic = pic.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
    # ui.label.setPixmap(smallerPic)

def insertImage():
    imageLoc = str(ui.lineEdit.text().strip())
    query = "INSERT INTO IMAGES (image) VALUES (\"{0}\") ".format(imageLoc)
    debug.info (query)
    addImage = db.execute(query)
    debug.info (addImage)
    if (addImage==1):
        ui.lineEdit.clear()
        ui.lineEdit.setText("Add Success")
    if (addImage==0):
        ui.lineEdit.clear()
        ui.lineEdit.setText("Add Failed")

def viewImage():
    ui.tableWidget.setRowCount(0)
    queryCol = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'IMAGES' "
    debug.info (queryCol)
    # column = db.getColumnsOfImages(queryCol)
    column = db.execute(queryCol,dictionary=True)
    theColumn = [x['COLUMN_NAME'] for x in column]
    debug.info(theColumn)
    ui.tableWidget.setColumnCount(len(theColumn))
    ui.tableWidget.setHorizontalHeaderLabels(theColumn)

    queryAll = "SELECT * FROM IMAGES"
    # theRows = db.getAllRowsOfImages(queryAll)
    theRows = db.execute(queryAll,dictionary=True)
    debug.info(theRows)
    ui.tableWidget.setRowCount(len(theRows))

    row = 0
    # db.getAllValuesOfImages(queryAll, init=True)
    while True:
        # primaryResult = db.getAllValuesOfImages(queryAll)
        if (row == len(theRows)):
            break
        primaryResult = theRows[row]
        debug.info (primaryResult)
        # if (not primaryResult):
        col = 0
        for n in theColumn:
            result = primaryResult[n]
            ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(result)))
            col += 1
        row += 1

    numRows = ui.tableWidget.rowCount()
    for row in range(numRows):
        imagePath = str(ui.tableWidget.item(row, 1).text())
        debug.info(imagePath)
        ui.tableWidget.takeItem(row, 1)
        imageThumb = ImageWidget(imagePath,32)
        imageThumb.clicked.connect(lambda x, imagePath = imagePath:imageWidgetClicked(imagePath))
        ui.tableWidget.setCellWidget(row, 1, imageThumb)

    ui.tableWidget.resizeColumnsToContents()
    ui.tableWidget.resizeRowsToContents()

# def cellClick():
#     debug.info("cell clicked")

def imageWidgetClicked(imagePath):
    image_path = str(imagePath)
    debug.info (image_path)
    debug.info("Image Clicked")

    # cmdFull = "xdg-open \"" + image_path + "\""
    cmdFull = "feh \"" + image_path + "\" -Z -."
    debug.info(cmdFull)
    subprocess.Popen(cmdFull, shell=True)



app = QApplication(sys.argv)

ui = uic.loadUi(os.path.join("imageInTable.ui"))
# ui.show()

# ui.tableWidget.setRowCount(0)
ui.browseButton.clicked.connect(openFile)
ui.addButton.clicked.connect(insertImage)
ui.viewButton.clicked.connect(viewImage)
# ui.tableWidget.itemClicked.connect(cellClick)
# fileName = QFileDialog.getOpenFileName('Open file', 'c:\\', "Image files (*.jpg *.gif)")
ui.show()


sys.exit(app.exec_())

