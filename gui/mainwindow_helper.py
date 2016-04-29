import logging
import os.path
import sys
from os import makedirs, getcwd
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui

import config.pycal_globals as pcgl
from comms.ical_threads import PingThread, Q330Thread, QCalThread
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

from ida.calibration.process import process_qcal_data
import ida.seismometers


class MainWindowHelper(object):

    def __init__(self, cfg, app_win, main_win, app_root_dir):
        self.cfg = cfg
        self.cdm = CfgDataModel(self.cfg)
        self.app_win = app_win
        self.main_win = main_win
        self.cur_row = -1
        self.set_run_btns_enabled(self.cur_row)
        self.last_click = datetime.min
        self.main_win.q330NetworkStatus.setText("")
        self.main_win.q330Info.setText("")
        self.app_root_dir = app_root_dir


    def setup_main_window(self):
        self.setup_actions()
        self.setup_tableview()

    def setup_actions(self):
        self.main_win.acViewLogMessages.triggered.connect(self.view_log_messages)
        self.main_win.quitBtn.clicked.connect(self.main_win.actionQuit.trigger)

        self.main_win.sensARunLFBtn.clicked.connect(self.run_cal_A)
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
        dlgHlpr = LogviewDlgHelper(pcgl.get_log_filename(), dlg, dlgUI)

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
            dlg.setWindowTitle('PyCal - Edit Configuration')
        elif edit_mode == EditDlgHelper.ADD_MODE:
            dlg.setWindowTitle('PyCal - Add New Configuration')

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
                        QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)

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
                QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)

            self.main_win.cfgListTV.resizeColumnsToContents()


    def run_cal_confirm(self, sensor, caltype):

        completed = False
        sensor = sensor.upper()
        caltype = caltype.lower()
        output_dir = ''
        output_msfn = ''

        if self.cur_row >= 0:
            wcfg = self.cfg[self.cur_row]
            sens_name = ''
            if wcfg:
                # need to get calib obj to estimate cal time
                if sensor == 'A':
                    sens_name = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A]
                    sensor_descr = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A]
                    chancodes =  'BH1,BH2,BHZ' #wcfg.data[WrapperCfg.WRAPPER_KEY_CHANCODES_A]
                    loc = '50' # wcfg.data[WrapperCfg.WRAPPER_KEY_LOC_A]
                elif sensor == 'B':
                    sens_name = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B]
                    sensor_descr = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B]
                    chancodes =  'BH1,BH2,BHZ' #wcfg.data[WrapperCfg.WRAPPER_KEY_CHANCODES_A]
                    loc = '50' # wcfg.data[WrapperCfg.WRAPPER_KEY_LOC_B]
                else:
                    msg = 'Invalid A/B sensor: {}'.format(sensor)
                    logging.error(msg)
                    QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg,
                                                     QtWidgets.QMessageBox().Close,
                                                     QtWidgets.QMessageBox().Close)
                    raise Exception(msg)

                calib = self.cfg.find_calib(sens_name + '|' + caltype)

                if not calib:
                    msg = 'Calib Record not Found for sensor [{}] and caltype [{}].'.format(sens_name, caltype)
                    logging.error(msg)
                    QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg,
                                                     QtWidgets.QMessageBox().Close,
                                                     QtWidgets.QMessageBox().Close)
                    raise Exception(msg)

                sta = wcfg.data[WrapperCfg.WRAPPER_KEY_STA]
                ip = wcfg.data[WrapperCfg.WRAPPER_KEY_IP]
                output_dir = os.path.join(pcgl.get_results_root(), '-'.join([sta, ip.replace('.', '_'), sensor, sens_name]))
                makedirs(output_dir, mode=0o744, exist_ok=True)

                cal_descr =  '{:>11} : {:<6} at {}'.format('Q330 Tag#', wcfg.data[WrapperCfg.WRAPPER_KEY_TAGNO], ip)
                cal_descr += '\n{:>11} : {} (Sensor {})'.format('Sensor', sensor_descr, sensor)
                cmd_line = wcfg.gen_qcal_cmdline(sensor, caltype) + ' root=' + self.cfg.root_dir

                dlg = QtWidgets.QDialog(self.app_win)
                rundlg = Ui_RunDlg()
                rundlg.setupUi(dlg)
                dlg.setWindowTitle('PyCal - Run Calibration Confirmation')
                rundlgHlpr = RunDlgHelper(rundlg, cal_descr, calib.cal_time_min(), cmd_line)
                rundlgHlpr.setup_ui(dlg)

                # if dlg.exec() == QtWidgets.QDialog.Accepted:

                dlg = QtWidgets.QDialog(self.app_win)
                progdlg = Ui_ProgressDlg()
                progdlg.setupUi(dlg)
                dlg.setWindowTitle('PyCal - Calibration Running')

                # create qcal thread
                qcal_thread = QCalThread(os.path.join(self.app_root_dir, pcgl.get_bin_root()), cmd_line, output_dir)

                progdlgHlpr = ProgressDlgHelper(dlg, cal_descr, calib.cal_time_min(), progdlg, qcal_thread)
                progdlgHlpr.start()

                if (dlg.exec() == QtWidgets.QDialog.Accepted) and (progdlgHlpr.retcode == 0):
                    output_msfn = progdlgHlpr.calmsfn
                    completed = True
                    msg = 'Calibration completed successfully. Miniseed file saved: {}'.format(progdlgHlpr.calmsfn)
                    logging.info(msg)
                    res = QtWidgets.QMessageBox().information(self.app_win, 'PyCal',
                                                              'Calibration Completed!\n\n' + progdlgHlpr.msg,
                                                              QtWidgets.QMessageBox().Close,
                                                              QtWidgets.QMessageBox().Close)

                else:
                    msg1 = 'Calibration failed with exit code: {}'.format(progdlgHlpr.retcode)
                    msg2 = 'Calibration failed with message: {}'.format(progdlgHlpr.msg)
                    logging.error(msg1)
                    logging.error(msg2)
                    res = QtWidgets.QMessageBox().warning(self.app_win, 'PyCal', msg2,
                                                          QtWidgets.QMessageBox().Close,
                                                          QtWidgets.QMessageBox().Close)

        return completed, output_dir, output_msfn, sens_name, sta, chancodes, loc


    def run_cal_A(self):
        success, output_dir, lf_msfn, seis_model, sta, chancodes, loc = self.run_cal_confirm('A', 'rblf')
        if success:
            success, output_dir, hf_msfn, seis_model, _, _, _ = self.run_cal_confirm('A', 'rbhf')
            if success:
                chancodeslst = chancodes.split(',')
                channel_codes = ida.seismometers.ChanCodesTpl(chancodeslst[0], chancodeslst[1], chancodeslst[2])
                lf_logfn = os.path.splitext(lf_msfn)[0] + '.log'
                hf_logfn = os.path.splitext(hf_msfn)[0] + '.log'
                print('LF data: ',
                      os.path.join(output_dir, lf_msfn),
                      os.path.exists(os.path.join(output_dir, lf_msfn)),
                      os.path.exists(os.path.join(output_dir, lf_logfn))
                      )
                print('HF data: ',
                      os.path.join(output_dir, hf_msfn),
                      os.path.exists(os.path.join(output_dir, hf_msfn)),
                      os.path.exists(os.path.join(output_dir, hf_logfn))
                      )

                # Calibrations completed successfully.
                # you may disconnect from network
                #
                # prompt to continue with analysis
                #
                # get initial component independent response

                if 'MacOS' in getcwd():
                    resp_fpath = os.path.abspath(os.path.join('.', 'IDA', 'data', 'nom_resp_sts2_5.ida'))
                else:  # DEBUG...
                    resp_fpath = os.path.abspath(os.path.join('.', 'data', 'nom_resp_sts2_5.ida'))


                ida.calibration.process_qcal_data(sta, channel_codes, loc,
                                                  output_dir,
                                                 (lf_msfn, lf_logfn),
                                                 (hf_msfn, hf_logfn),
                                                 seis_model.upper(),
                                                 resp_fpath)




    def run_cal_A_LF(self):
        lf_output_dir, lf_msfn = self.run_cal_confirm('A', 'rblf')

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

        self.main_win.netLE.setText('')
        self.main_win.staLE.setText('')
        self.main_win.ipLE.setText('')
        self.main_win.tagnoLE.setText('')
        self.main_win.snLE.setText('')
        self.main_win.dpLE.setText('')
        self.main_win.dpauthLE.setText('')

        self.main_win.sensADescrLE.setPlainText('')
        self.main_win.sensAMonPortLE.setText('')
        self.main_win.sensALastLFLE.setText('')
        self.main_win.sensALastHFLE.setText('')

        self.main_win.sensBDescrLE.setPlainText('')
        self.main_win.sensBMonPortLE.setText('')
        self.main_win.sensBLastLFLE.setText('')
        self.main_win.sensBLastHFLE.setText('')


    def set_details(self, cfg_ndx):

        cfg = self.cfg[cfg_ndx]

        self.main_win.q330NetworkStatus.setText("")
        self.main_win.q330Info.setText("")

        # start thread to check IP/HOST availability
        self.pingThread = PingThread(cfg.data[WrapperCfg.WRAPPER_KEY_IP])
        self.pingThread.pingResult.connect(self.ping_result_slot)

        # start thread to get TAGNO and Firmware Vers
        self.q330Thread = Q330Thread(cfg.data[WrapperCfg.WRAPPER_KEY_IP],
                                     'id',
                                     pcgl.get_bin_root(),
                                     pcgl.get_config_root())

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

