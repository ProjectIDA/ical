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

import logging
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer

import config.config_utils as pcgl
from config.wrapper_cfg import WrapperCfg
from comms.ical_threads import QVerifyThread

class EstCommsDlgHelper(object):

    def __init__(self, dlg, dlgUI, sensor, cfg):
        self.qtDlg = dlg
        self.dlgUI = dlgUI
        self.sensor = sensor
        self.cfg = cfg
        self.qVerify_thread = None
        self.qVerify_returned = False
        self.result = QDialog.Accepted

        if sensor.upper() == 'A':
            self.mon_port = self.cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_A]
        else:
            self.mon_port = self.cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_B]

        self.dlgUI.closeBtn.clicked.connect(self.close)


    def close(self):
        self.qtDlg.done(self.result)


    def exec(self):

        self.qVerifyThread = QVerifyThread(self.cfg.data[WrapperCfg.WRAPPER_KEY_IP],
                                           self.cfg.data[WrapperCfg.WRAPPER_KEY_DATAPORT],
                                           pcgl.get_bin_root(),
                                           pcgl.get_config_root())

        self.qVerifyThread.qVerifyQueryResult.connect(self.qVerify_query_result_slot)
        self.qVerifyThread.start()
        self.dlgUI.connMsgsEdit.setStyleSheet("QLabel{color:rgb(200, 120, 20);}")
        self.dlgUI.connMsgsEdit.setPlainText('Connecting to Q330 at {}...'.format(self.cfg.data[WrapperCfg.WRAPPER_KEY_IP]))

        QTimer.singleShot(30000, self.timeout)

        return self.qtDlg.exec()


    def timeout(self):

        if not self.qVerify_returned:
            self.qVerifyThread.qVerifyQueryResult.disconnect(self.qVerify_query_result_slot)
            self.qVerifyThread.cancel()
            self.qVerifyThread.quit()
            self.dlgUI.connMsgsEdit.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
            self.dlgUI.connMsgsEdit.setPlainText('Unable to connect to Q330 at {}.'.format(
                self.cfg.data[WrapperCfg.WRAPPER_KEY_IP])
            )
            self.dlgUI.closeBtn.setEnabled(True)
            self.result = QDialog.Rejected


    def qVerify_query_result_slot(self, host, port, error, results):

        self.qVerify_returned = True
        self.dlgUI.closeBtn.setEnabled(True)

        logging.info('QVerify establishment of connection successful: ' + str(not error))
        logging.info('QVerify result message: ' + results.strip())

        act_ports = results.split()[7:]
        if error != 0:
            self.result = QDialog.Rejected
            self.dlgUI.connMsgsEdit.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
            self.dlgUI.connMsgsEdit.setPlainText(results.strip())
        elif not self.mon_port in act_ports:
            self.dlgUI.connMsgsEdit.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
            self.dlgUI.connMsgsEdit.setPlainText(
                'Q330 (Tag #: {}) Sensor {} calibration monitoring channel [{}] is not '
                'in the list of channels enabled in the Q330 Global Setup: [{}].'.format(
                    self.cfg.data[WrapperCfg.WRAPPER_KEY_TAGNO],
                    self.sensor,
                    self.mon_port,
                    ', '.join(act_ports)
                )
            )
            logging.error('Monitoring channel not enabled in Q330 Global Setup.')
            self.result = QDialog.Rejected
        else:  # all good...
            self.dlgUI.connMsgsEdit.setStyleSheet("QLabel{color:rgb(0, 102, 0);}")
            self.dlgUI.connMsgsEdit.setPlainText('Connection successful.')
            logging.debug('QVerify q330 checks are OK')
            self.result = QDialog.Accepted
            self.close()
