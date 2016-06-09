#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################

import logging
import os.path
import sys
from os import makedirs, getcwd
from subprocess import call
from datetime import datetime, timezone
from PyQt5 import QtCore, QtWidgets, QtGui

import config.pycal_globals as pcgl
from config.ical_config import IcalConfig
from config.wrapper_cfg import WrapperCfg
import gui.mainwindow
from gui.about import Ui_AboutDlg
from gui.progress_dlg import Ui_ProgressDlg
from gui.progress_dlg_helper import ProgressDlgHelper
from gui.edit_dlg import Ui_EditDlg
from gui.edit_dlg_helper import EditDlgHelper
from gui.analysis_progress_window import Ui_AnalysisProgressFrm
from gui.analysis_progress_dlg_helper import AnalysisProgressDlgHelper
from gui.analysis_progress_dialog import ProgressDlg
from gui.logview_dlg import Ui_LogviewDlg
from gui.logview_dlg_helper import LogviewDlgHelper
from gui.cfg_data_model import CfgDataModel

from comms.ical_threads import QCalThread, QVerifyThread
from ida.ctbto.process import process_qcal_data
from ida.instruments import *


class MainWindowHelper(object):

    def __init__(self, cfg, app_win, main_win, app_root_dir):
        self.cfg = cfg
        self.cdm = CfgDataModel(self.cfg)
        self.app_win = app_win
        self.main_win = main_win
        self.cur_row = -1
        self.set_run_btns_enabled(self.cur_row)
        self.last_click = datetime.min
        self.main_win.q330Info.setText("")
        self.app_root_dir = app_root_dir
        self.test_set = dict()
        self.verbose_log = False
        self.qVerifyThread = None

        self.log_dlgHlpr = None

        self.test_set_action_group = QtWidgets.QActionGroup(app_win)
        self.test_set_action_group.addAction(self.main_win.actionUOSS_2016)
        self.test_set_action_group.addAction(self.main_win.actionAAK_2015)
        self.test_set_action_group.addAction(self.main_win.actionXPFO_2016)
        self.test_set_action_group.addAction(self.main_win.actionALE)
        self.test_set_action_group.addAction(self.main_win.actionERM)
        self.test_set_action_group.addAction(self.main_win.actionRPN)
        self.test_set_action_group.addAction(self.main_win.actionTAU)
        self.test_set_action_group.addAction(self.main_win.actionBORG)
        self.test_set_action_group.addAction(self.main_win.actionPFO_CTBTO)
        self.test_set_action_group.addAction(self.main_win.actionSHEMLYA)

    def setup_main_window(self):
        self.setup_actions()
        self.setup_tableview()

    def setup_actions(self):
        logging.debug('Setting up QActions')

        self.main_win.actionAbout_PyCal.triggered.connect(self.show_about)

        self.main_win.acViewLogMessages.triggered.connect(self.view_log_messages)

        self.main_win.quitBtn.clicked.connect(self.main_win.actionQuit.trigger)

        self.main_win.sensARunBtn.clicked.connect(self.run_cal_A)
        self.main_win.sensBRunBtn.clicked.connect(self.run_cal_B)

        self.main_win.addBtn.clicked.connect(self.main_win.actionNew.trigger)
        self.main_win.editBtn.addAction(self.main_win.actionEdit)

        self.main_win.actionNew.triggered.connect(self.AddCfg)
        self.main_win.actionEdit.triggered.connect(self.EditCfg)
        self.main_win.actionDelete.triggered.connect(self.delete_cfg)
        self.main_win.actionQuit.triggered.connect(self.close)
        self.main_win.actionVerbose_Log.triggered.connect(self.toggle_verbose)

        # self.main_win.testAnalysisBtn.clicked.connect(self.run_test_analysis)
        self.test_set_action_group.triggered.connect(self.set_test_set)


    def show_about(self):
        dlg = QtWidgets.QDialog(self.app_win)
        dlg.setModal(False)
        dlgUI = Ui_AboutDlg()
        dlgUI.setupUi(dlg)
        # dlg.setWindowTitle('PyCal - Log Viewer')
        # dlgHlpr = LogviewDlgHelper(pcgl.get_log_filename(), dlg, dlgUI)

        # self.log_dlgHlpr = dlgHlpr

        dlg.show()


    def toggle_verbose(self):

        self.verbose_log = not self.verbose_log

        if self.verbose_log:
            lvl = logging.disable(logging.NOTSET)
        else:
            lvl = logging.disable(logging.DEBUG)


    def set_test_set(self, action):

        if action == self.main_win.actionUOSS_2016:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'UOSS',
                'loc' : 'TT',
                'ip' : 'uoss10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-uoss10-sts2-rbhf-2016-0204-0612.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-uoss10-sts2-rbhf-2016-0204-0612.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-uoss10-sts2-rblf-2016-0204-0651.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-uoss10-sts2-rblf-2016-0204-0651.log'
            }
        elif  action == self.main_win.actionAAK_2015:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'AAK',
                'loc' : 'TT',
                'ip' : 'aak10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-aak10-sts2.5-rbhf-2015-0605-0610.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-aak10-sts2.5-rbhf-2015-0605-0610.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-aak10-sts2.5-rblf-2015-0605-0648.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-aak10-sts2.5-rblf-2015-0605-0648.log'
            }

        elif  action == self.main_win.actionXPFO_2016:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'XPFO',
                'loc' : '50',
                'ip' : '172.23.34.108',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-172.23.34.108-STS2_5-rbhf-2016-0602-2154.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-172.23.34.108-STS2_5-rbhf-2016-0602-2154.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-172.23.34.108-STS2_5-rblf-2016-0602-1718.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-172.23.34.108-STS2_5-rblf-2016-0602-1718.log'
            }

        elif  action == self.main_win.actionPFO_CTBTO:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'PFO',
                'loc' : 'TT',
                'ip' : '198.202.124.228',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-198.202.124.228-sts2.5-rbhf-2016-0511-1213.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-198.202.124.228-sts2.5-rbhf-2016-0511-1213.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-198.202.124.228-sts2.5-rblf-2016-0511-1249.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-198.202.124.228-sts2.5-rblf-2016-0511-1249.log'
            }

        elif  action == self.main_win.actionALE:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'ALE',
                'loc' : 'TT',
                'ip' : 'ale10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-ale10-sts2-rbhf-2015-0903-1826.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-ale10-sts2-rbhf-2015-0903-1826.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-ale10-sts2-rblf-2015-0903-1859.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-ale10-sts2-rblf-2015-0903-1859.log'
            }

        elif  action == self.main_win.actionBORG:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'BORG',
                'loc' : 'TT',
                'ip' : 'borg10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-borg10-sts2-rbhf-2015-1020-2358.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-borg10-sts2-rbhf-2015-1020-2358.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-borg10-sts2-rblf-2015-1021-0037.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-borg10-sts2-rblf-2015-1021-0037.log'
            }

        elif  action == self.main_win.actionERM:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'ERM',
                'loc' : 'TT',
                'ip' : 'erm10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-erm10-sts2-rbhf-2015-0819-0609.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-erm10-sts2-rbhf-2015-0819-0609.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-erm10-sts2-rblf-2015-0819-0647.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-erm10-sts2-rblf-2015-0819-0647.log'
            }

        elif  action == self.main_win.actionRPN:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'RPN',
                'loc' : 'TT',
                'ip' : 'rpn10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-rpn10-sts2.5-rbhf-2015-0701-0612.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-rpn10-sts2.5-rbhf-2015-0701-0612.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-rpn10-sts2.5-rblf-2015-0701-0650.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-rpn10-sts2.5-rblf-2015-0701-0650.log'
            }

        elif  action == self.main_win.actionTAU:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'TAU',
                'loc' : 'TT',
                'ip' : 'tau10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-tau10-sts2-rbhf-2016-0127-0622.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-tau10-sts2-rbhf-2016-0127-0622.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-tau10-sts2-rblf-2016-0127-0700.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-tau10-sts2-rblf-2016-0127-0700.log'
            }

        elif  action == self.main_win.actionSHEMLYA:
            self.test_set = {
                'seis_model' : SEISTYPE_STS25,
                'sta' : 'SHEM',
                'loc' : '',
                'ip' : 'shem10',
                'hf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-SHEMLYA-STS25_2016-05-25-HF.ms',
                'hf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-SHEMLYA-STS25_2016-05-25-HF.log',
                'lf_msfn' : '/Users/dauerbach/dev/ical/src/CAL-SHEMLYA-STS25_2016-05-25-LF.ms',
                'lf_logfn' : '/Users/dauerbach/dev/ical/src/CAL-SHEMLYA-STS25_2016-05-25-LF.log'
            }

    # CAL-SHEMLYA-STS25_2016-05-25-



    def setup_tableview(self): #MainWindow, mw_ui):
        logging.debug('Setting up QTableview')
        self.main_win.cfgListTV.setModel(self.cdm)
        hdrvw = self.main_win.cfgListTV.horizontalHeader()
        hdrvw.setStretchLastSection(True)
        self.main_win.cfgListTV.resizeColumnsToContents()
        self.main_win.cfgListTV.setSortingEnabled(False)
        self.main_win.cfgListTV.clicked.connect(self.record_click)
        self.main_win.cfgListTV.selectionModel().selectionChanged.connect(self.MWSelectionChanged)

        self.update_details(-1)


    def close(self):
        self.app_win.close()


    def view_log_messages(self):

        if self.log_dlgHlpr:
            dlg = self.log_dlgHlpr.qtDlg
            dlgUI = self.log_dlgHlpr.dlgUI
        else:
            dlg = QtWidgets.QDialog(self.app_win)
            dlg.setModal(False)
            dlgUI = Ui_LogviewDlg()
            dlgUI.setupUi(dlg)
            dlg.setWindowTitle('PyCal - Log Viewer')
            dlgHlpr = LogviewDlgHelper(pcgl.get_log_filename(), dlg, dlgUI)

            self.log_dlgHlpr = dlgHlpr

        dlg.show()


    def MWSelectionChanged(self, seldelta, deseldelta):
        sel_ndxs = self.main_win.cfgListTV.selectedIndexes()

        if len(sel_ndxs) >= 1:
            self.cur_row = sel_ndxs[0].row()

        else:
            self.cur_row = -1

        self.update_details(self.cur_row)

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
            logging.info('Editing configuration for Q330 with Tag # {}'.format(tagno))
            wcfg = self.cfg.find(tagno)
            if wcfg:

                dlg, dlgUI, dlgUIHlpr = self.setup_edit_dialog(EditDlgHelper.EDIT_MODE, wcfg.data)
                # need to keep dlgUIHlpr in scope for GUI callbacks
                if dlg.exec() == QtWidgets.QDialog.Accepted:
                    try:
                        self.cdm.UpdateCfg(wcfg.tagno(), dlgUI.new_cfg)
                        self.update_details(self.cur_row)
                        logging.debug('PyCal Q330 configuration updated.')
                    except Exception as e:
                        logging.error('Error saving PyCal Q330 config record. ' + str(e))
                        QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)

                    self.main_win.cfgListTV.resizeColumnsToContents()
                else:
                    logging.info('Editing cancelled by user.')

                dlg, dlgUI, dlgUIHlpr = None, None, None

        self.main_win.cfgListTV.resizeColumnsToContents()


    def delete_cfg(self):
        if self.cur_row >= 0:
            # get tagno and delete
            mdlNdx = QtCore.QAbstractItemModel.createIndex(self.cdm, self.cur_row, CfgDataModel.TAGNO_COL)
            tagno = self.cdm.data(mdlNdx, QtCore.Qt.DisplayRole)
            if tagno:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Warning)
                msg_box.setText('DELETE config for Q330 with Tag # {}?'.format(tagno))
                msg_box.setInformativeText('This is permanent!')
                msg_box.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                del_btn = msg_box.addButton("DELETE", QtWidgets.QMessageBox.DestructiveRole);
                cancel_btn = msg_box.addButton(QtWidgets.QMessageBox.Cancel);

                msg_box.exec()

                if msg_box.clickedButton() == del_btn:
                    logging.info('Deleting configuration for Q330 with Tag # {}'.format(tagno))
                    self.cfg.remove(tagno)
                    self.cdm.endResetModel()

        self.main_win.cfgListTV.resizeColumnsToContents()


    def AddCfg(self):
        logging.info('Adding new q330 configuration')

        dlg, dlgUI, dlgUIHlpr = self.setup_edit_dialog(EditDlgHelper.ADD_MODE, WrapperCfg.new_dict())
        # need to keep dlgUIHlpr in scope for GUI callbacks
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            try:
                self.cdm.AddCfg(dlgUI.new_cfg)
                logging.debug('New PyCal Q330 configuration saved.')
            except Exception as e:
                logging.error('Error saving new PyCal Q330 config record. ' + str(e))
                QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', str(e), QtWidgets.QMessageBox().Close, QtWidgets.QMessageBox().Close)
        else:
            logging.info('Add new configuration cancelled by user.')

        self.main_win.cfgListTV.resizeColumnsToContents()


    def run_analysis(self, method, *args):

        dlg = ProgressDlg()
        dlgUI = Ui_AnalysisProgressFrm()
        dlgUI.setupUi(dlg)
        dlg.setWindowTitle('PyCal - Data Analysis')
        dlgHlpr = AnalysisProgressDlgHelper(dlg, dlgUI)

        res, msg_fn, amppltfn, phapltfn = dlgHlpr.run_analysis(method, *args)
        if res == -1:
            logging.warning('Analysis canceled by user.')
        elif res == 0:
            logging.info('Analysis completed.')

        return res, msg_fn, amppltfn, phapltfn


    def run_test_analysis(self):

        QtWidgets.QMessageBox().information(self.app_win, 'PyCal Analysis',
                                                  'Calibration data acquired successfully.\n\n'
                                                  'The data will now be analyzed.\n'
                                                  'This could take approximately 5 minutes.',
                                                  QtWidgets.QMessageBox().Close,
                                                  QtWidgets.QMessageBox().Close)

        channel_codes = ComponentsTpl(north='BHN', east='BHE', vertical='BHZ')

        sensor = 'A'
        seis_model = SEISTYPE_STS25

        # sta = 'AS108'
        # loc = '10'
        # ip = '198.202.124.228'
        # hf_msfn  = 'CAL-198.202.124.228-sts2.5-rbhf-2016-0511-1213.ms'
        # hf_logfn = 'CAL-198.202.124.228-sts2.5-rbhf-2016-0511-1213.log'
        # lf_msfn  = 'CAL-198.202.124.228-sts2.5-rblf-2016-0511-1249.ms'
        # lf_logfn = 'CAL-198.202.124.228-sts2.5-rblf-2016-0511-1249.log'
        #
        # # XPFO "Fast" test
        # seis_model = 'sts2.5-F'
        # sta='XPFO'
        # ip = '172.23.34.108'
        # hf_msfn = 'CAL-172.23.34.108-sts2.5-F-rbhf-2016-0511-0838.ms'
        # hf_logfn = 'CAL-172.23.34.108-sts2.5-F-rbhf-2016-0511-0838.log'
        # lf_msfn = 'CAL-172.23.34.108-sts2.5-F-rblf-2016-0511-0836.ms'
        # lf_logfn = 'CAL-172.23.34.108-sts2.5-F-rblf-2016-0511-0836.log'
        #
        seis_model = self.test_set['seis_model']
        sta = self.test_set['sta']
        ip = self.test_set['ip']
        loc = self.test_set['loc']
        hf_msfn = self.test_set['hf_msfn']
        hf_logfn = self.test_set['hf_logfn']
        lf_msfn = self.test_set['lf_msfn']
        lf_logfn = self.test_set['lf_logfn']

        output_dir = os.path.join(pcgl.get_results_root(), '-'.join([sta, ip.replace('.','_'), sensor, seis_model]))

        if seis_model in SEISMOMETER_RESPONSES:
            if getattr(sys, 'frozen', False):
                bundle_dir = sys._MEIPASS
                full_paz_fn = os.path.abspath(os.path.join(bundle_dir, 'IDA', 'data', SEISMOMETER_RESPONSES[seis_model]['full_resp_file']))
            else:
                full_paz_fn = os.path.abspath(os.path.join('.', 'data', SEISMOMETER_RESPONSES[seis_model]['full_resp_file']))
        else:
            msg1 = 'PyCal does not have response information for SENSOR MODEL: ' + seis_model
            msg2 = 'Analysis can not be performed.'
            logging.error(msg1)
            logging.error(msg2)
            QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg1 + '\n' + msg2,
                                             QtWidgets.QMessageBox().Close,
                                             QtWidgets.QMessageBox().Close)
            return

        logging.info('Analysis starting...')
        logging.debug('Using FULL response at: ' + full_paz_fn)

        retcode, \
        ims_calres_txt_fn, \
        cal_amp_plot_fn, \
        cal_pha_plot_fn = self.run_analysis(process_qcal_data,
                                            sta,
                                            channel_codes,
                                            loc,
                                            output_dir,
                                            (lf_msfn, lf_logfn),
                                            (hf_msfn, hf_logfn),
                                            seis_model,
                                            full_paz_fn)

        if retcode == 0:
            call(['open', output_dir])
            call(['open', '-a', 'TextEdit', ims_calres_txt_fn])
            call(['open', cal_amp_plot_fn])
            call(['open', cal_pha_plot_fn])

            msg_list = ['Calibration completed successfully. ',
                        'The following files have been saved in directory:\n\n{}\n\n'.format(output_dir),
                        '{}:\n\n{}\n\n'.format('CALIBRATE_RESULT Msg', os.path.basename(ims_calres_txt_fn)),
                        '{}:\n\n{}\n\n'.format('Amplitude Response Plots', os.path.basename(cal_amp_plot_fn)),
                        '{}:\n\n{}'.format('Phase Response Plots', os.path.basename(cal_pha_plot_fn))]

            logging.info('The following files have been saved in directory: ' + output_dir)
            logging.info('   CALIBRATE_RESULT Msg: ' + os.path.basename(ims_calres_txt_fn))
            logging.info('   Amplitude Response Plots: ' + os.path.basename(cal_amp_plot_fn))
            logging.info('   Phase Response Plots: ' + os.path.basename(cal_pha_plot_fn))

            res = QtWidgets.QMessageBox().information(self.app_win, 'PyCal',
                                                      'Calibration Completed!\n\n' + ''.join(msg_list),
                                                      QtWidgets.QMessageBox().Close,
                                                      QtWidgets.QMessageBox().Close)

    def run_sensor_cal_type(self, sensor, caltype, cal_info):

        completed = False

        logging.info('Running {} calibration for sensor {} on q330 (hostname: {})'.format(caltype.upper(), sensor, cal_info['ip']))

        # create qcal thread
        qcal_thread = QCalThread(os.path.join(self.app_root_dir, pcgl.get_bin_root()),
                                 cal_info['cmd_line'][caltype],
                                 cal_info['output_dir'])

        dlg = QtWidgets.QDialog(self.app_win)
        progdlg = Ui_ProgressDlg()
        progdlg.setupUi(dlg)
        dlg.setWindowTitle('PyCal - Data Acquisition')

        if caltype == CALTYPE_RBLF:
            cal_descr = 'Calibration Signal: LOW Frequency Random Binary\n\n' + cal_info['cal_descr']
        elif caltype == CALTYPE_RBHF:
            cal_descr = 'Calibration Signal: HIGH Frequency Random Binary\n\n' + cal_info['cal_descr']
        else:
            msg = 'Invalid CALIBRATION TYPE:' + caltype
            logging.error(msg)
            QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg,
                                             QtWidgets.QMessageBox().Close,
                                             QtWidgets.QMessageBox().Close)
            return False, None

        progdlgHlpr = ProgressDlgHelper(dlg, cal_descr, cal_info['cal_time'][caltype], progdlg, qcal_thread)
        progdlgHlpr.start()

        if (dlg.exec() == QtWidgets.QDialog.Accepted) and (progdlgHlpr.retcode == 0):
            completed = True
            msg = 'Calibration completed successfully. Miniseed file saved: {}'.format(progdlgHlpr.calmsfn)
            logging.info(msg)
            # res = QtWidgets.QMessageBox().information(self.app_win, 'PyCal',
            #                                           'Calibration Completed!\n\n' + progdlgHlpr.msg,
            #                                           QtWidgets.QMessageBox().Close,
            #                                           QtWidgets.QMessageBox().Close)

        else:
            completed = False
            msg1 = 'Calibration failed with exit code: {}'.format(progdlgHlpr.retcode)
            msg2 = 'Calibration failed with message: {}'.format(progdlgHlpr.msg)
            logging.error(msg1)
            logging.error(msg2)
            res = QtWidgets.QMessageBox().critical(self.app_win, 'PyCal', msg2,
                                                  QtWidgets.QMessageBox().Close,
                                                  QtWidgets.QMessageBox().Close)

        return completed, progdlgHlpr.calmsfn


    def run_sensor_cal(self, sensor):

        if (self.cur_row < 0):
            msg = 'No Q330 has been seleceted'
            logging.info(msg)
            res = QtWidgets.QMessageBox().warning(self.app_win, 'PyCal', msg,
                                                  QtWidgets.QMessageBox().Close,
                                                  QtWidgets.QMessageBox().Close)
        else:
            wcfg = self.cfg[self.cur_row]

            if sensor not in ['A', 'B']:
                msg = 'Invalid sensor can not be calibrated:' + sensor
                logging.error(msg)
                raise Exception(msg)

            if sensor == 'A':
                seis_model = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A]
                sensor_descr = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A]
                chancodes = wcfg.data[WrapperCfg.WRAPPER_KEY_CHANNELS_A]
                loc = wcfg.data[WrapperCfg.WRAPPER_KEY_LOCATION_A]
            elif sensor == 'B':
                seis_model = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B]
                sensor_descr = wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B]
                chancodes = wcfg.data[WrapperCfg.WRAPPER_KEY_CHANNELS_B]
                loc = wcfg.data[WrapperCfg.WRAPPER_KEY_LOCATION_B]

            # lets just make sure sensor in CTBTO supported list
            # should never get here is cfg files deployed correctly
            if seis_model not in CTBTO_SEIS_MODELS:
                msg = 'PyCal UNSUPPORTED SENSOR MODEL: ' + seis_model
                logging.error(msg)
                QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg,
                                             QtWidgets.QMessageBox().Close,
                                             QtWidgets.QMessageBox().Close)
                return

            lf_calib = self.cfg.find_calib(seis_model + '|' + CALTYPE_RBLF)
            hf_calib = self.cfg.find_calib(seis_model + '|' + CALTYPE_RBHF)

            if (not lf_calib) or (not hf_calib):
                msg = 'Calib Record missing for sensor [{}].'.format(seis_model)
                logging.error(msg)
                QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg,
                                                 QtWidgets.QMessageBox().Close,
                                                 QtWidgets.QMessageBox().Close)
                return

            sta = wcfg.data[WrapperCfg.WRAPPER_KEY_STA]
            ip = wcfg.data[WrapperCfg.WRAPPER_KEY_IP]

            output_dir = os.path.join(pcgl.get_results_root(), '-'.join([sta, ip.replace('.', '_'), sensor, seis_model]))
            makedirs(output_dir, mode=0o744, exist_ok=True)


            cal_descr = '{:>11} : {:<6} at {}'.format('Q330 Tag#', wcfg.data[WrapperCfg.WRAPPER_KEY_TAGNO], ip)
            cal_descr += '\n{:>11} : {} (Sensor {})'.format('Sensor', sensor_descr, sensor)
            cal_descr += '\n{:>11} : {}'.format('Station', wcfg.data[WrapperCfg.WRAPPER_KEY_STA])
            cal_descr += '\n{:>11} : {}'.format('Loc', loc)
            cal_descr += '\n{:>11} : {}'.format('Chan Codes', chancodes)

            tot_cal_time = lf_calib.cal_time_min() + hf_calib.cal_time_min()

            cal_info = {
                'sta' : sta,
                'loc' : loc,
                'chancodes' : chancodes,
                'ip' : ip,
                'seis_model' : seis_model,
                'cal_descr': cal_descr,
                'cal_tot_time_mins': tot_cal_time,
                'cal_time' : {
                    CALTYPE_RBLF : lf_calib.cal_time_min(),
                    CALTYPE_RBHF : hf_calib.cal_time_min(),
                },
                'cmd_line' : {
                    CALTYPE_RBHF : wcfg.gen_qcal_cmdline(sensor, CALTYPE_RBHF) + ' root=' + self.cfg.root_dir,
                    CALTYPE_RBLF : wcfg.gen_qcal_cmdline(sensor, CALTYPE_RBLF) + ' root=' + self.cfg.root_dir
                },
                'output_dir': output_dir
            }

            logging.debug('cal_info:' + str(cal_info))

            success, lf_msfn = self.run_sensor_cal_type(sensor, CALTYPE_RBLF, cal_info)
            if success:
                lf_logfn = os.path.splitext(lf_msfn)[0] + '.log'
                logging.info('QCal RBLF Miniseed file saved: ' + os.path.join(output_dir, lf_msfn))
                logging.info('QCal RBLF Log file saved: ' + os.path.join(output_dir, lf_logfn))

                success, hf_msfn = self.run_sensor_cal_type(sensor, CALTYPE_RBHF, cal_info)
                if success:
                    chancodeslst = chancodes.split(',')
                    channel_codes = ComponentsTpl(vertical=chancodeslst[0], north=chancodeslst[1], east=chancodeslst[2])

                    hf_logfn = os.path.splitext(hf_msfn)[0] + '.log'
                    logging.info('QCal RBHF Miniseed file saved: ' + os.path.join(output_dir, hf_msfn))
                    logging.info('QCal RBHF Log file saved: ' + os.path.join(output_dir, hf_logfn))

                    QtWidgets.QMessageBox().information(self.app_win, 'PyCal Analysis Phase Starting',
                                                        'Calibration data acquired successfully.\n\n'
                                                        'The data will now be analyzed.\n'
                                                        'This could take approximately 5 minutes.',
                                                        QtWidgets.QMessageBox().Close,
                                                        QtWidgets.QMessageBox().Close)

                    if seis_model in SEISMOMETER_RESPONSES:
                        if getattr(sys, 'frozen', False):
                            bundle_dir = sys._MEIPASS
                            full_paz_fn = os.path.abspath(os.path.join(bundle_dir,
                                                                       'IDA',
                                                                       'data',
                                                                       SEISMOMETER_RESPONSES[seis_model]['full_resp_file']))
                        else:
                            full_paz_fn = os.path.abspath(os.path.join('.',
                                                                       'data',
                                                                       SEISMOMETER_RESPONSES[seis_model]['full_resp_file']))
                    else:
                        msg1 = 'PyCal does not have response information for SENSOR MODEL: ' + seis_model
                        msg2 = 'Analysis can not be performed.'
                        logging.error(msg1)
                        logging.error(msg2)
                        QtWidgets.QMessageBox().critical(self.app_win, 'PyCal ERROR', msg1 + '\n' + msg2,
                                                         QtWidgets.QMessageBox().Close,
                                                         QtWidgets.QMessageBox().Close)
                        return

                    logging.info('Analysis starting...')
                    logging.debug('Using FULL response at: ' + full_paz_fn)

                    retcode, \
                    ims_calres_txt_fn, \
                    cal_amp_plot_fn, \
                    cal_pha_plot_fn = self.run_analysis(process_qcal_data,
                                                        sta,
                                                        channel_codes,
                                                        loc,
                                                        output_dir,
                                                        (lf_msfn, lf_logfn),
                                                        (hf_msfn, hf_logfn),
                                                        seis_model,
                                                        full_paz_fn)

                    if retcode == 0:
                        msg_list = ['Calibration completed successfully. ',
                                    'The following files have been saved in directory:\n\n{}\n\n'.format(output_dir),
                                    '{}:\n\n{}\n\n'.format('CALIBRATE_RESULT Msg', os.path.basename(ims_calres_txt_fn)),
                                    '{}:\n\n{}\n\n'.format('Amplitude Response Plots', os.path.basename(cal_amp_plot_fn)),
                                    '{}:\n\n{}'.format('Phase Response Plots', os.path.basename(cal_pha_plot_fn))]

                        logging.info('Analysis phase completed with return code: {}'.format(retcode))
                        logging.info('The following files have been saved in directory: ' + output_dir)
                        logging.info('  {} {}'.format('CALIBRATE_RESULT Msg: ', os.path.basename(ims_calres_txt_fn)))
                        logging.info('  {} {}'.format('Amplitude Response Plots: ', os.path.basename(cal_amp_plot_fn)))
                        logging.info('  {} {}'.format('Phase Response Plots: ', os.path.basename(cal_pha_plot_fn)))

                        res = QtWidgets.QMessageBox().information(self.app_win, 'PyCal',
                                                                  'Calibration Completed!\n\n' + ''.join(msg_list),
                                                                  QtWidgets.QMessageBox().Close,
                                                                  QtWidgets.QMessageBox().Close)

                        now_str = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
                        if sensor == 'A':
                            wcfg.update({ wcfg.WRAPPER_KEY_LAST_CAL_A : now_str })
                        else:  # must be 'B'
                            wcfg.update({ wcfg.WRAPPER_KEY_LAST_CAL_B : now_str })
                        self.cfg.save()

                        self.update_details(self.cur_row)

                        call(['open', output_dir])
                        call(['open', ims_calres_txt_fn])
                        call(['open', cal_amp_plot_fn])
                        call(['open', cal_pha_plot_fn])
                    else:
                        logging.warning('Analysis phase completed with return code: {}'.format(retcode))
            else:
                logging.error("Unable to complete calibration")


    def run_cal_A(self):
        self.run_sensor_cal('A')


    def run_cal_B(self):
        self.run_sensor_cal('B')


    def update_details(self, row):

        self.main_win.editBtn.setEnabled(row != -1)
        self.main_win.actionEdit.setEnabled(row != -1)
        self.main_win.actionDelete.setEnabled(row != -1)

        self.set_run_btns_enabled(row)

        if self.qVerifyThread:
            self.qVerifyThread.cancel()
            self.qVerifyThread = None

        if row == -1:
            self.clear_details()
            if self.qVerifyThread:
                self.qVerifyThread.qVerifyQueryResult.disconnect(self.qVerify_query_result_slot)
                self.qVerifyThread.exit(-1)
        else:
            self.set_details(row)
            if self.qVerifyThread:
                self.qVerifyThread.start()


    def set_run_btns_enabled(self, row):

        if (row == -1):
            self.main_win.sensARunBtn.setEnabled(False)
            self.main_win.sensBRunBtn.setEnabled(False)
        else:
            wcfg = self.cfg[self.cur_row]
            self.main_win.sensARunBtn.setEnabled(
                wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] != WrapperCfg.WRAPPER_KEY_NONE
            )
            self.main_win.sensBRunBtn.setEnabled(
                wcfg.data[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] != WrapperCfg.WRAPPER_KEY_NONE
            )


    def qVerify_query_result_slot(self, host, port, ret_status, results):

        logging.debug('QVerify retcode: ' + str(ret_status))
        if ret_status == 0:
            act_ports = results.split()[7:]
            if port in act_ports:
                self.main_win.ipLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
                self.main_win.q330Info.setStyleSheet("QLabel{color:rgb(0, 102, 0);}")
                self.main_win.q330Info.setText('Q330 (Tag #: {}) is reachable and ready to rumble. '
                                               '(Q330 firmware versions: {})'.format(self.main_win.tagnoLE.text(),
                                                                                     '/'.join(results.split()[3:5])))
            else:
                self.main_win.sensARunBtn.setEnabled(False)
                self.main_win.sensARunBtn.setEnabled(False)
                self.main_win.sensBRunBtn.setEnabled(False)
                self.main_win.sensBRunBtn.setEnabled(False)
                self.main_win.ipLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
                self.main_win.q330Info.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
                self.main_win.q330Info.setText(
                    'Q330 (Tag #: {}) is reachable but the configured [{}] Data Port is not '
                    'in the list of Active Channels: [{}].'.format(
                        self.main_win.tagnoLE.text(),
                        port,
                        ', '.join(act_ports)
                    )
                )

        else:
            self.main_win.sensARunBtn.setEnabled(False)
            self.main_win.sensARunBtn.setEnabled(False)
            self.main_win.sensBRunBtn.setEnabled(False)
            self.main_win.sensBRunBtn.setEnabled(False)
            self.main_win.ipLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            self.main_win.q330Info.setStyleSheet("QLabel{color:rgb(179, 0, 0);}")
            self.main_win.q330Info.setText("Error: " + results)

        self.qVerifyThread = None


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
        self.main_win.sensALastCalLE.setText('')

        self.main_win.sensBDescrLE.setPlainText('')
        self.main_win.sensBMonPortLE.setText('')
        self.main_win.sensBLastCalLE.setText('')

        self.main_win.q330Info.setText('')


    def set_details(self, cfg_ndx):

        cfg = self.cfg[cfg_ndx]

        self.main_win.q330Info.setText("")

        # start thread to check IP/HOST availability, staus with qverify
        if self.qVerifyThread:
            self.qVerifyThread.cancel()

        self.qVerifyThread = QVerifyThread(cfg.data[WrapperCfg.WRAPPER_KEY_IP],
                                     cfg.data[WrapperCfg.WRAPPER_KEY_DATAPORT],
                                     pcgl.get_bin_root(),
                                     pcgl.get_config_root())

        self.qVerifyThread.qVerifyQueryResult.connect(self.qVerify_query_result_slot)

        self.main_win.netLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_NET])
        self.main_win.staLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_STA])
        self.main_win.ipLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_IP])
        self.main_win.tagnoLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_TAGNO])
        self.main_win.snLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_SN])
        self.main_win.dpLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DATAPORT])
        self.main_win.dpauthLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_DP1_AUTH])

        self.main_win.sensADescrLE.setPlainText(cfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A])
        if cfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A].lower() == WrapperCfg.WRAPPER_KEY_NONE:
            self.main_win.sensAMonPortLE.setText('')
            self.main_win.sensALastCalLE.setText('')
        else:
            self.main_win.sensAMonPortLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_A])
            self.main_win.sensALastCalLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_CAL_A])

        self.main_win.sensBDescrLE.setPlainText(cfg.data[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B])
        if cfg.data[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B].lower() == WrapperCfg.WRAPPER_KEY_NONE:
            self.main_win.sensBMonPortLE.setText('')
            self.main_win.sensBLastCalLE.setText('')
        else:
            self.main_win.sensBMonPortLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_MONPORT_B])
            self.main_win.sensBLastCalLE.setText(cfg.data[WrapperCfg.WRAPPER_KEY_LAST_CAL_B])

