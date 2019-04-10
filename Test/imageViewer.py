#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys
import subprocess
import argparse
from PyQt5 import QtGui,QtWidgets,QtCore,uic, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])

databasePath = os.path.join(progPath, "GUI")
sys.path.append(databasePath)
import debug


def resizeEvent(event):
    # ui.label.setScaledContents(True)
    x = ui.label.size()
    h = x.height()
    w = x.width()
    # debug.info(h)
    # debug.info(w)
    pix = ui.label.pixmap()
    ui.label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation))
    # ui.label.setScaledContents(False)


    debug.info(x)
    event.accept()

app = QApplication(sys.argv)

ui = uic.loadUi(os.path.join("imageViewer.ui"))

# class ImageWidget(QLabel):
#     def __init__(self, imagePath, parent=None):
#         super(ImageWidget, self).__init__(parent)
#         pic = QIcon(imagePath)
#         # smallerPic = pic.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
#         self.setIcon(pic)
parser = argparse.ArgumentParser(description="Utility to view images")
parser.add_argument('path', metavar='N', type=str, help='Path to image file')
args = parser.parse_args()

# # ui.label.setScaledContents(True)
# ui.label.resizeEvent = resizeEvent
# # x = ui.label.sizeHint()
# # debug.info(x)
# pic = QPixmap(args.path)
# # pic  = pic.scaledToHeight(512,996)
#
# # pic = pic.scaled(1024, 992, Qt.KeepAspectRatio, Qt.FastTransformation)
# ui.label.setPixmap(pic)

# ui.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(args.path))
ui.webEngineView.setUrl(QtCore.QUrl("file:///home/sanath.shetty/PycharmProjects/Grantha/Test/Simple-Image-Viewer-jQuery/index.html"))
# ui.webEngineView.setZoomFactor(1)

ui.setWindowTitle('Image Viewer')
ui.show()


sys.exit(app.exec_())

