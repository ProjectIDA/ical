import time
import logging

from PyQt5 import QtCore, QtWidgets

from gui.progress_dlg import Ui_ProgressDlg

import config.pycal_globals as pcgl
from config.wrapper_cfg import WrapperCfg
from comms.ical_threads import QCalThread


class ProgressDlgHelper(object):

    UPDATE_PERIOD = 1 # seconds


    def __init__(self, bindir, cmdline, caldescr, caltime, progdlg):
        self.bindir = bindir
        self.cmdline = cmdline
        self.caldescr = caldescr
        self.caltime = caltime
        self.progdlg = progdlg
        self.elapsed = 0


    def setupUi(self, qtdlg):

        self.qtdlg = qtdlg

        self.progdlg.cancelBtn.clicked.connect(self.cancelled)

        self.progdlg.calDescrLbl.setText(self.caldescr)

        self.progdlg.maxLbl.setText('Approximately ' + str(self.caltime) + ' minutes')
        self.progdlg.minLbl.setText('0')
        self.progdlg.valLbl.setText('')
        self.progdlg.progPB.setMinimum(0)
        self.progdlg.progPB.setValue(0)
        self.progdlg.progPB.setMaximum(int(self.caltime * 60))

        # qcal thread callback
        self.qcalThread = QCalThread(pcgl.get_bin_root(), self.cmdline, pcgl.get_results_root())
        self.qcalThread.qcalResult.connect(self.qcal_finished)

        self.qcalThread.start()


        # progress timer
        self.timer = QtCore.QTimer(self.qtdlg)
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.UPDATE_PERIOD * 1000)


    def tick(self):
        self.elapsed += self.UPDATE_PERIOD
        self.progdlg.progPB.setValue(self.elapsed)
        self.progdlg.valLbl.setText(str(int((self.elapsed * 100) / (self.caltime * 60))) + '%')


    def qcal_finished(self, retcode, msg):
        self.retcode = retcode
        self.msg = msg
        logging.info('cal completed with error code: {}\n{}'.format(self.retcode, self.msg))
        self.qtdlg.accept()


    def cancelled(self):
        self.retcode = 1
        logging.info('Calibration canceled by user.')
        self.msg = 'Calibration canceled by user.'
        self.qcalThread.cancel()
        self.qcalThread = None
        self.qtdlg.reject()