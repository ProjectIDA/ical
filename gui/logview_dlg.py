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

