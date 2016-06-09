#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################

"""GUI Python code auto-generated from Qt Creator *.ui files by PyQt pyuic utility."""
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDlg(object):
    def setupUi(self, ProgressDlg):
        ProgressDlg.setObjectName("ProgressDlg")
        ProgressDlg.resize(670, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressDlg.sizePolicy().hasHeightForWidth())
        ProgressDlg.setSizePolicy(sizePolicy)
        ProgressDlg.setMinimumSize(QtCore.QSize(670, 250))
        ProgressDlg.setMaximumSize(QtCore.QSize(670, 400))
        ProgressDlg.setSizeGripEnabled(False)
        ProgressDlg.setModal(True)
        self.groupBox = QtWidgets.QGroupBox(ProgressDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 651, 341))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.calDescrLbl = QtWidgets.QLabel(self.groupBox)
        self.calDescrLbl.setGeometry(QtCore.QRect(20, 50, 611, 121))
        font = QtGui.QFont()
        font.setFamily("PT Mono")
        font.setBold(True)
        font.setWeight(75)
        self.calDescrLbl.setFont(font)
        self.calDescrLbl.setStyleSheet("line-height: 150%")
        self.calDescrLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl.setObjectName("calDescrLbl")
        self.maxLbl = QtWidgets.QLabel(self.groupBox)
        self.maxLbl.setGeometry(QtCore.QRect(468, 287, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.maxLbl.setFont(font)
        self.maxLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxLbl.setObjectName("maxLbl")
        self.progPB = QtWidgets.QProgressBar(self.groupBox)
        self.progPB.setGeometry(QtCore.QRect(20, 270, 611, 23))
        self.progPB.setProperty("value", 24)
        self.progPB.setObjectName("progPB")
        self.minLbl = QtWidgets.QLabel(self.groupBox)
        self.minLbl.setGeometry(QtCore.QRect(20, 288, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.minLbl.setFont(font)
        self.minLbl.setObjectName("minLbl")
        self.valLbl = QtWidgets.QLabel(self.groupBox)
        self.valLbl.setGeometry(QtCore.QRect(290, 289, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.valLbl.setFont(font)
        self.valLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.valLbl.setObjectName("valLbl")
        self.calWarningLbl = QtWidgets.QLabel(self.groupBox)
        self.calWarningLbl.setGeometry(QtCore.QRect(20, 190, 611, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.calWarningLbl.setFont(font)
        self.calWarningLbl.setStyleSheet("color: red;\n"
"line-height: 150%")
        self.calWarningLbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.calWarningLbl.setWordWrap(True)
        self.calWarningLbl.setObjectName("calWarningLbl")
        self.cancelBtn = QtWidgets.QPushButton(ProgressDlg)
        self.cancelBtn.setGeometry(QtCore.QRect(550, 360, 115, 32))
        self.cancelBtn.setObjectName("cancelBtn")

        self.retranslateUi(ProgressDlg)
        QtCore.QMetaObject.connectSlotsByName(ProgressDlg)

    def retranslateUi(self, ProgressDlg):
        _translate = QtCore.QCoreApplication.translate
        ProgressDlg.setWindowTitle(_translate("ProgressDlg", "Calibration In Progress"))
        self.groupBox.setTitle(_translate("ProgressDlg", "Calibration running..."))
        self.calDescrLbl.setText(_translate("ProgressDlg", "Line 1\n"
"Line 2"))
        self.maxLbl.setText(_translate("ProgressDlg", "TextLabel"))
        self.minLbl.setText(_translate("ProgressDlg", "TextLabel"))
        self.valLbl.setText(_translate("ProgressDlg", "TextLabel"))
        self.calWarningLbl.setText(_translate("ProgressDlg", "text goes here..."))
        self.cancelBtn.setText(_translate("ProgressDlg", "Cancel"))

