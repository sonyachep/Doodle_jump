# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\pythonProject\design/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(272, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setMinimumSize(QtCore.QSize(0, 60))
        self.exit_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.exit_btn.setFont(font)
        self.exit_btn.setObjectName("exit_btn")
        self.gridLayout.addWidget(self.exit_btn, 4, 0, 1, 1)
        self.rating_btn = QtWidgets.QPushButton(self.centralwidget)
        self.rating_btn.setMinimumSize(QtCore.QSize(0, 60))
        self.rating_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.rating_btn.setFont(font)
        self.rating_btn.setObjectName("rating_btn")
        self.gridLayout.addWidget(self.rating_btn, 3, 0, 1, 1)
        self.play_btn = QtWidgets.QPushButton(self.centralwidget)
        self.play_btn.setMinimumSize(QtCore.QSize(0, 60))
        self.play_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.play_btn.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.play_btn.setFont(font)
        self.play_btn.setObjectName("play_btn")
        self.gridLayout.addWidget(self.play_btn, 1, 0, 1, 1)
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setMinimumSize(QtCore.QSize(0, 60))
        self.settings_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.settings_btn.setFont(font)
        self.settings_btn.setObjectName("settings_btn")
        self.gridLayout.addWidget(self.settings_btn, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SnakeGame"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))
        self.rating_btn.setText(_translate("MainWindow", "Rating"))
        self.play_btn.setText(_translate("MainWindow", "Play"))
        self.settings_btn.setText(_translate("MainWindow", "Settings"))
