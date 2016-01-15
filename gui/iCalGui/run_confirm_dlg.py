# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'run_confirm_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RunDlg(object):
    def setupUi(self, RunDlg):
        RunDlg.setObjectName("RunDlg")
        RunDlg.resize(663, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(RunDlg)
        self.buttonBox.setGeometry(QtCore.QRect(300, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.cmdlineLE = QtWidgets.QLineEdit(RunDlg)
        self.cmdlineLE.setGeometry(QtCore.QRect(30, 30, 611, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.cmdlineLE.setFont(font)
        self.cmdlineLE.setObjectName("cmdlineLE")
        self.label = QtWidgets.QLabel(RunDlg)
        self.label.setGeometry(QtCore.QRect(30, 10, 171, 16))
        self.label.setObjectName("label")

        self.retranslateUi(RunDlg)
        self.buttonBox.accepted.connect(RunDlg.accept)
        self.buttonBox.rejected.connect(RunDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(RunDlg)

    def retranslateUi(self, RunDlg):
        _translate = QtCore.QCoreApplication.translate
        RunDlg.setWindowTitle(_translate("RunDlg", "Dialog"))
        self.label.setText(_translate("RunDlg", "QCAL Command line:"))

