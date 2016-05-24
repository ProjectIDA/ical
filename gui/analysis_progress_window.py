# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analysis_progress_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnalysisProgressFrm(object):
    def setupUi(self, AnalysisProgressFrm):
        AnalysisProgressFrm.setObjectName("AnalysisProgressFrm")
        AnalysisProgressFrm.resize(312, 130)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AnalysisProgressFrm.sizePolicy().hasHeightForWidth())
        AnalysisProgressFrm.setSizePolicy(sizePolicy)
        AnalysisProgressFrm.setMinimumSize(QtCore.QSize(312, 130))
        AnalysisProgressFrm.setMaximumSize(QtCore.QSize(312, 130))
        self.progPB = QtWidgets.QProgressBar(AnalysisProgressFrm)
        self.progPB.setGeometry(QtCore.QRect(20, 60, 272, 23))
        self.progPB.setMaximum(0)
        self.progPB.setProperty("value", -1)
        self.progPB.setObjectName("progPB")
        self.calDescrLbl = QtWidgets.QLabel(AnalysisProgressFrm)
        self.calDescrLbl.setGeometry(QtCore.QRect(20, 10, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.calDescrLbl.setFont(font)
        self.calDescrLbl.setStyleSheet("line-height: 150%")
        self.calDescrLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl.setObjectName("calDescrLbl")
        self.calDescrLbl_2 = QtWidgets.QLabel(AnalysisProgressFrm)
        self.calDescrLbl_2.setGeometry(QtCore.QRect(21, 40, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setBold(False)
        font.setWeight(50)
        self.calDescrLbl_2.setFont(font)
        self.calDescrLbl_2.setStyleSheet("line-height: 150%")
        self.calDescrLbl_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl_2.setObjectName("calDescrLbl_2")
        self.cancelBtn = QtWidgets.QPushButton(AnalysisProgressFrm)
        self.cancelBtn.setGeometry(QtCore.QRect(182, 90, 115, 32))
        self.cancelBtn.setObjectName("cancelBtn")

        self.retranslateUi(AnalysisProgressFrm)
        QtCore.QMetaObject.connectSlotsByName(AnalysisProgressFrm)

    def retranslateUi(self, AnalysisProgressFrm):
        _translate = QtCore.QCoreApplication.translate
        AnalysisProgressFrm.setWindowTitle(_translate("AnalysisProgressFrm", "Form"))
        self.calDescrLbl.setText(_translate("AnalysisProgressFrm", "Analyzing calibration data..."))
        self.calDescrLbl_2.setText(_translate("AnalysisProgressFrm", "This will take several minutes."))
        self.cancelBtn.setText(_translate("AnalysisProgressFrm", "Cancel"))

