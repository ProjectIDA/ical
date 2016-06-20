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

from time import time
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import QTimer

class CoolOffDlgHelper(object):

    update_interval = 5  # seconds

    def __init__(self, dlg, dlgUI):
        self.dlgUI = dlgUI
        self.qtDlg = dlg
        self.cooling_period_seconds = 330  # default to 5.5 minutes
        self.start_time = time()

        self.timer = QTimer(self.qtDlg)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.tick)

        self.dlgUI.cancelBtn.clicked.connect(self.cancel)


    def cancel(self):

        self.timer.stop()

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText('Do you wish to cancel this calibration?')
        msg_box.setInformativeText('If you cancel you will need to rerun the calibration from the beginning.')
        yes_btn = msg_box.addButton(QMessageBox.Yes)
        no_btn = msg_box.addButton(QMessageBox.No)
        msg_box.setDefaultButton(no_btn)

        msg_box.exec()

        if msg_box.clickedButton() == yes_btn:
            self.qtDlg.done(QDialog.Rejected)
        else:
            self.timer.start()


    def exec(self):
        self.start()
        return self.qtDlg.exec()


    def start(self):

        self.start_tme = time()
        self.dlgUI.progPB.setMinimum(-5)
        self.dlgUI.progPB.setMaximum(100)
        self.dlgUI.progPB.setValue(0)

        self.timer.start(1000 * self.update_interval)  # QTimer works in ms, so tick every 10 seconds


    def tick(self):

        pcnt_time = ((time() - self.start_time) / self.cooling_period_seconds) * 100.0

        if pcnt_time > 100:
            self.timer.stop()
            self.qtDlg.done(QDialog.Accepted)
        else:
            self.dlgUI.progPB.setValue(pcnt_time)

