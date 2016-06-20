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

# Form implementation generated from reading ui file 'est_comms_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EstConnFrm(object):
    def setupUi(self, EstConnFrm):
        EstConnFrm.setObjectName("EstConnFrm")
        EstConnFrm.resize(480, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EstConnFrm.sizePolicy().hasHeightForWidth())
        EstConnFrm.setSizePolicy(sizePolicy)
        EstConnFrm.setMinimumSize(QtCore.QSize(480, 240))
        EstConnFrm.setMaximumSize(QtCore.QSize(480, 240))
        self.progPB = QtWidgets.QProgressBar(EstConnFrm)
        self.progPB.setGeometry(QtCore.QRect(20, 30, 441, 23))
        self.progPB.setMaximum(0)
        self.progPB.setProperty("value", -1)
        self.progPB.setObjectName("progPB")
        self.calDescrLbl = QtWidgets.QLabel(EstConnFrm)
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
        self.connMsgsEdit = QtWidgets.QPlainTextEdit(EstConnFrm)
        self.connMsgsEdit.setGeometry(QtCore.QRect(20, 90, 441, 101))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(128, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.connMsgsEdit.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.connMsgsEdit.setFont(font)
        self.connMsgsEdit.setReadOnly(True)
        self.connMsgsEdit.setPlainText("")
        self.connMsgsEdit.setObjectName("connMsgsEdit")
        self.closeBtn = QtWidgets.QPushButton(EstConnFrm)
        self.closeBtn.setEnabled(False)
        self.closeBtn.setGeometry(QtCore.QRect(324, 206, 141, 32))
        self.closeBtn.setObjectName("closeBtn")
        self.calDescrLbl_3 = QtWidgets.QLabel(EstConnFrm)
        self.calDescrLbl_3.setGeometry(QtCore.QRect(20, 70, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setBold(True)
        font.setWeight(75)
        self.calDescrLbl_3.setFont(font)
        self.calDescrLbl_3.setStyleSheet("line-height: 150%")
        self.calDescrLbl_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.calDescrLbl_3.setObjectName("calDescrLbl_3")

        self.retranslateUi(EstConnFrm)
        QtCore.QMetaObject.connectSlotsByName(EstConnFrm)

    def retranslateUi(self, EstConnFrm):
        _translate = QtCore.QCoreApplication.translate
        EstConnFrm.setWindowTitle(_translate("EstConnFrm", "Form"))
        self.calDescrLbl.setText(_translate("EstConnFrm", "Establishing connection to Q330..."))
        self.closeBtn.setText(_translate("EstConnFrm", "Close"))
        self.calDescrLbl_3.setText(_translate("EstConnFrm", "Connection messages:"))

