# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\weight.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(301, 246)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 281, 211))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.groupBox.setFont(font)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 261, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 81, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 111, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 81, 41))
        self.label_3.setObjectName("label_3")
        self.input_weight_ip_address = QtWidgets.QLineEdit(self.groupBox)
        self.input_weight_ip_address.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.input_weight_ip_address.setObjectName("input_weight_ip_address")
        self.label_weight_datetime = QtWidgets.QLabel(self.groupBox)
        self.label_weight_datetime.setGeometry(QtCore.QRect(110, 90, 161, 21))
        self.label_weight_datetime.setObjectName("label_weight_datetime")
        self.label_weight_value = QtWidgets.QLabel(self.groupBox)
        self.label_weight_value.setGeometry(QtCore.QRect(110, 120, 161, 21))
        self.label_weight_value.setObjectName("label_weight_value")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "秤重儀"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.label_2.setText(_translate("MainWindow", "Datetime:"))
        self.label_3.setText(_translate("MainWindow", "Value:"))
        self.input_weight_ip_address.setText(_translate("MainWindow", "192.168.1.100:5000"))
        self.label_weight_datetime.setText(_translate("MainWindow", "Unconnect"))
        self.label_weight_value.setText(_translate("MainWindow", "Unconnect"))


