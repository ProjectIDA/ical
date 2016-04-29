# import time
import logging
from PyQt5.QtCore import QTimer
# , QtWidgets
# import config.pycal_globals as pcgl
# from comms.ical_threads import QCalThread
# from gui.progress_dlg import Ui_ProgressDlg
# from config.wrapper_cfg import WrapperCfg


class ProgressDlgHelper(object):

    UPDATE_PERIOD = 1  # seconds


    # def __init__(self, cmdline, descr, total_time_mins, progdlg):
    def __init__(self, qtdlg, descr, total_time_mins, progdlg, qcal_thread):
        # self.cmdline = cmdline
        self.caldescr = descr
        self.total_time_mins = total_time_mins
        self.progdlg = progdlg
        self.elapsed = 0
        self.qtdlg = qtdlg
        self.timer = QTimer(self.qtdlg)
        self.qcal_thread = qcal_thread
        self.retcode = -1
        self.msg = ''
        self.calmsfn = ''


    def start(self):

        self.progdlg.cancelBtn.clicked.connect(self.cancelled)

        self.progdlg.calDescrLbl.setText(self.caldescr)

        self.progdlg.maxLbl.setText('Approximately ' + str(self.total_time_mins) + ' minutes')
        self.progdlg.minLbl.setText('0')
        self.progdlg.valLbl.setText('')
        self.progdlg.progPB.setMinimum(0)
        self.progdlg.progPB.setValue(0)
        self.progdlg.progPB.setMaximum(int(self.total_time_mins * 60))

        # qcal thread callback
        # self.qcal_thread = QCalThread(pcgl.get_bin_root(), self.cmdline, pcgl.get_results_root())
        self.qcal_thread.completed.connect(self.completed)
        self.qcal_thread.start()

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.UPDATE_PERIOD * 1000)


    def tick(self):
        self.elapsed += self.UPDATE_PERIOD
        self.progdlg.progPB.setValue(self.elapsed)
        self.progdlg.valLbl.setText(str(int((self.elapsed * 100) / (self.total_time_mins * 60))) + '%')


    def completed(self, retcode, msg, calmsfn):
        self.retcode = retcode
        self.msg = msg
        self.calmsfn = calmsfn
        self.qcal_thread = None
        self.qtdlg.accept()


    def cancelled(self):
        self.retcode = 1
        logging.info('Calibration canceled by user.')
        self.msg = 'Calibration canceled by user.'
        self.qcal_thread.cancel()
        self.qcal_thread = None
        self.qtdlg.reject()
