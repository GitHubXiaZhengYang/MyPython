# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from install import wenjian_daxiao, pan_name, pan_daxiao, true_no

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    global wenjian_daxiao, pan_name, pan_daxiao, true_no
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(400, 400)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.liulanPath = QtWidgets.QPushButton(self.centralwidget)
        self.liulanPath.setGeometry(QtCore.QRect(280, 10, 100, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.liulanPath.setFont(font)
        self.liulanPath.setObjectName("liulanPath")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 10, 250, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.OK = QtWidgets.QPushButton(self.centralwidget)
        self.OK.setGeometry(QtCore.QRect(320, 320, 75, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.OK.setFont(font)
        self.OK.setObjectName("OK")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 110, 360, 200))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.listView.setFont(font)
        self.listView.setObjectName("listView")
        self.install = QtWidgets.QPushButton(self.centralwidget)
        self.install.setGeometry(QtCore.QRect(20, 80, 360, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.install.setFont(font)
        self.install.setObjectName("install")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 50, 361, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        global wenjian_daxiao, pan_name, pan_daxiao, true_no
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "软件安装程序"))
        self.liulanPath.setText(_translate("MainWindow", "浏览"))
        self.lineEdit.setText(_translate("MainWindow", "输入安装目录"))
        self.OK.setText(_translate("MainWindow", "OK"))
        self.install.setText(_translate("MainWindow", "开始安装"))
        self.label.setText(_translate("MainWindow", f"应用所需{wenjian_daxiao},{pan_name}盘剩余{pan_daxiao},{true_no}"))
