import logging
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui

from comms.ical_threads import PingThread, Q330Thread
import gui.mainwindow
from gui.run_dlg import Ui_RunDlg
from gui.run_dlg_helper import RunDlgHelper
from gui.progress_dlg import Ui_ProgressDlg
from gui.progress_dlg_helper import ProgressDlgHelper
from gui.edit_dlg import Ui_EditDlg
from gui.edit_dlg_helper import EditDlgHelper
from gui.logview_dlg import Ui_LogviewDlg
from gui.logview_dlg_helper import LogviewDlgHelper
from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg
from gui.cfg_data_model import CfgDataModel

class MainWindowHelper(object):

    def __init__(self, load_ok, cfg, app_win, main_win):
        self.cfg_load_ok = load_ok
        self.cfg = cfg
        self.cdm = CfgDataModel(self.cfg)
        self.app_win = app_win
        self.main_win = main_win
        self.cur_row = -1
        self.set_run_btns_enabled(self.cur_row)
        self.last_click = datetime.min
        self.main_win.q330NetworkStatus.setText("")
        self.main_win.q330Info.setText("")


    def check_cfg_load(self):
        if not self.cfg_load_ok:
            QtWidgets.QMessageBox().critical(self.app_win, 
                'ICAL ERROR', 
                'There was an error reading the ICAL configuration files. Check the ical.log file for more information.', 
                QtWidgets.QMessageBox().Close, 
                QtWidgets.QMessageBox().Close)
            return False
        else:
            return True


    def setup_main_window(self):
        self.setup_actions()
        self.setup_tableview()


    def setup_actions(self):
        self.main_win.acViewLogMessages.triggered.connect(self.view_log_messages)
        self.main_win.quitBtn.clicked.connect(self.main_win.actionQuit.trigger)

        self.main_win.sensARunLFBtn.clicked.connect(self.run_cal_A_LF)
        self.main_win.sensARunHFBtn.clicked.connect(self.run_cal_A_HF)
        self.main_win.sensBRunLFBtn.clicked.connect(self.run_cal_B_LF)
        self.main_win.sensBRunHFBtn.clicked.connect(self.run_cal_B_HF)

        self.main_win.addBtn.clicked.connect(self.AddCfg)
        self.main_win.editBtn.clicked.connect(self.EditCfg)

        self.main_win.actionQuit.triggered.connect(self.close)


    def setup_tableview(self): #MainWindow, mw_ui):
        self.main_win.cfgListTV.setModel(self.cdm)
        hdrvw = self.main_win.cfgListTV.horizontalHeader()
        hdrvw.setStretchLastSection(True)
        self.main_win.cfgListTV.resizeColumnsToContents()
        self.main_win.cfgListTV.setSortingEnabled(False)
        self.main_win.cfgListTV.clicked.connect(self.record_click)
        self.main_win.cfgListTV.selectionModel().selectionChanged.connect(self.MWSelectionChanged)


    def close(self):
        self.app_win.close()


    def view_log_messages(self):
        dlg = QtWidgets.QDialog()
        dlgUI = Ui_LogviewDlg()
        dlgUI.setupUi(dlg)
        dlgHlpr = LogviewDlgHelper('ical.log', dlg, dlgUI)

        dlg.exec()


    def MWSelectionChanged(self, seldelta, deseldelta):
        sel_ndxs = self.main_win.cfgListTV.selectedIndexes()

        if len(sel_ndxs) >= 1:
            self.cur_row = sel_ndxs[0].row()
            self.update_details(self.cur_row)
        else:
            self.cur_row = -1


    def record_click(self):
        gap = datetime.now() - self.last_click
        self.last_click = datetime.now()
        if (gap.seconds + gap.microseconds/10.0**6) < 0.25:
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
            logging.info('Editing configuration for q330 tagno=' + str(tagno))
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
        logging.info('Editing new q330 configuration')

        dlg, dlgUI, dlgUIHlpr = self.setup_edit_dialog(EditDlgHelper.ADD_MODE, WrapperCfg.new_dict())
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

                    if (dlg.exec() == QtWidgets.QDialog.Accepted) and (progdlgHlpr.retcode == 0):
                        res = QtWidgets.QMessageBox().information(self.app_win, 'ICAL', 'Calibration Completed!\n\n' + progdlgHlpr.msg, QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)
                    else:
                        res = QtWidgets.QMessageBox().warning(self.app_win, 'ICAL', 'Calibration failed with exit code: ' + str(progdlgHlpr.retcode) + '\n' + progdlgHlpr.msg, QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)


    def run_cal_A_LF(self):
        self.run_cal_confirm('A', 'rblf')

    def run_cal_A_HF(self):
        self.run_cal_confirm('A', 'rbhf')

    def run_cal_B_LF(self):
        self.run_cal_confirm('B', 'rblf')

    def run_cal_B_HF(self):
        self.run_cal_confirm('B', 'rbhf')


    def update_details(self, row):

        self.main_win.editBtn.setEnabled(row != -1)
        self.set_run_btns_enabled(row)

        if row == -1:
            self.clear_details()
        else:
            self.set_details(row)

        if self.pingThread:
            self.pingThread.start()


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


    def ping_result_slot(self, host, up_status, ping_time):
        if up_status:
            self.main_win.ipLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
            self.main_win.q330NetworkStatus.setStyleSheet("QLabel{color:rgb(0, 102, 0);}")
            self.main_win.q330NetworkStatus.setText('Q330 is reachable. Ping: ' + ping_time)

            self.q330Thread.start()
        else:
            self.main_win.ipLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            self.main_win.q330NetworkStatus.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
            self.main_win.q330NetworkStatus.setText('Q330 is Unreachable, no ping response.')
            self.main_win.q330Info.setText("")


    def q330_query_result_slot(self, host, ret_status, results):
        if ret_status == 0:
            self.main_win.q330Info.setText('Firmware: ' + '/'.join(results.split()[-2:]))
        else:
            self.main_win.q330Info.setText("Q330 Error: " + results)


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

        self.main_win.q330NetworkStatus.setText("")
        self.main_win.q330Info.setText("")

        # start thread to check IP/HOST availability
        self.pingThread = PingThread(cfg.data[WrapperCfg.WRAPPER_KEY_IP])
        self.pingThread.pingResult.connect(self.ping_result_slot)

        # start thread to get TAGNO and Firmware Vers
        self.q330Thread = Q330Thread(cfg.data[WrapperCfg.WRAPPER_KEY_IP], 'id')
        self.q330Thread.q330QueryResult.connect(self.q330_query_result_slot)

        self.main_win.netLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_NET])
        self.main_win.staLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_STA])
        self.main_win.ipLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_IP])
        self.main_win.tagnoLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_TAGNO])
        self.main_win.snLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_SN])
        self.main_win.dpLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DATAPORT])
        self.main_win.dpauthLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DP1_AUTH])

        self.main_win.q330NetworkStatus.setText('')

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

