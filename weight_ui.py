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
        MainWindow.resize(766, 279)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 291, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 111, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 81, 41))
        self.label_3.setObjectName("label_3")
        self.label_weight_datetime = QtWidgets.QLabel(self.groupBox)
        self.label_weight_datetime.setGeometry(QtCore.QRect(120, 40, 161, 31))
        self.label_weight_datetime.setObjectName("label_weight_datetime")
        self.label_weight_value = QtWidgets.QLabel(self.groupBox)
        self.label_weight_value.setGeometry(QtCore.QRect(120, 80, 161, 21))
        self.label_weight_value.setObjectName("label_weight_value")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 291, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 81, 41))
        self.label_6.setObjectName("label_6")
        self.label_rfid_value = QtWidgets.QLabel(self.groupBox_2)
        self.label_rfid_value.setGeometry(QtCore.QRect(60, 40, 221, 21))
        self.label_rfid_value.setObjectName("label_rfid_value")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(20, 70, 121, 41))
        self.label_7.setObjectName("label_7")
        self.label_rfid_value_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_rfid_value_2.setGeometry(QtCore.QRect(140, 80, 161, 21))
        self.label_rfid_value_2.setText("")
        self.label_rfid_value_2.setObjectName("label_rfid_value_2")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(310, 20, 441, 231))
        self.tableView.setObjectName("tableView")
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
        self.label_2.setText(_translate("MainWindow", "Datetime:"))
        self.label_3.setText(_translate("MainWindow", "Value:"))
        self.label_weight_datetime.setText(_translate("MainWindow", "Waiting"))
        self.label_weight_value.setText(_translate("MainWindow", "Waiting"))
        self.groupBox_2.setTitle(_translate("MainWindow", "RFID"))
        self.label_6.setText(_translate("MainWindow", "UID:"))
        self.label_rfid_value.setText(_translate("MainWindow", "Waiting"))
        self.label_7.setText(_translate("MainWindow", "CountTime:"))


