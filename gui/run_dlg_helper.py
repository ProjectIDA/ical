from PyQt5 import QtCore, QtWidgets

# import gui.mainwindow
# from gui.run_dlg import Ui_RunDlg

# from config.ical_config import IcalConfig
# from config.wrapper_cfg import WrapperCfg
# from config.calib import Calib
#
# from gui.cfg_data_model import CfgDataModel

class RunDlgHelper(object):

    # def __init__(self, wcfg, calib_rec, cfg_root_dir, run_dlg, sensor, caltype):
    def __init__(self, run_dlg, cal_descr, cal_time_mins, cmd_line):
        self.run_dlg = run_dlg
        self.cal_descr = cal_descr
        self.cal_time_mins = cal_time_mins
        self.cmd_line = cmd_line


    def setup_ui(self, dlg):

        self.dlg = dlg
        self.run_dlg.confirmTextLbl.setWordWrap(True)
        self.run_dlg.confirmTextLbl.setText('{}\n\nApproximate Calibration Time: {} mins'.format(self.cal_descr, self.cal_time_mins))
        self.run_dlg.cmdlineBtn.clicked.connect(self.show_cmdline)


    def show_cmdline(self):

        QtWidgets.QMessageBox().information(self.dlg, 'PyCal: qcal Cmd Line', self.cmd_line, QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)

