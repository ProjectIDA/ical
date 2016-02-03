import subprocess

from PyQt5 import QtCore, QtWidgets, QtGui

import gui.mainwindow

from gui.run_dlg import Ui_RunDlg
from gui.run_dlg_helper import RunDlgHelper

from gui.progress_dlg import Ui_ProgressDlg
from gui.progress_dlg_helper import ProgressDlgHelper

from gui.edit_dlg import Ui_EditDlg
from gui.edit_dlg_helper import EditDlgHelper

from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg

from gui.cfg_data_model import CfgDataModel

class MainWindowHelper(object):

    def __init__(self, cfg, app_win, main_win):
        self.cfg = cfg
        self.cdm = CfgDataModel(self.cfg)
        self.app_win = app_win
        self.main_win = main_win
        self.cur_row = -1
        self.set_run_btns_enabled(self.cur_row)


    def setup_main_window(self):
        self.setup_actionQuit()
        self.setup_tableview()
        self.setup_actionRun()
        self.setup_actionEdit()


    def setup_actionQuit(self):
        self.main_win.actionQuit.triggered.connect(self.close)
        self.main_win.quitBtn.clicked.connect(self.main_win.actionQuit.trigger)


    def setup_actionRun(self):
        self.main_win.sensARunLFBtn.clicked.connect(self.run_cal_A_LF)
        self.main_win.sensARunHFBtn.clicked.connect(self.run_cal_A_HF)
        self.main_win.sensBRunLFBtn.clicked.connect(self.run_cal_B_LF)
        self.main_win.sensBRunHFBtn.clicked.connect(self.run_cal_B_HF)


    def setup_actionEdit(self):
        self.main_win.addBtn.clicked.connect(self.AddCfg)
        self.main_win.editBtn.clicked.connect(self.EditCfg)


    def setup_tableview(self): #MainWindow, mw_ui):

        self.main_win.cfgListTV.setModel(self.cdm)

        hdrvw = self.main_win.cfgListTV.horizontalHeader()
        hdrvw.setStretchLastSection(True)
        self.main_win.cfgListTV.resizeColumnsToContents()

        self.main_win.cfgListTV.setSortingEnabled(False)

        self.main_win.cfgListTV.doubleClicked.connect(self.TVDoubleClick)
        self.main_win.cfgListTV.selectionModel().selectionChanged.connect(self.MWSelectionChanged)


    def close(self):
        self.app_win.close()


    def TVDoubleClick(self, index):
        self.EditCfg()


    def setup_edit_dialog(self, edit_mode, cur_data={}):

        dlg = QtWidgets.QDialog(self.app_win)
        dlgUI = Ui_EditDlg()
        dlgUI.setupUi(dlg)

        dlgUIHlpr = EditDlgHelper()
        dlgUIHlpr.sensorlist = self.cfg.sensor_list()

        dlgUIHlpr.setupUi(cur_data, edit_mode, dlg, dlgUI)
    
        if edit_mode == EditDlgHelper.EDIT_MODE:
            dlg.setWindowTitle('ICAL - Edit Configuration')
        elif edit_mode == EditDlgHelper.ADD_MODE:
            dlg.setWindowTitle('ICAL - Add New Configuration')

        return (dlg, dlgUI, dlgUIHlpr)


    def EditCfg(self):

        if self.cur_row >= 0:
            # get tagno and then wcfg...
            mdlNdx = QtCore.QAbstractItemModel.createIndex(self.cdm, self.cur_row, CfgDataModel.TAGNO_COL)
            tagno = self.cdm.data(mdlNdx, QtCore.Qt.DisplayRole)
            wcfg = self.cfg.find(tagno)
            if wcfg:

                dlg, dlgUI, dlgUIHlpr = self.setup_edit_dialog(EditDlgHelper.EDIT_MODE, wcfg.data)
                # need to keep dlgUIHlpr in scope for GUI callbacks
                if dlg.exec() == QtWidgets.QDialog.Accepted:
                    try:
                        self.cdm.UpdateCfg(wcfg.tagno(), dlgUI.new_cfg)
                        self.update_details(self.cur_row)
                    except Exception as e:
                        QtWidgets.QMessageBox().critical(self.app_win, 'ICAL ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)                    


                    self.main_win.cfgListTV.resizeColumnsToContents()

                dlg, dlgUI, dlgUIHlpr = None, None, None


    def AddCfg(self):

        dlg, dlgUI, dlgUIHlpr = self.setup_edit_dialog(EditDlgHelper.ADD_MODE, {})
        # need to keep dlgUIHlpr in scope for GUI callbacks
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            try:
                self.cdm.AddCfg(dlgUI.new_cfg)
            except Exception as e:
                QtWidgets.QMessageBox().critical(self.app_win, 'ICAL ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)                    

            self.main_win.cfgListTV.resizeColumnsToContents()


    def run_cal_confirm(self, sensor, caltype):

        if self.cur_row >= 0:
            wcfg = self.cfg[self.cur_row]
            if wcfg:
                # need to get calib obj to estimate cal time
                sens_name = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] if sensor.upper() == 'A' \
                    else wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B]
                calib = self.cfg.find_calib(sens_name + '|' + caltype)
                if not calib:
                    QtWidgets.QMessageBox().critical(self.app_win, 'ICAL ERROR', 'ERROR Calib Record not Found for ['+ sens_name + '|' + caltype + ']', QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)                    
                dlg = QtWidgets.QDialog(self.app_win)
                rundlg = Ui_RunDlg()
                rundlg.setupUi(dlg)
                dlg.setWindowTitle('ICAL - Run Calibration Confirmation')

                rundlgHlpr = RunDlgHelper(wcfg, calib, self.cfg.root_dir, rundlg, sensor, caltype)
                rundlgHlpr.setupUi(dlg)

                if dlg.exec() == QtWidgets.QDialog.Accepted:

                    dlg = QtWidgets.QDialog(self.app_win)

                    progdlg = Ui_ProgressDlg()
                    progdlg.setupUi(dlg)
                    dlg.setWindowTitle('ICAL - Calibration Running')

                    progdlgHlpr = ProgressDlgHelper(rundlgHlpr.cmdline, rundlgHlpr.caldescr, rundlgHlpr.cal_time_mins, progdlg)
                    progdlgHlpr.setupUi(dlg)

                    if dlg.exec() == QtWidgets.QDialog.Accepted:
                        res = QtWidgets.QMessageBox().information(self.app_win, 'ICAL', 'Calibration Completed!', QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)
                    else:
                        res = QtWidgets.QMessageBox().warning(self.app_win, 'ICAL', 'Calibration canceled!', QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)

                else:
                    res = QtWidgets.QMessageBox().warning(self.app_win, 'ICAL', 'Calibration canceled!', QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)


    def run_cal_A_LF(self):
        self.run_cal_confirm('A', 'rblf')

    def run_cal_A_HF(self):
        self.run_cal_confirm('A', 'rbhf')

    def run_cal_B_LF(self):
        self.run_cal_confirm('B', 'rblf')

    def run_cal_B_HF(self):
        self.run_cal_confirm('B', 'rbhf')


    def MWSelectionChanged(self, seldelta, deseldelta):

        sel_ndxs = self.main_win.cfgListTV.selectedIndexes()

        if len(sel_ndxs) >= 1:
            self.cur_row = sel_ndxs[0].row()
            self.update_details(self.cur_row)
        else:
            self.cur_row = -1


        # self.ping_hosts()

    def update_details(self, row):

        self.main_win.editBtn.setEnabled(row != -1)
        self.set_run_btns_enabled(row)

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
