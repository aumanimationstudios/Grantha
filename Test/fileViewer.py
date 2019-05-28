#!/usr/bin/python2
# *-* coding: utf-8 *-*

# import os
# import sys
# import subprocess
# from PyQt5 import QtGui,QtWidgets,QtCore,uic
# from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton, QFileSystemModel
# from PyQt5.QtGui import QIcon,QPixmap
# from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt, QDir
# import MySQLdb
# import MySQLdb.cursors
# import dbGrantha
# import debug
#
# filePath = os.path.abspath(__file__)
# progPath = os.sep.join(filePath.split(os.sep)[:-2])
# uiFilePath = os.path.join(progPath,"GUI","uiFiles")
# imgFilePath = os.path.join(progPath, "GUI","imageFiles")
#
# sys.path.append(uiFilePath)
# sys.path.append(imgFilePath)
#
# # db = dbGrantha.dbGrantha()
#
#
# def onClicked(dirModel, fileModel):
#     # index = (dirModel.index(path))
#     # debug.info(index)
#     path = dirModel.fileInfo(index).absoluteFilePath()
#     ui.listView.setRootIndex(fileModel.setRootPath(path))
#
#
# app = QApplication(sys.argv)
#
# ui = uic.loadUi(os.path.join(uiFilePath, "fileViewer.ui"))
#
# path = QDir.rootPath()
#
# dirModel = QFileSystemModel()
# dirModel.setRootPath(QDir.rootPath())
# dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
#
# fileModel = QFileSystemModel()
# fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)
#
# ui.treeView.setModel(dirModel)
# ui.listView.setModel(fileModel)
#
# ui.treeView.setRootIndex(dirModel.index(path))
# # index = (dirModel.index(path))
# # debug.info(index)
# # path = dirModel.fileInfo(index).absoluteFilePath()
# # debug.info(path)
# ui.listView.setRootIndex(fileModel.index(path))
#
# index = ui.treeView.selectedIndexes()
# debug.info(index)
#
# # ui.treeView.clicked.connect(onClicked(dirModel,fileModel))
#
#
# ui.show()
#
# sys.exit(app.exec_())




import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        hlay = QHBoxLayout(self)
        self.treeview = QTreeView()
        # self.listview = QListView()
        hlay.addWidget(self.treeview)
        # hlay.addWidget(self.listview)

        # path = QDir.rootPath()
        rootDir = "/crap/crap.server/Sanath_Shetty/piCameraCaptures/"
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(rootDir)
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        # self.fileModel = QFileSystemModel()
        # self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)

        self.treeview.setModel(self.dirModel)
        # self.listview.setModel(self.fileModel)

        self.treeview.setRootIndex(self.dirModel.index(rootDir))
        # self.listview.setRootIndex(self.fileModel.index(rootDir))

        # self.treeview.clicked.connect(self.onClicked)

    # def on_clicked(self, index):
    #     path = self.dirModel.fileInfo(index).absoluteFilePath()
    #     self.listview.setRootIndex(self.fileModel.setRootPath(path))
    # def onClicked(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
