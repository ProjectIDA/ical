# import sip
import os
import shutil
import sys
import logging

from PyQt5 import QtGui, QtWidgets, QtCore, QtPrintSupport

from gui.mainwindow import *
from gui.mainwindow_helper import MainWindowHelper

from config.ical_config import IcalConfig
import config.pycal_globals as pcgl


class PyCalMainWindow(QtWidgets.QMainWindow):
    # not really necessary at this point.
    def __init__(self):
        super(PyCalMainWindow, self).__init__()


def initialize_app():

    # check for config dir
    if os.path.exists(pcgl.get_config_root()):
        cfg_success, cfg = load_cfg(pcgl.get_config_root())

    else:
        os.makedirs(os.path.join(pcgl.get_config_root(), 'etc'), exist_ok=True)
        cfg_success = False
        cfg = None

    # if config not read, need to seed config dir with initial config files
    if not cfg_success:
        # get ird of any existing config dir and re-init from app bundle
        if os.path.exists(pcgl.get_config_root()):
            shutil.rmtree(pcgl.get_config_root())
        # copy from internal config
        shutil.copytree(pcgl.get_initial_config_root(), pcgl.get_config_root())

        cfg_success, cfg = load_cfg(pcgl.get_config_root())

    # make sure there exists a results dir
    os.makedirs(os.path.join(pcgl.get_root(), 'Results'), exist_ok=True)

    return cfg_success, cfg


def load_cfg(cfg_root_path):
    success = False

    if os.path.exists(cfg_root_path):

        cfg = IcalConfig(cfg_root_path)
        success = cfg.load()
        if success:
            logging.info('PyCal configuration loaded from: ' + cfg_root_path)
        else:
            logging.error('Error loading PyCal configuration files from ' + cfg_root_path)
    else:
        cfg = None

    return success, cfg


if __name__ == '__main__':

    # need to get this done right away so log file can be written
    os.makedirs(pcgl.get_root(), exist_ok=True)

    logging.basicConfig(filename=pcgl.get_log_filename(),
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %I:%M:%S %Z')
    logging.info('*--------------------------------------------------------------------------------*')
    logging.info('PyCal Starting...')

    load_ok, cfg = initialize_app()

    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = PyCalMainWindow()

    main_win = Ui_MainWindow()
    main_win.setupUi(appMainWindow)

    main_win_hlpr = MainWindowHelper(cfg, appMainWindow, main_win)

    main_win_hlpr.setup_main_window()

    appMainWindow.show()

    if not load_ok:
        logging.error('Error loading configuration data.')
        QtWidgets.QMessageBox().critical(appMainWindow,
                                         'PyCal ERROR',
                                         'There was an error reading the PyCal configuration files. Check the pycal.log file for more information.',
                                         QtWidgets.QMessageBox().Close,
                                         QtWidgets.QMessageBox().Close)
        logging.info('PyCal Quitting.')
        logging.info('*--------------------------------------------------------------------------------*')
        sys.exit(1)
    # check 
    else:
        res = app.exec()
        logging.info('PyCal exited normally.')
        logging.info('*--------------------------------------------------------------------------------*')
        sys.exit(res)
