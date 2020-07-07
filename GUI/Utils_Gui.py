#!/usr/bin/python2
# *-* coding: utf-8 *-*

from PyQt5 import QtWidgets, QtCore, QtGui
import debug
import subprocess
import os

filePath = os.path.abspath(__file__)
# currDir = os.sep.join(filePath.split(os.sep)[:-1])
projDir = os.sep.join(filePath.split(os.sep)[:-2])
# uiFilePath = os.path.join(projDir,"GUI","uiFiles")
# imgFilePath = os.path.join(projDir, "GUI","imageFiles")


def setStyleSheet(ui,theme="light"):
    Theme = theme+".qss"
    # debug.info(Theme)
    qssFile = os.path.join(projDir, "GUI", "styleSheet", Theme)
    with open(qssFile, "r") as sS:
        ui.setStyleSheet(sS.read())

def getFileSize(fileSize):
    for count in ['Bytes', 'KB', 'MB']:
        if fileSize > -1024.0 and fileSize < 1024.0:
            size = "%3.1f%s" % (fileSize, count)
        fileSize /= 1024.0
    return str(size)

def imageWidgetClicked(path):
    """
    Open image in a image viewer
    :param self:
    :param path:
    :return:
    """
    image_path = str(path)
    debug.info(image_path)
    # debug.info("Image Clicked")
    # cmdFull = "feh \"" + image_path + "\" -Z -."
    # cmdFull = "python imageViewerGrantha.py " + image_path
    # debug.info(cmdFull)
    # subprocess.Popen(cmdFull, shell=True)
    # cmd = "python " + os.path.join(projDir, "src", "batch_rename.py") + " --path " + path + " --asset " + selectedFiles[0]
    cmd = "python " + os.path.join(projDir, "GUI", "imageViewerGrantha.py")+" --path "+ image_path
    # cmd = "xdg-open " + image_path
    debug.info(cmd)
    subprocess.Popen(cmd, shell=True)


def messageBox(msg1, msg2="", path=""):
    """
    Show informative message
    :param msg1:
    :param msg2:
    :return:
    """
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Message")
    msg.setText(msg1+"\n"+msg2)
    okBut = msg.addButton("OK", QtWidgets.QMessageBox.NoRole)
    msg.setDefaultButton(okBut)
    if path:
        msg.setIconPixmap(QtGui.QPixmap(path))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)

    # setStyleSheet(msg)
    theme = os.environ['GRANTHA_THEME']
    debug.info(theme)
    setStyleSheet(msg, theme)
    msg.exec_()

# class messageBox(QtWidgets.QMessageBox):
#     """
#     Show message box
#     :param self:
#     :param msg1:
#     :param msg2:
#     :return:
#     """
#     def __init__(self, msg1, msg2="",parent=None):
#         super(messageBox,self).__init__(parent)
#         # QtWidgets.QMessageBox.__init__(self)
#
#         # self.msg = QtWidgets.QMessageBox()
#         self.setIcon(QtWidgets.QMessageBox.Information)
#         self.setWindowTitle("Message")
#         self.setText(msg1+"\n"+msg2)
#         okBut = self.addButton("OK", QtWidgets.QMessageBox.NoRole)
#         self.setDefaultButton(okBut)
#         # self.exec_()
#
#     def close(self):
#         self.close()


class ImageWidget(QtWidgets.QPushButton):
    def __init__(self, imagePath, imageSize, parent=None):
        """
        Create an image widget
        :param imagePath:
        :param imageSize:
        :param parent:
        """
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


class TimerMessageBox(QtWidgets.QMessageBox):
    def __init__(self, timeout, msg1, msg2="", parent=None):
        """
        Show informative message and close on timeout
        :param timeout:
        :param msg1:
        :param msg2:
        :param parent:
        """
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("Message")
        self.time_to_wait = timeout
        self.setText(msg1+"\n"+msg2)
        self.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.setText("wait (closing automatically)")
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

