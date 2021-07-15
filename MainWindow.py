# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

fileName = ''
rotation_angle = ''


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 871)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setWindowTitle("label show image")
        self.setWindowIcon(QIcon('1.jpg'))

        self.label = QLabel(self)
        self.label.setText("   show original image")
        self.label.setFixedSize(300, 400)
        self.label.move(200, 30)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                 )

        self.label2 = QLabel(self)
        self.label2.setText("   show image after filtering")
        self.label2.setFixedSize(300, 400)
        self.label2.move(550, 30)

        self.label2.setStyleSheet("QLabel{background:white;}"
                                  "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                  )


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 30, 120, 60))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.openimage)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 140, 120, 60))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.getRotationAngle)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 260, 120, 60))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 380, 120, 60))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 490, 121, 60))
        self.pushButton_5.setObjectName("pushButton_5")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Open image"))
        self.pushButton_2.setText(_translate("MainWindow", "Rotation"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))


    def openRotationWindow(self):
        import RotationWindow2
        self.rotationWindow = RotationWindow2.Ui_MainWindow()

    def getRotationAngle(self):
        global rotation_angle
        global fileName
        img_before_rotation = cv2.imread(fileName)
        rotation_angle_input, ok = QInputDialog.getText(self, "yes", "No",
                                                        QtWidgets.QLineEdit.Normal)

        if ok:
            rotation_angle = rotation_angle_input
            self.rotation()

    def rotation(self):
        global fileName
        global rotation_angle

        print(rotation_angle)

        rotation_angle = int (rotation_angle)

        img_before_rotation = cv2.imread(fileName)
        h, w = img_before_rotation.shape[:2]

        M = cv2.getRotationMatrix2D((w / 2, h / 2), rotation_angle, 1)  # 旋转  通过getRotationMatrix2D得到图像旋转后的矩阵

        dst = cv2.warpAffine(img_before_rotation, M, (w, h))  # 通过仿射变换函数warpAffine将矩阵转化为图像
        size = (int(self.label2.width()), int(self.label2.height()))  # 获得控件lable的尺寸
        shrink = cv2.resize(dst, size, interpolation=cv2.INTER_AREA)  # 对图像进行缩放
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
        self.QtImg = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  QtGui.QImage.Format_RGB888)
        self.label2.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))

    def openimage(self):
        global fileName
        QMessageBox.question(self, '提醒', '选择图片时要是绝对路径(且全英文路径)',
                             QMessageBox.Ok)
        imgName, imgType = QFileDialog.getOpenFileName(self, "image.jpg", os.getcwd())
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(QPixmap(jpg))
        self.label2.setPixmap(QPixmap(jpg))
        fileName = imgName
        originalImage = cv2.imread(imgName)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())