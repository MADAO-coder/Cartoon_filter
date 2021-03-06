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

import null as null
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

fileName = ''
resultImage = np.zeros((100,100,3), dtype=np.uint8)
global pt1, pt2

# Class for GUI
class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 871)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.setWindowTitle("label show image")
        self.setWindowIcon(QIcon('1.jpg'))

        # Set up the label for image1, default width is 300, height is 400
        self.label = QLabel(self)
        self.label.setText("   show original image")
        self.label.setFixedSize(300, 400)
        self.label.move(200, 30)
        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                 )

        # Set up the label for image2, default width is 300, height is 400
        self.label2 = QLabel(self)
        self.label2.setText("   show image after filtering")
        self.label2.setFixedSize(300, 400)
        self.label2.move(550, 30)
        self.label2.setStyleSheet("QLabel{background:white;}"
                                  "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                  )


        # Set up button1 for open images
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 30, 120, 60))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openimage)

        # Set up button2 for rotate images
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 140, 120, 60))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.getRotationAngle)

        # Set up button3 for scaling images
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 260, 120, 60))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.getScalingInput)

        # Set up button4 for implementing cartoon filter
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 380, 120, 60))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.image_crop)

        # Set up button for saving the output image
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 490, 120, 60))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.cartoon_filter)


        self.pushButton_cropLeft = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cropLeft.setGeometry(QtCore.QRect(200, 720, 120, 60))
        self.pushButton_cropLeft.setObjectName("Save image")
        self.pushButton_cropLeft.clicked.connect(self.saveImage)


        # Initialize the main window for GUI
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

    # Function to name the buttons
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Open image"))
        self.pushButton_2.setText(_translate("MainWindow", "Rotation"))
        self.pushButton_3.setText(_translate("MainWindow", "Scaling"))
        self.pushButton_4.setText(_translate("MainWindow", "Image crop"))
        self.pushButton_5.setText(_translate("MainWindow", "Cartoon filter"))
        self.pushButton_cropLeft.setText(_translate("MainWindow", "Save image"))


    # Function get the input of rotation angle
    def getRotationAngle(self):
        global fileName

        # Read the original image by reading fileName
        img_before_rotation = self.get_original_image()

        # If users click ok, perform rotation based on their input angle
        if img_before_rotation is not None:
            # Create a input box and user can choose their input angle
            rotation_angle_input, ok = QInputDialog.getInt(self, "Rotation",
                                                           "Please input angle you want to rotate (such as 30)",
                                                           QtWidgets.QLineEdit.Normal)
            if ok:
                self.rotation(img_before_rotation, rotation_angle_input)
        else:
            self.wrong_msg_box("Empty image", "Please upload image first!")

    # Function to perform rotation
    def rotation(self, img_before_rotation, rotation_angle):

        global resultImage

        # change the rotation_angle from input to string
        rotation_angle = int (rotation_angle)

        # if the input angle between 0 to 360, perform rotation
        if rotation_angle > 0 and rotation_angle<360:


            h, w = img_before_rotation.shape[:2] # Find height and width of the original image
            M = cv2.getRotationMatrix2D((w / 2, h / 2), rotation_angle, 1) # Find the center position of original image
            dst = cv2.warpAffine(img_before_rotation, M, (w, h)) # Use wrapAffine function achieve image after rotation

            # Reset the label2's size to make it to default
            self.reset_label2_size()
            # Set the output image at label2
            self.set_img_to_label(dst, "label2")
        else:
            self.wrong_msg_box("invalid input", "Please input number between 1-359")

    # Function to open the local image
    def openimage(self):
        global fileName
        QMessageBox.question(self, 'Remind', 'Please choose one image from your computer',
                             QMessageBox.Ok)
        # Get the image's name and image's type
        imgName, imgType = QFileDialog.getOpenFileName(self, "image.jpg", os.getcwd())

        # Read the original image based on file location
        originalImage = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())

        # Set up original image at label1 and label2 as begin
        self.label.setPixmap(QPixmap(originalImage))
        self.label2.setPixmap(QPixmap(originalImage))
        fileName = imgName

    # Function to implement scaling to original image
    def getScalingInput(self):

        img_before_scaling = self.get_original_image()
        print(img_before_scaling)
        if img_before_scaling is not None:

            # Retrieve users' input (support scale from 0.2 times to 2.0 times of original image)
            scaling_size_input, ok = QInputDialog.getItem(self, "Scaling",
                                                          "Please input scaling multiples you want (2 is double image)",
                                                          ("0.2", "0.4", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0")
                                                          , 0, False)

            # Once users click ok, image will be scaled based on users input, for example 2 means double the image
            if ok:
                # Get the original image

                # Use resize function to make the original image fill the label size
                img_before_scaling = cv2.resize(img_before_scaling, (300, 400), interpolation=cv2.INTER_CUBIC)
                # Convert image to RGB
                img_before_scaling = cv2.cvtColor(img_before_scaling, cv2.COLOR_BGR2RGB)

                # Covert the user's input from string to float
                scaling_size_input = float(scaling_size_input)

                # resize the image based on user's input
                dst_scaling = cv2.resize(img_before_scaling, None, fx= scaling_size_input, fy= scaling_size_input, interpolation=cv2.INTER_CUBIC)
                self.set_img_to_label(dst_scaling, "scaling")
        else:
            self.wrong_msg_box("Empty image", "Please upload image first!")

    # Function to retrieve the original image based on file name
    def get_original_image(self):
        global fileName
        return cv2.imread(fileName, 1) # Return original image

    # Function to make the label2's size reset to default
    def reset_label2_size(self):
        self.label2.setFixedSize(300, 400)

    # Function to implement cartoon filter
    def cartoon_filter(self):
        global resultImage
        global fileName
        img = cv2.imread(fileName)

        if img is not None :
            data = np.float32(img).reshape((-1, 3))

            # Determine criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

            # Implementing K-Means
            ret, label, center = cv2.kmeans(data, 9, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            result = result.reshape(img.shape)

            blurred = cv2.bilateralFilter(result, d=7,
                                          sigmaColor=200, sigmaSpace=200)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray, 7)
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7,
                                          7)

            cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

            t1,dst1 = cv2.threshold(cartoon, 127, 255, cv2.THRESH_BINARY)
            self.set_img_to_label(dst1, "label2")
        else:
            self.wrong_msg_box("Empty image", "Please upload image first!")

    # Function to set images to its labels
    def set_img_to_label(self, inputImg, labelName):

        # Get the size of label2
        size = (int(self.label2.width()), int(self.label2.height()))

        # resize the image to make it same as the label size
        shrink = cv2.resize(inputImg, size, interpolation=cv2.INTER_AREA)
        # Change image to RGB
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)

        # Switch cv2 image to QtImg, which can be showing in GUI
        self.QtImg = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  QtGui.QImage.Format_RGB888)
        # Show image on label2
        if labelName is "label2":
            self.label2.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))
        # Show image on label1
        if labelName is "label1":
            self.label.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))
        # Show image if perform scaling, since scaling will change the size of label
        if labelName is "scaling":
            self.QtImg = QtGui.QImage(inputImg.data,
                                      inputImg.shape[1],
                                      inputImg.shape[0],
                                      QtGui.QImage.Format_RGB888)
            # Get the width and height of image
            width = inputImg.shape[1]
            height = inputImg.shape[0]

            # reset the size of label2
            self.label2.setFixedSize(width, height)
            # show the image at label2
            self.label2.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))

    def switchImage(self):
        global resultImage
        global fileName

        originalImage = cv2.imread(fileName, 1)
        print(originalImage)

        self.QtImg = QtGui.QImage(resultImage.data,
                                  resultImage.shape[1],
                                  resultImage.shape[0],
                                  QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))

    # Function to save the output image at local
    def saveImage(self):

        # Once user choose the dir path, save it
        self.dir_path = QFileDialog.getExistingDirectory(None, "Choose path", os.getcwd())

        # Save the output image based on the path that user choosed
        cv2.imwrite(os.path.join(self.dir_path, 'result.jpg'), resultImage)


    def on_mouse(self, event, x, y, flags, param):
        global pt1, pt2, resultImage
        img2 = self.get_original_image()
        if event == cv2.EVENT_LBUTTONDOWN:
            pt1 = (x, y)
            cv2.circle(img2, pt1, 10, (0, 255, 0), 5)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(img2, pt1, (x, y), (255, 0, 0), 5)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_LBUTTONUP:
            pt2 = (x, y)
            cv2.rectangle(img2, pt1, pt2, (0, 0, 255), 5)
            cv2.imshow('image', img2)
            min_x = min(pt1[0], pt2[0])
            min_y = min(pt1[1], pt2[1])
            width = abs(pt1[0] - pt2[0])
            height = abs(pt1[1] - pt2[1])
            cut_img = self.get_original_image()[min_y:min_y + height, min_x:min_x + width]
            resultImage = cut_img
            self.saveImage()

    def image_crop(self):

        originalImage = self.get_original_image()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.on_mouse)
        cv2.imshow('image', originalImage)
        cv2.waitKey(0)

    def empty_image(self):
        if self.get_original_image() is null:
            return True
    def wrong_msg_box(self, title, body):
        QMessageBox.information(self, title, body, QMessageBox.Ok)



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

