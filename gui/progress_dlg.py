# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDlg(object):
    def setupUi(self, ProgressDlg):
        ProgressDlg.setObjectName("ProgressDlg")
        ProgressDlg.resize(670, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressDlg.sizePolicy().hasHeightForWidth())
        ProgressDlg.setSizePolicy(sizePolicy)
        ProgressDlg.setMinimumSize(QtCore.QSize(670, 250))
        ProgressDlg.setMaximumSize(QtCore.QSize(670, 250))
        ProgressDlg.setSizeGripEnabled(False)
        ProgressDlg.setModal(True)
        self.progBtnBx = QtWidgets.QDialogButtonBox(ProgressDlg)
        self.progBtnBx.setGeometry(QtCore.QRect(530, 210, 121, 32))
        self.progBtnBx.setAutoFillBackground(False)
        self.progBtnBx.setStyleSheet("text-color: rgb(255, 0, 0)")
        self.progBtnBx.setOrientation(QtCore.Qt.Horizontal)
        self.progBtnBx.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.progBtnBx.setObjectName("progBtnBx")
        self.groupBox = QtWidgets.QGroupBox(ProgressDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 651, 181))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.calDescrLbl = QtWidgets.QLabel(self.groupBox)
        self.calDescrLbl.setGeometry(QtCore.QRect(20, 50, 551, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.calDescrLbl.setFont(font)
        self.calDescrLbl.setStyleSheet("line-height: 150%")
        self.calDescrLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl.setObjectName("calDescrLbl")
        self.maxLbl = QtWidgets.QLabel(self.groupBox)
        self.maxLbl.setGeometry(QtCore.QRect(528, 137, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.maxLbl.setFont(font)
        self.maxLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxLbl.setObjectName("maxLbl")
        self.progPB = QtWidgets.QProgressBar(self.groupBox)
        self.progPB.setGeometry(QtCore.QRect(20, 120, 611, 23))
        self.progPB.setProperty("value", 24)
        self.progPB.setObjectName("progPB")
        self.minLbl = QtWidgets.QLabel(self.groupBox)
        self.minLbl.setGeometry(QtCore.QRect(20, 138, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.minLbl.setFont(font)
        self.minLbl.setObjectName("minLbl")

        self.retranslateUi(ProgressDlg)
        self.progBtnBx.accepted.connect(ProgressDlg.accept)
        self.progBtnBx.rejected.connect(ProgressDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(ProgressDlg)

    def retranslateUi(self, ProgressDlg):
        _translate = QtCore.QCoreApplication.translate
        ProgressDlg.setWindowTitle(_translate("ProgressDlg", "Calibration In Progress"))
        self.groupBox.setTitle(_translate("ProgressDlg", "Calibration running..."))
        self.calDescrLbl.setText(_translate("ProgressDlg", "Line 1\n"
"Line 2"))
        self.maxLbl.setText(_translate("ProgressDlg", "TextLabel"))
        self.minLbl.setText(_translate("ProgressDlg", "TextLabel"))
