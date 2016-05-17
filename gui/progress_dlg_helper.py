import time
import logging
from PyQt5.QtCore import QTimer


class ProgressDlgHelper(object):

    UPDATE_PERIOD = 1  # seconds


    # def __init__(self, cmdline, descr, total_time_mins, progdlg):
    def __init__(self, qtdlg, descr, total_time_mins, progdlg, qcal_thread):
        # self.cmdline = cmdline
        self.caldescr = descr
        self.total_time_mins = total_time_mins + 0.25  # threading/processing overhead fudge factor
        self.progdlg = progdlg
        self.elapsed = 0
        self.qtdlg = qtdlg
        self.timer = QTimer(self.qtdlg)
        self.qcal_thread = qcal_thread
        self.retcode = -1
        self.msg = ''
        self.calmsfn = ''
        self.progdlg.calWarningLbl.setText('Do NOT disconnect from the network and\n'
                                           'Do NOT allow the computer to sleep\n ' +
                                           'while the calibration is running.')


    def start(self):

        self.progdlg.cancelBtn.clicked.connect(self.cancelled)

        self.progdlg.calDescrLbl.setText(self.caldescr)

        self.progdlg.maxLbl.setText('~' + str(round(self.total_time_mins,1)) + ' mins')
        self.progdlg.minLbl.setText('0')
        self.progdlg.valLbl.setText('')
        self.progdlg.progPB.setMinimum(0)
        self.progdlg.progPB.setValue(0)
        self.progdlg.progPB.setMaximum(self.total_time_mins * 60)

        logging.debug('Setting QProgress max to:' + str(self.total_time_mins * 60))

        logging.debug('Starting qcal thread...')

        self.qcal_thread.completed.connect(self.completed)
        self.qcal_thread.start()

        self.elapsed = 0

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.UPDATE_PERIOD * 1000)


    def tick(self):
        self.elapsed += self.UPDATE_PERIOD
        logging.debug('Progress tick at : {}'.format(time.time()))
        self.progdlg.progPB.setValue(self.elapsed)
        self.progdlg.valLbl.setText(str(int((self.elapsed * 100) / (self.total_time_mins * 60))) + '%')


    def completed(self, retcode, msg, calmsfn):

        logging.debug('Starting qcal thread... complected with retcode: ' + str(retcode))

        self.retcode = retcode
        self.msg = msg
        self.calmsfn = calmsfn
        self.qcal_thread = None
        self.qtdlg.accept()


    def cancelled(self):
        logging.debug('Starting qcal thread... killed by user')
        logging.info('Calibration canceled by user.')
        self.retcode = 1
        self.msg = 'Calibration canceled by user.'
        self.qcal_thread.cancel()
        self.qcal_thread = None
        self.qtdlg.reject()
