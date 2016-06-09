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
import logging
from PyQt5.QtCore import QTimer


class ProgressDlgHelper(object):

    def __init__(self, qtdlg, descr, total_time_mins, progdlg, qcal_thread):
        # self.cmdline = cmdline
        self.caldescr = descr
        self.total_time_mins = total_time_mins + 0.3  # threading/processing overhead fudge factor
        self.update_interval = (self.total_time_mins * 60.0) / 100.0 # 0.1% of total time in secs (~16 secs for rblf)
        self.elapsed = 0
        self.qtdlg = qtdlg
        self.timer = QTimer(self.qtdlg)
        self.qcal_thread = qcal_thread
        self.retcode = -1
        self.msg = ''
        self.calmsfn = ''
        self.start_time = None
        self.progdlg = progdlg
        self.progdlg.calWarningLbl.setText('Do NOT disconnect from the network and\n'
                                           'Do NOT allow the computer to sleep\n ' +
                                           'while the calibration is running.')
        self.progdlg.valLbl.setText('0%')


    def start(self):

        self.start_time = time()
        self.end_time = self.start_time + self.total_time_mins * 60.0

        self.progdlg.cancelBtn.clicked.connect(self.canceled)

        self.progdlg.calDescrLbl.setText(self.caldescr)

        self.progdlg.maxLbl.setText('~' + str(round(self.total_time_mins,1)) + ' mins')
        self.progdlg.minLbl.setText('0')
        self.progdlg.valLbl.setText('0 %')
        self.progdlg.progPB.setMinimum(0)
        self.progdlg.progPB.setMaximum(self.total_time_mins * 60)
        self.progdlg.progPB.setValue(0)

        logging.debug('Setting QProgress max to:' + str(self.total_time_mins * 60))

        logging.debug('Starting qcal thread...')

        self.qcal_thread.completed.connect(self.completed)
        self.qcal_thread.start()

        self.elapsed = 0

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.update_interval * 1000)  # QTimer works in ms


    def tick(self):

        pcnt_time = ((time() - self.start_time) / (self.total_time_mins * 60.0)) * 100.0

        self.elapsed += self.update_interval
        self.progdlg.progPB.setValue(self.elapsed)
        self.progdlg.valLbl.setText(str(int(round(pcnt_time, 0))) + '%')


    def completed(self, retcode, msg, calmsfn):

        logging.debug('Starting qcal thread... complected with retcode: ' + str(retcode))

        self.retcode = retcode
        self.msg = msg
        self.calmsfn = calmsfn
        self.qcal_thread = None
        self.qtdlg.accept()


    def canceled(self):

        logging.info('Calibration canceled by user.')
        self.retcode = 1
        self.msg = 'Calibration canceled by user.'
        self.qcal_thread.cancel()
        self.qcal_thread = None
        self.qtdlg.reject()
