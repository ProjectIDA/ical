import subprocess

from PyQt5 import QtCore, QtWidgets

import gui.iCalGui.mw
from gui.iCalGui.run_confirm_dlg import Ui_RunDlg
from gui.iCalGui.edit_dlg import Ui_EditDlg

from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg

from gui.iCalGui.cfg_data_model import CfgDataModel

class MainWindowHelper(object):

    def __init__(self, cfg, app_win, main_win):
        self.cfg = cfg
        self.app_win = app_win
        self.main_win = main_win
        self.cur_row = -1
        self.set_run_btns_enabled(self.cur_row)



    def setup_main_window(self):
        self.setup_actionQuit()
        self.setup_tableview()
        self.setup_actionRun()

    def setup_actionQuit(self):
        self.main_win.actionQuit.triggered.connect(self.app_win.close)
        self.main_win.quitBtn.clicked.connect(self.main_win.actionQuit.trigger)


    # def setup_actionAboutICAL(MainWindow, mw_ui):
    #     return

    def setup_actionRun(self):
        self.main_win.sensARunLFBtn.clicked.connect(self.run_cal_A_LF)
        self.main_win.sensARunHFBtn.clicked.connect(self.run_cal_A_HF)
        self.main_win.sensBRunLFBtn.clicked.connect(self.run_cal_B_LF)
        self.main_win.sensBRunHFBtn.clicked.connect(self.run_cal_B_HF)


    # def setup_actionRunLF(MainWindow, mw_ui):
    #     return

    # def setup_actionEditConfig(MainWindow, mw_ui):
    #     return

    # def setup_actionAddConfig(MainWindow, mw_ui):
    #     return

    def setup_tableview(self): #MainWindow, mw_ui):

        self.cdm = CfgDataModel(self.cfg)
       
        self.main_win.cfgListTV.setModel(self.cdm)

        hdrvw = self.main_win.cfgListTV.horizontalHeader()
        hdrvw.setStretchLastSection(True)
        self.main_win.cfgListTV.resizeColumnsToContents()

        self.main_win.cfgListTV.doubleClicked.connect(self.MWEditRow)
        self.main_win.cfgListTV.selectionModel().selectionChanged.connect(self.MWSelectionChanged)


    def run_cal(self, sensor, caltype):

        if self.cur_row >= 0:
            wcfg = self.cfg[self.cur_row]
            if wcfg:
                cmdline = wcfg.gen_qcal_cmdline(sensor, caltype)
                cmdline += ' root=' + self.cfg.root_dir
                dlg = QtWidgets.QDialog()
                rundlg = Ui_RunDlg()
                rundlg.setupUi(dlg)
                # print(dir(rundlg))
                rundlg.cmdlineLE.setText(cmdline)
                dlg.exec()


    def run_cal_A_LF(self):
        self.run_cal('A', 'rblf')

    def run_cal_A_HF(self):
        self.run_cal('A', 'rbhf')

    def run_cal_B_LF(self):
        self.run_cal('B', 'rblf')

    def run_cal_B_HF(self):
        self.run_cal('B', 'rbhf')


    def MWSelectionChanged(self, seldelta, deseldelta):

        sel_ndxs = self.main_win.cfgListTV.selectedIndexes()

        if len(sel_ndxs) >= 1:
            self.cur_row = sel_ndxs[0].row()
        else:
            self.cur_row = -1

        self.update_details(self.cur_row)
        self.set_run_btns_enabled(self.cur_row)

        # self.ping_hosts()

    def MWEditRow(self, index):

        col = index.column()
        row = index.row()

        print('row edit:',row)    


    def update_details(self, row):

        if row == -1:
            self.clear_details()
        else:
            self.set_details(row)


    def ping_hosts(self):

        for wcfg in self.cfg:
            print('IP:', wcfg.data[WrapperCfg.WRAPPER_KEY_IP])
            ipaddress = wcfg.data[WrapperCfg.WRAPPER_KEY_IP]
            # ipaddress = '132.239.153.83'  # guess who
            proc = subprocess.Popen(
                ['ping', '-c', '1', '-t', '1', ipaddress],
                stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if proc.returncode == 0:
                print('{} is UP'.format(ipaddress))
            else:
                print('{} is DOWN'.format(ipaddress))


    def set_run_btns_enabled(self, row):

        if (row == -1):
            self.main_win.sensARunLFBtn.setEnabled(False)
            self.main_win.sensARunHFBtn.setEnabled(False)
            self.main_win.sensBRunLFBtn.setEnabled(False)
            self.main_win.sensBRunHFBtn.setEnabled(False)
        else:
            wcfg = self.cfg[self.cur_row]
            self.main_win.sensARunLFBtn.setEnabled(wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] != 'none')
            self.main_win.sensARunHFBtn.setEnabled(wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] != 'none')
            self.main_win.sensBRunLFBtn.setEnabled(wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] != 'none')
            self.main_win.sensBRunHFBtn.setEnabled(wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] != 'none')

        # self.main_win.sensARunLFBtn.changeEvent(QtCore.QEvent(QtCore.QEvent.EnabledChange))
        # self.main_win.sensARunHFBtn.changeEvent(QtCore.QEvent(QtCore.QEvent.EnabledChange))
        # self.main_win.sensBRunLFBtn.changeEvent(QtCore.QEvent(QtCore.QEvent.EnabledChange))
        # self.main_win.sensBRunHFBtn.changeEvent(QtCore.QEvent(QtCore.QEvent.EnabledChange))


    def clear_details(self):

        self.main_win.netLE.setText('');
        self.main_win.staLE.setText('');
        self.main_win.ipLE.setText('');
        self.main_win.tagnoLE.setText('');
        self.main_win.snLE.setText('');
        self.main_win.dpLE.setText('');
        self.main_win.dpauthLE.setText('');

        self.main_win.sensADescrLE.setPlainText('');
        self.main_win.sensAMonPortLE.setText('');
        self.main_win.sensALastLFLE.setText('');
        self.main_win.sensALastHFLE.setText('');

        self.main_win.sensBDescrLE.setPlainText('');
        self.main_win.sensBMonPortLE.setText('');
        self.main_win.sensBLastLFLE.setText('');
        self.main_win.sensBLastHFLE.setText('');

    def set_details(self, cfg_ndx):

        cfg = self.cfg[cfg_ndx]

        # for k,v in cfg.data.items(): 
        #     print(k,v)

        self.main_win.netLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_NET])
        self.main_win.staLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_STA])
        self.main_win.ipLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_IP])
        self.main_win.tagnoLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_TAGNO])
        self.main_win.snLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_SN])
        self.main_win.dpLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DATAPORT])
        self.main_win.dpauthLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DP1_AUTH])

        self.main_win.sensADescrLE.setPlainText(cfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A])
        if cfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A].lower() == 'none':
            self.main_win.sensAMonPortLE.setText('')
            self.main_win.sensALastLFLE.setText('')
            self.main_win.sensALastHFLE.setText('')
        else:
            self.main_win.sensAMonPortLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_A])
            self.main_win.sensALastLFLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_LF_A])
            self.main_win.sensALastHFLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_HF_A])

        self.main_win.sensBDescrLE.setPlainText(cfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B])
        if cfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B].lower() == 'none':
            self.main_win.sensBMonPortLE.setText('')
            self.main_win.sensBLastLFLE.setText('')
            self.main_win.sensBLastHFLE.setText('')
        else:
            self.main_win.sensBMonPortLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_B])
            self.main_win.sensBLastLFLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_LF_B])
            self.main_win.sensBLastHFLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_HF_B])

