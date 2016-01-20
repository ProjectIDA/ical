# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'run_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RunDlg(object):
    def setupUi(self, RunDlg):
        RunDlg.setObjectName("RunDlg")
        RunDlg.resize(666, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RunDlg.sizePolicy().hasHeightForWidth())
        RunDlg.setSizePolicy(sizePolicy)
        RunDlg.setMinimumSize(QtCore.QSize(666, 250))
        RunDlg.setMaximumSize(QtCore.QSize(666, 250))
        self.buttonBox = QtWidgets.QDialogButtonBox(RunDlg)
        self.buttonBox.setGeometry(QtCore.QRect(300, 209, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.cmdlineBtn = QtWidgets.QPushButton(RunDlg)
        self.cmdlineBtn.setGeometry(QtCore.QRect(20, 210, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cmdlineBtn.setFont(font)
        self.cmdlineBtn.setObjectName("cmdlineBtn")
        self.groupBox = QtWidgets.QGroupBox(RunDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 641, 181))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.confirmTextLbl = QtWidgets.QLabel(self.groupBox)
        self.confirmTextLbl.setGeometry(QtCore.QRect(30, 40, 551, 91))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.confirmTextLbl.setFont(font)
        self.confirmTextLbl.setStyleSheet("line-height: 150%")
        self.confirmTextLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.confirmTextLbl.setObjectName("confirmTextLbl")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(RunDlg)
        self.buttonBox.accepted.connect(RunDlg.accept)
        self.buttonBox.rejected.connect(RunDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(RunDlg)

    def retranslateUi(self, RunDlg):
        _translate = QtCore.QCoreApplication.translate
        RunDlg.setWindowTitle(_translate("RunDlg", "Run Calibration"))
        self.cmdlineBtn.setText(_translate("RunDlg", "View Cmdline..."))
        self.groupBox.setTitle(_translate("RunDlg", "Confirm Calibration Parameters"))
        self.confirmTextLbl.setText(_translate("RunDlg", "Line 1\n"
"Line 2"))
        self.label_2.setText(_translate("RunDlg", "Begin Calibration?"))

