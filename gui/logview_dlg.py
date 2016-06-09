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

# Form implementation generated from reading ui file 'logview_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogviewDlg(object):
    def setupUi(self, LogviewDlg):
        LogviewDlg.setObjectName("LogviewDlg")
        LogviewDlg.resize(703, 689)
        LogviewDlg.setMinimumSize(QtCore.QSize(703, 689))
        LogviewDlg.setMaximumSize(QtCore.QSize(703, 68915))
        LogviewDlg.setSizeGripEnabled(False)
        self.groupBox = QtWidgets.QGroupBox(LogviewDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 681, 631))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.logPTE = QtWidgets.QPlainTextEdit(self.groupBox)
        self.logPTE.setGeometry(QtCore.QRect(10, 31, 661, 591))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.logPTE.setFont(font)
        self.logPTE.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logPTE.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logPTE.setReadOnly(True)
        self.logPTE.setObjectName("logPTE")
        self.closeBtn = QtWidgets.QPushButton(LogviewDlg)
        self.closeBtn.setGeometry(QtCore.QRect(580, 650, 115, 32))
        self.closeBtn.setObjectName("closeBtn")
        self.clearBtn = QtWidgets.QPushButton(LogviewDlg)
        self.clearBtn.setGeometry(QtCore.QRect(5, 651, 115, 32))
        self.clearBtn.setObjectName("clearBtn")

        self.retranslateUi(LogviewDlg)
        QtCore.QMetaObject.connectSlotsByName(LogviewDlg)

    def retranslateUi(self, LogviewDlg):
        _translate = QtCore.QCoreApplication.translate
        LogviewDlg.setWindowTitle(_translate("LogviewDlg", "PyCal Log Viewer"))
        self.groupBox.setTitle(_translate("LogviewDlg", "PyCal Log"))
        self.closeBtn.setText(_translate("LogviewDlg", "Close"))
        self.clearBtn.setText(_translate("LogviewDlg", "Clear Log File"))

