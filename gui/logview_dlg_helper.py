# import subprocess

from PyQt5 import QtCore, QtWidgets

import gui.mainwindow
from gui.logview_dlg import Ui_LogviewDlg


class LogviewDlgHelper(object):

    def __init__(self, logfilename, dlg, dlgUI):
        self.logfilename = logfilename
        self.dlgUI = dlgUI
        self.qtDlg = dlg

        self.readlog()
        self.update()

        self.dlgUI.logPTE.setReadOnly(True)
        self.dlgUI.closeBtn.clicked.connect(self.close)
        self.dlgUI.clearBtn.clicked.connect(self.clear)


    def readlog(self):
        with open(self.logfilename, 'r') as fl:
            self.logtext = fl.read()


    def close(self):
        self.qtDlg.accept()


    def clear(self):
        with open(self.logfilename, 'w'):
            pass
        self.readlog()
        self.update()


    def update(self):
        self.dlgUI.logPTE.setPlainText(self.logtext)

