# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.calListGB = QtWidgets.QGroupBox(self.centralWidget)
        self.calListGB.setGeometry(QtCore.QRect(10, 10, 1070, 251))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.calListGB.setFont(font)
        self.calListGB.setObjectName("calListGB")
        self.cfgListTV = QtWidgets.QTableView(self.calListGB)
        self.cfgListTV.setGeometry(QtCore.QRect(10, 61, 1050, 181))
        self.cfgListTV.setAlternatingRowColors(True)
        self.cfgListTV.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.cfgListTV.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.cfgListTV.setCornerButtonEnabled(False)
        self.cfgListTV.setObjectName("cfgListTV")
        self.addBtn = QtWidgets.QPushButton(self.calListGB)
        self.addBtn.setEnabled(False)
        self.addBtn.setGeometry(QtCore.QRect(950, 29, 115, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addBtn.setFont(font)
        self.addBtn.setObjectName("addBtn")
        self.editBtn = QtWidgets.QPushButton(self.calListGB)
        self.editBtn.setEnabled(False)
        self.editBtn.setGeometry(QtCore.QRect(820, 29, 115, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.editBtn.setFont(font)
        self.editBtn.setObjectName("editBtn")
        self.calDetailsGB = QtWidgets.QGroupBox(self.centralWidget)
        self.calDetailsGB.setGeometry(QtCore.QRect(10, 270, 1070, 290))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.calDetailsGB.setFont(font)
        self.calDetailsGB.setObjectName("calDetailsGB")
        self.sensorAGB = QtWidgets.QGroupBox(self.calDetailsGB)
        self.sensorAGB.setGeometry(QtCore.QRect(330, 40, 360, 211))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.sensorAGB.setFont(font)
        self.sensorAGB.setTitle("")
        self.sensorAGB.setObjectName("sensorAGB")
        self.label = QtWidgets.QLabel(self.sensorAGB)
        self.label.setGeometry(QtCore.QRect(68, 31, 42, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.sensorAGB)
        self.label_2.setGeometry(QtCore.QRect(15, 78, 95, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(95, 0))
        self.label_2.setMaximumSize(QtCore.QSize(95, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.sensorAGB)
        self.label_3.setGeometry(QtCore.QRect(35, 105, 75, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(75, 0))
        self.label_3.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.sensAMonPortLE = QtWidgets.QLineEdit(self.sensorAGB)
        self.sensAMonPortLE.setGeometry(QtCore.QRect(118, 77, 50, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensAMonPortLE.sizePolicy().hasHeightForWidth())
        self.sensAMonPortLE.setSizePolicy(sizePolicy)
        self.sensAMonPortLE.setMinimumSize(QtCore.QSize(50, 0))
        self.sensAMonPortLE.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensAMonPortLE.setFont(font)
        self.sensAMonPortLE.setFrame(False)
        self.sensAMonPortLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensAMonPortLE.setPlaceholderText("")
        self.sensAMonPortLE.setObjectName("sensAMonPortLE")
        self.sensALastLFLE = QtWidgets.QLineEdit(self.sensorAGB)
        self.sensALastLFLE.setGeometry(QtCore.QRect(118, 105, 230, 17))
        self.sensALastLFLE.setMinimumSize(QtCore.QSize(230, 0))
        self.sensALastLFLE.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensALastLFLE.setFont(font)
        self.sensALastLFLE.setFrame(False)
        self.sensALastLFLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensALastLFLE.setPlaceholderText("")
        self.sensALastLFLE.setObjectName("sensALastLFLE")
        self.sensARunLFBtn = QtWidgets.QPushButton(self.sensorAGB)
        self.sensARunLFBtn.setEnabled(False)
        self.sensARunLFBtn.setGeometry(QtCore.QRect(40, 170, 120, 32))
        self.sensARunLFBtn.setStyleSheet("color: red;")
        self.sensARunLFBtn.setObjectName("sensARunLFBtn")
        self.sensARunHFBtn = QtWidgets.QPushButton(self.sensorAGB)
        self.sensARunHFBtn.setEnabled(False)
        self.sensARunHFBtn.setGeometry(QtCore.QRect(200, 170, 120, 32))
        self.sensARunHFBtn.setStyleSheet("color: red;")
        self.sensARunHFBtn.setObjectName("sensARunHFBtn")
        self.sensADescrLE = QtWidgets.QPlainTextEdit(self.sensorAGB)
        self.sensADescrLE.setGeometry(QtCore.QRect(118, 29, 230, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensADescrLE.sizePolicy().hasHeightForWidth())
        self.sensADescrLE.setSizePolicy(sizePolicy)
        self.sensADescrLE.setMinimumSize(QtCore.QSize(230, 40))
        self.sensADescrLE.setMaximumSize(QtCore.QSize(230, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensADescrLE.setFont(font)
        self.sensADescrLE.setAutoFillBackground(False)
        self.sensADescrLE.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sensADescrLE.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensADescrLE.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensADescrLE.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.sensADescrLE.setBackgroundVisible(False)
        self.sensADescrLE.setPlaceholderText("")
        self.sensADescrLE.setObjectName("sensADescrLE")
        self.label_27 = QtWidgets.QLabel(self.sensorAGB)
        self.label_27.setGeometry(QtCore.QRect(10, 10, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.sensALastHFLE = QtWidgets.QLineEdit(self.sensorAGB)
        self.sensALastHFLE.setGeometry(QtCore.QRect(118, 133, 230, 17))
        self.sensALastHFLE.setMinimumSize(QtCore.QSize(230, 0))
        self.sensALastHFLE.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensALastHFLE.setFont(font)
        self.sensALastHFLE.setFrame(False)
        self.sensALastHFLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensALastHFLE.setPlaceholderText("")
        self.sensALastHFLE.setObjectName("sensALastHFLE")
        self.label_4 = QtWidgets.QLabel(self.sensorAGB)
        self.label_4.setGeometry(QtCore.QRect(35, 133, 75, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(75, 0))
        self.label_4.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.sensorBGB = QtWidgets.QGroupBox(self.calDetailsGB)
        self.sensorBGB.setGeometry(QtCore.QRect(700, 40, 360, 209))
        self.sensorBGB.setTitle("")
        self.sensorBGB.setObjectName("sensorBGB")
        self.label_28 = QtWidgets.QLabel(self.sensorBGB)
        self.label_28.setGeometry(QtCore.QRect(10, 10, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.sensBLastLFLE = QtWidgets.QLineEdit(self.sensorBGB)
        self.sensBLastLFLE.setGeometry(QtCore.QRect(118, 105, 230, 17))
        self.sensBLastLFLE.setMinimumSize(QtCore.QSize(230, 0))
        self.sensBLastLFLE.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensBLastLFLE.setFont(font)
        self.sensBLastLFLE.setFrame(False)
        self.sensBLastLFLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensBLastLFLE.setPlaceholderText("")
        self.sensBLastLFLE.setObjectName("sensBLastLFLE")
        self.sensBLastHFLE = QtWidgets.QLineEdit(self.sensorBGB)
        self.sensBLastHFLE.setGeometry(QtCore.QRect(118, 133, 230, 17))
        self.sensBLastHFLE.setMinimumSize(QtCore.QSize(230, 0))
        self.sensBLastHFLE.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensBLastHFLE.setFont(font)
        self.sensBLastHFLE.setFrame(False)
        self.sensBLastHFLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensBLastHFLE.setPlaceholderText("")
        self.sensBLastHFLE.setObjectName("sensBLastHFLE")
        self.sensBRunLFBtn = QtWidgets.QPushButton(self.sensorBGB)
        self.sensBRunLFBtn.setEnabled(False)
        self.sensBRunLFBtn.setGeometry(QtCore.QRect(40, 170, 120, 32))
        self.sensBRunLFBtn.setStyleSheet("color: red;")
        self.sensBRunLFBtn.setObjectName("sensBRunLFBtn")
        self.label_8 = QtWidgets.QLabel(self.sensorBGB)
        self.label_8.setGeometry(QtCore.QRect(35, 105, 75, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(75, 0))
        self.label_8.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.sensorBGB)
        self.label_9.setGeometry(QtCore.QRect(35, 133, 75, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(75, 0))
        self.label_9.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.sensBDescrLE = QtWidgets.QPlainTextEdit(self.sensorBGB)
        self.sensBDescrLE.setGeometry(QtCore.QRect(118, 29, 230, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensBDescrLE.sizePolicy().hasHeightForWidth())
        self.sensBDescrLE.setSizePolicy(sizePolicy)
        self.sensBDescrLE.setMinimumSize(QtCore.QSize(230, 40))
        self.sensBDescrLE.setMaximumSize(QtCore.QSize(230, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensBDescrLE.setFont(font)
        self.sensBDescrLE.setAutoFillBackground(False)
        self.sensBDescrLE.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sensBDescrLE.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensBDescrLE.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensBDescrLE.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.sensBDescrLE.setBackgroundVisible(False)
        self.sensBDescrLE.setPlaceholderText("")
        self.sensBDescrLE.setObjectName("sensBDescrLE")
        self.label_10 = QtWidgets.QLabel(self.sensorBGB)
        self.label_10.setGeometry(QtCore.QRect(68, 31, 42, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.sensBMonPortLE = QtWidgets.QLineEdit(self.sensorBGB)
        self.sensBMonPortLE.setGeometry(QtCore.QRect(118, 77, 50, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensBMonPortLE.sizePolicy().hasHeightForWidth())
        self.sensBMonPortLE.setSizePolicy(sizePolicy)
        self.sensBMonPortLE.setMinimumSize(QtCore.QSize(50, 0))
        self.sensBMonPortLE.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.sensBMonPortLE.setFont(font)
        self.sensBMonPortLE.setFrame(False)
        self.sensBMonPortLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sensBMonPortLE.setPlaceholderText("")
        self.sensBMonPortLE.setObjectName("sensBMonPortLE")
        self.label_14 = QtWidgets.QLabel(self.sensorBGB)
        self.label_14.setGeometry(QtCore.QRect(15, 78, 95, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QtCore.QSize(95, 0))
        self.label_14.setMaximumSize(QtCore.QSize(95, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.sensBRunHFBtn = QtWidgets.QPushButton(self.sensorBGB)
        self.sensBRunHFBtn.setEnabled(False)
        self.sensBRunHFBtn.setGeometry(QtCore.QRect(200, 170, 120, 32))
        self.sensBRunHFBtn.setStyleSheet("color: red;")
        self.sensBRunHFBtn.setObjectName("sensBRunHFBtn")
        self.q330GB = QtWidgets.QGroupBox(self.calDetailsGB)
        self.q330GB.setGeometry(QtCore.QRect(10, 40, 310, 241))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.q330GB.setFont(font)
        self.q330GB.setTitle("")
        self.q330GB.setObjectName("q330GB")
        self.label_26 = QtWidgets.QLabel(self.q330GB)
        self.label_26.setGeometry(QtCore.QRect(12, 7, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.widget = QtWidgets.QWidget(self.q330GB)
        self.widget.setGeometry(QtCore.QRect(5, 31, 295, 188))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.networkLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.networkLabel.setFont(font)
        self.networkLabel.setObjectName("networkLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.networkLabel)
        self.netLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.netLE.sizePolicy().hasHeightForWidth())
        self.netLE.setSizePolicy(sizePolicy)
        self.netLE.setMinimumSize(QtCore.QSize(60, 0))
        self.netLE.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.netLE.setFont(font)
        self.netLE.setFrame(False)
        self.netLE.setObjectName("netLE")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.netLE)
        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.staLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staLE.sizePolicy().hasHeightForWidth())
        self.staLE.setSizePolicy(sizePolicy)
        self.staLE.setMinimumSize(QtCore.QSize(60, 0))
        self.staLE.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.staLE.setFont(font)
        self.staLE.setFrame(False)
        self.staLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.staLE.setObjectName("staLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.staLE)
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.ipLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipLE.sizePolicy().hasHeightForWidth())
        self.ipLE.setSizePolicy(sizePolicy)
        self.ipLE.setMinimumSize(QtCore.QSize(145, 0))
        self.ipLE.setMaximumSize(QtCore.QSize(145, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.ipLE.setFont(font)
        self.ipLE.setFrame(False)
        self.ipLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ipLE.setObjectName("ipLE")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ipLE)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.tagnoLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagnoLE.sizePolicy().hasHeightForWidth())
        self.tagnoLE.setSizePolicy(sizePolicy)
        self.tagnoLE.setMinimumSize(QtCore.QSize(60, 0))
        self.tagnoLE.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.tagnoLE.setFont(font)
        self.tagnoLE.setFrame(False)
        self.tagnoLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.tagnoLE.setObjectName("tagnoLE")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.tagnoLE)
        self.label_11 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.snLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.snLE.sizePolicy().hasHeightForWidth())
        self.snLE.setSizePolicy(sizePolicy)
        self.snLE.setMinimumSize(QtCore.QSize(145, 0))
        self.snLE.setMaximumSize(QtCore.QSize(145, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.snLE.setFont(font)
        self.snLE.setFrame(False)
        self.snLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.snLE.setObjectName("snLE")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.snLE)
        self.label_12 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.dpLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dpLE.sizePolicy().hasHeightForWidth())
        self.dpLE.setSizePolicy(sizePolicy)
        self.dpLE.setMinimumSize(QtCore.QSize(60, 0))
        self.dpLE.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.dpLE.setFont(font)
        self.dpLE.setText("")
        self.dpLE.setFrame(False)
        self.dpLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.dpLE.setObjectName("dpLE")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.dpLE)
        self.label_13 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.dpauthLE = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dpauthLE.sizePolicy().hasHeightForWidth())
        self.dpauthLE.setSizePolicy(sizePolicy)
        self.dpauthLE.setMinimumSize(QtCore.QSize(60, 0))
        self.dpauthLE.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.dpauthLE.setFont(font)
        self.dpauthLE.setFrame(False)
        self.dpauthLE.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.dpauthLE.setObjectName("dpauthLE")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.dpauthLE)
        self.quitBtn = QtWidgets.QPushButton(self.centralWidget)
        self.quitBtn.setGeometry(QtCore.QRect(970, 570, 115, 32))
        self.quitBtn.setObjectName("quitBtn")
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainMenu = QtWidgets.QMenuBar(MainWindow)
        self.mainMenu.setGeometry(QtCore.QRect(0, 0, 1090, 22))
        self.mainMenu.setNativeMenuBar(False)
        self.mainMenu.setObjectName("mainMenu")
        self.menuFile = QtWidgets.QMenu(self.mainMenu)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.mainMenu)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout_ICAL = QtWidgets.QAction(MainWindow)
        self.actionAbout_ICAL.setEnabled(False)
        self.actionAbout_ICAL.setObjectName("actionAbout_ICAL")
        self.actionRunHF = QtWidgets.QAction(MainWindow)
        self.actionRunHF.setObjectName("actionRunHF")
        self.actionRunLF = QtWidgets.QAction(MainWindow)
        self.actionRunLF.setObjectName("actionRunLF")
        self.actionEditConfig = QtWidgets.QAction(MainWindow)
        self.actionEditConfig.setObjectName("actionEditConfig")
        self.actionAddConfig = QtWidgets.QAction(MainWindow)
        self.actionAddConfig.setObjectName("actionAddConfig")
        self.menuFile.addAction(self.actionAbout_ICAL)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.mainMenu.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.quitBtn.clicked.connect(self.actionQuit.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "iCal - Project IDA Calibration Tool"))
        self.calListGB.setTitle(_translate("MainWindow", "Stored Calibration Configurations"))
        self.addBtn.setText(_translate("MainWindow", "Add..."))
        self.editBtn.setText(_translate("MainWindow", "Edit..."))
        self.calDetailsGB.setTitle(_translate("MainWindow", "Selected Configuration Details"))
        self.label.setToolTip(_translate("MainWindow", "<html><head/><body><p>Sensor Model.</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Model:"))
        self.label_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Calibration Monitoring Port.</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Calib Mon Port:"))
        self.label_3.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) HIGH Frequency calibration (UTC)"))
        self.label_3.setText(_translate("MainWindow", "Last LF Cal:"))
        self.sensAMonPortLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>Calibration Monitoring Port.</p></body></html>"))
        self.sensALastLFLE.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) HIGH Frequency calibration (UTC)"))
        self.sensARunLFBtn.setToolTip(_translate("MainWindow", "Initiate LOW Frequency calibration on this sensor."))
        self.sensARunLFBtn.setText(_translate("MainWindow", "Run LF Cal..."))
        self.sensARunHFBtn.setToolTip(_translate("MainWindow", "Initiate HIGH Frequency calibration on this sensor."))
        self.sensARunHFBtn.setText(_translate("MainWindow", "Run HF Cal..."))
        self.label_27.setText(_translate("MainWindow", "Sensor A"))
        self.sensALastHFLE.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) LOW Frequency calibration (UTC)"))
        self.label_4.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) LOW Frequency calibration (UTC)"))
        self.label_4.setText(_translate("MainWindow", "Last HF Cal:"))
        self.label_28.setText(_translate("MainWindow", "Sensor B"))
        self.sensBLastLFLE.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) HIGH Frequency calibration (UTC)"))
        self.sensBLastHFLE.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) LOW Frequency calibration (UTC)"))
        self.sensBRunLFBtn.setToolTip(_translate("MainWindow", "Initiate LOW Frequency calibration on this sensor."))
        self.sensBRunLFBtn.setText(_translate("MainWindow", "Run LF Cal..."))
        self.label_8.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) HIGH Frequency calibration (UTC)"))
        self.label_8.setText(_translate("MainWindow", "Last LF Cal:"))
        self.label_9.setToolTip(_translate("MainWindow", "Timestamp of previous (successful) LOW Frequency calibration (UTC)"))
        self.label_9.setText(_translate("MainWindow", "Last HF Cal:"))
        self.label_10.setToolTip(_translate("MainWindow", "<html><head/><body><p>Sensor Model.</p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Model:"))
        self.sensBMonPortLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>Calibration Monitoring Port.</p></body></html>"))
        self.label_14.setToolTip(_translate("MainWindow", "<html><head/><body><p>Calibration Monitoring Port.</p></body></html>"))
        self.label_14.setText(_translate("MainWindow", "Calib Mon Port:"))
        self.sensBRunHFBtn.setToolTip(_translate("MainWindow", "Initiate HIGH Frequency calibration on this sensor."))
        self.sensBRunHFBtn.setText(_translate("MainWindow", "Run HF Cal..."))
        self.label_26.setText(_translate("MainWindow", "Q330"))
        self.networkLabel.setText(_translate("MainWindow", "Network"))
        self.netLE.setPlaceholderText(_translate("MainWindow", "NET"))
        self.label_5.setToolTip(_translate("MainWindow", "<html><head/><body><p>Three to six (alpha-numeric) character Station Code</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Station:"))
        self.staLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>Three to six (alpha-numeric) character Station Code</p></body></html>"))
        self.staLE.setPlaceholderText(_translate("MainWindow", "STA"))
        self.label_6.setToolTip(_translate("MainWindow", "<html><head/><body><p>IP4 network address used to communicate with this Q330.</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "IP4 Address:"))
        self.ipLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>IP4 network address used to communicate with this Q330.</p></body></html>"))
        self.ipLE.setPlaceholderText(_translate("MainWindow", "000.000.000.000"))
        self.label_7.setToolTip(_translate("MainWindow", "<html><head/><body><p>Kinemetric Tag Number for this Q330.</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "Tag #:"))
        self.tagnoLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>Kinemetric Tag Number for this Q330.</p></body></html>"))
        self.tagnoLE.setPlaceholderText(_translate("MainWindow", "0000"))
        self.label_11.setToolTip(_translate("MainWindow", "<html><head/><body><p>The Internal Serial Number for this Q330. This can be obtained by ...</p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "Int. SN:"))
        self.snLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>The Internal Serial Number for this Q330. This can be obtained by ...</p></body></html>"))
        self.snLE.setPlaceholderText(_translate("MainWindow", "0123456789ABCDEF"))
        self.label_12.setToolTip(_translate("MainWindow", "<html><head/><body><p>Data Port used for calibrating sensors attached to this Q330.</p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "Data Port:"))
        self.dpLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>Data Port used for calibrating sensors attached to this Q330.</p></body></html>"))
        self.dpLE.setPlaceholderText(_translate("MainWindow", "[1-4]"))
        self.label_13.setToolTip(_translate("MainWindow", "<html><head/><body><p>The Auth Code for access to the Data Port used in calibrations. If no auth code is set, this value should be \'0\'.</p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "Data Port Auth Code:"))
        self.dpauthLE.setToolTip(_translate("MainWindow", "<html><head/><body><p>The Auth Code for access to the Data Port used in calibrations. If no auth code is set, this value should be \'0\'.</p></body></html>"))
        self.dpauthLE.setPlaceholderText(_translate("MainWindow", "0"))
        self.quitBtn.setText(_translate("MainWindow", "Quit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout_ICAL.setText(_translate("MainWindow", "About ICAL..."))
        self.actionRunHF.setText(_translate("MainWindow", "RunHF"))
        self.actionRunHF.setToolTip(_translate("MainWindow", "Run HF Calibration"))
        self.actionRunLF.setText(_translate("MainWindow", "RunLF"))
        self.actionRunLF.setToolTip(_translate("MainWindow", "Run LF Calibration"))
        self.actionEditConfig.setText(_translate("MainWindow", "EditConfig"))
        self.actionEditConfig.setToolTip(_translate("MainWindow", "Edit Configuration"))
        self.actionAddConfig.setText(_translate("MainWindow", "AddConfig"))
        self.actionAddConfig.setToolTip(_translate("MainWindow", "Add Configuration"))

