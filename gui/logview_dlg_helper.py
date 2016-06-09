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
