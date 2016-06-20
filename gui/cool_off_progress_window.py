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

# Form implementation generated from reading ui file 'cool_off_progress_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CoolOffFrm(object):
    def setupUi(self, CoolOffFrm):
        CoolOffFrm.setObjectName("CoolOffFrm")
        CoolOffFrm.resize(312, 130)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CoolOffFrm.sizePolicy().hasHeightForWidth())
        CoolOffFrm.setSizePolicy(sizePolicy)
        CoolOffFrm.setMinimumSize(QtCore.QSize(312, 130))
        CoolOffFrm.setMaximumSize(QtCore.QSize(312, 130))
        self.progPB = QtWidgets.QProgressBar(CoolOffFrm)
        self.progPB.setGeometry(QtCore.QRect(20, 60, 272, 23))
        self.progPB.setMaximum(0)
        self.progPB.setProperty("value", -1)
        self.progPB.setObjectName("progPB")
        self.infoLbl = QtWidgets.QLabel(CoolOffFrm)
        self.infoLbl.setGeometry(QtCore.QRect(20, 10, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.infoLbl.setFont(font)
        self.infoLbl.setStyleSheet("line-height: 150%")
        self.infoLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.infoLbl.setObjectName("infoLbl")
        self.calDescrLbl_2 = QtWidgets.QLabel(CoolOffFrm)
        self.calDescrLbl_2.setGeometry(QtCore.QRect(21, 40, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setBold(False)
        font.setWeight(50)
        self.calDescrLbl_2.setFont(font)
        self.calDescrLbl_2.setStyleSheet("line-height: 150%")
        self.calDescrLbl_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl_2.setObjectName("calDescrLbl_2")
        self.cancelBtn = QtWidgets.QPushButton(CoolOffFrm)
        self.cancelBtn.setGeometry(QtCore.QRect(182, 90, 115, 32))
        self.cancelBtn.setObjectName("cancelBtn")

        self.retranslateUi(CoolOffFrm)
        QtCore.QMetaObject.connectSlotsByName(CoolOffFrm)

    def retranslateUi(self, CoolOffFrm):
        _translate = QtCore.QCoreApplication.translate
        CoolOffFrm.setWindowTitle(_translate("CoolOffFrm", "Form"))
        self.infoLbl.setText(_translate("CoolOffFrm", "Preparing for HF calibration stage..."))
        self.calDescrLbl_2.setText(_translate("CoolOffFrm", "Please wait..."))
        self.cancelBtn.setText(_translate("CoolOffFrm", "Cancel"))

