# import subprocess

# from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QPlainTextEdit

# import gui.mainwindow
# from gui.logview_dlg import Ui_LogviewDlg

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

        self.refresh_timer = QTimer(self.qtDlg)

        # noinspection PyUnresolvedReferences
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(1000) # update every 1 seconds


    def refresh(self):
        self.readlog()
        self.update()


    def readlog(self):
        with open(self.logfilename, 'r') as fl:
            self.logtext = fl.read()


    def close(self):
        self.refresh_timer.stop()
        self.qtDlg.accept()


    def clear(self):
        with open(self.logfilename, 'w'):
            pass
        self.readlog()
        self.update()


    def update(self):
        prev_cur_pos = self.dlgUI.logPTE.verticalScrollBar().value()

        self.dlgUI.logPTE.setPlainText(self.logtext)

        if QApplication.activeWindow() != self.qtDlg:
            self.dlgUI.logPTE.moveCursor(QTextCursor.End)
            self.dlgUI.logPTE.ensureCursorVisible()
        else:
            self.dlgUI.logPTE.moveCursor(QTextCursor.End)
            new_cur_pos = self.dlgUI.logPTE.verticalScrollBar().setValue(prev_cur_pos)
