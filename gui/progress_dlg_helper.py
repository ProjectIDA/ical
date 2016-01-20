from PyQt5 import QtCore, QtWidgets

from gui.progress_dlg import Ui_ProgressDlg

# from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg


class ProgressDlgHelper(object):


    def __init__(self, cmdline, caldescr, caltime, progdlg):
        self.cmdline = cmdline
        self.caldescr = caldescr
        self.caltime = caltime
        self.progdlg = progdlg


    def setupUi(self, qtdlg):

        self.qtdlg = qtdlg

        self.progdlg.calDescrLbl.setText(self.caldescr)
        self.progdlg.maxLbl.setText(str(self.caltime) + ' minutes')
        self.progdlg.minLbl.setText('0')
        self.progdlg.progPB.setMinimum(0)
        self.progdlg.progPB.setMaximum(int(self.caltime))

        # just for testing
        self.progdlg.progPB.setValue(int(self.caltime/3))

