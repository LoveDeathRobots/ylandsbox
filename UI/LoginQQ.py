# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginQQ.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_QQLogin(object):
    def setupUi(self, Dialog_QQLogin):
        Dialog_QQLogin.setObjectName("Dialog_QQLogin")
        Dialog_QQLogin.resize(1600, 600)
        Dialog_QQLogin.setMinimumSize(QtCore.QSize(1600, 600))
        Dialog_QQLogin.setBaseSize(QtCore.QSize(1600, 600))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_QQLogin)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_QQLogin)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setSizeIncrement(QtCore.QSize(0, 30))
        self.label.setBaseSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog_QQLogin)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.browser = QtWidgets.QVBoxLayout()
        self.browser.setObjectName("browser")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.browser.addItem(spacerItem)
        self.verticalLayout.addLayout(self.browser)

        self.retranslateUi(Dialog_QQLogin)
        QtCore.QMetaObject.connectSlotsByName(Dialog_QQLogin)

    def retranslateUi(self, Dialog_QQLogin):
        _translate = QtCore.QCoreApplication.translate
        Dialog_QQLogin.setWindowTitle(_translate("Dialog_QQLogin", "Dialog"))
        self.label.setText(_translate("Dialog_QQLogin", "为什么要登录艾兰岛创意工坊？ 艾兰岛的个人存档目录名是QQ对应的RailID。由于WeGame没有对个人开发第三方登录接口。因此，只能通过先登录艾兰岛创意工坊后，从Cookie中获取对应的RailID；"))


