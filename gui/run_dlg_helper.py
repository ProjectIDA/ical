# import subprocess

from PyQt5 import QtCore, QtWidgets

import gui.mainwindow
from gui.run_dlg import Ui_RunDlg

# from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg
from config.calib import Calib

from gui.cfg_data_model import CfgDataModel

class RunDlgHelper(object):

    def __init__(self, wcfg, calib_rec, cfg_root_dir, run_dlg, sensor, caltype):
        self.wcfg = wcfg
        self.calib_rec = calib_rec
        self.root_dir = cfg_root_dir
        self.is_reachable = False
        self.run_dlg = run_dlg
        self.sensor = sensor.upper()
        self.caltype = caltype

        self.sensor_descr = self.wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] if self.sensor == 'A' else self.wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B]

        self.cmdline = self.wcfg.gen_qcal_cmdline(sensor, caltype)
        self.cmdline += ' root=' + self.root_dir

        if calib_rec:
            self.cal_time_mins = calib_rec.cal_time_min()
        else:
            self.cal_time_mins = 'Unknown'


    def setupUi(self, dlg):

        self.dlg = dlg

        self.caldescr = '\n'.join([
            'Q330    :  Tag# ' + self.wcfg.data[WrapperCfg.WRAPPER_KEY_TAGNO] + '  at  ' + self.wcfg.data[WrapperCfg.WRAPPER_KEY_IP],
            'Sensor ' + self.sensor + ':  ' + self.sensor_descr,
            'Cal Type:  ' + Calib.caltype_descr(self.caltype)])

        self.run_dlg.confirmTextLbl.setWordWrap(True)
        self.run_dlg.confirmTextLbl.setText('\n'.join([ self.caldescr, \
            # 'Q330 Tag:   # ' + self.wcfg.data[WrapperCfg.WRAPPER_KEY_TAGNO] + '  at  ' + self.wcfg.data[WrapperCfg.WRAPPER_KEY_IP],
            # 'Sensor ' + self.sensor + ':  ' + self.sensor_descr,
            # 'Cal Type:  ' + Calib.caltype_descr(self.caltype),
            '\nApproximate Calibration Time: {} mins'.format(self.cal_time_mins)
            ]))

        self.run_dlg.cmdlineBtn.clicked.connect(self.show_cmdline)


    def show_cmdline(self):

        QtWidgets.QMessageBox().information(self.dlg, 'ICAL: qcal Cmd Line', self.cmdline, QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)                    

