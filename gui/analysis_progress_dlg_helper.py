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

from PyQt5.QtWidgets import QMessageBox
from comms.ical_threads import AnalysisThread

class AnalysisProgressDlgHelper(object):

    def __init__(self, dlg, dlgUI):
        self.dlgUI = dlgUI
        self.qtDlg = dlg
        self.ims_calres_txt_fn = ''
        self.cal_amp_plot_fn = ''
        self.cal_pha_plot_fn = ''
        self.subthread = None

        self.dlgUI.cancelBtn.clicked.connect(self.cancel)


    def cancel(self):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText('Do you wish to cancel this anaylsis?')
        msg_box.setInformativeText('If you cancel you will need to rerun the calibration from the beginning.')
        yes_btn = msg_box.addButton(QMessageBox.Yes)
        no_btn = msg_box.addButton(QMessageBox.No)
        msg_box.setDefaultButton(no_btn)

        msg_box.exec()

        if msg_box.clickedButton() == yes_btn:
            self.subthread.cancel()
            self.qtDlg.done(-1)


    def run_analysis(self, run_method, *args):

        self.subthread = AnalysisThread(run_method, *args)
        self.subthread.completed.connect(self.finished)
        self.subthread.start()

        return self.qtDlg.exec(), \
               self.ims_calres_txt_fn, \
               self.cal_amp_plot_fn, \
               self.cal_pha_plot_fn


    def finished(self, ims_calres_txt_fn, cal_amp_plot_fn, cal_pha_plot_fn):
        self.ims_calres_txt_fn = ims_calres_txt_fn
        self.cal_amp_plot_fn = cal_amp_plot_fn
        self.cal_pha_plot_fn = cal_pha_plot_fn
        self.qtDlg.done(0)