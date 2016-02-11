import os
import sys
import time
import argparse
import logging

from PyQt5 import QtGui, QtWidgets, QtCore

from gui.mainwindow import *
from gui.mainwindow_helper import MainWindowHelper #setup_main_window, setup_tableview

from config.ical_config import IcalConfig


class ICALMainWindow(QtWidgets.QMainWindow):
    # not really necessary at this point.
    def __init__(self):
        super(ICALMainWindow, self).__init__()



def has_config_dir(etcpath):
    fpath = os.path.abspath(etcpath)
    return (os.path.exists(fpath), fpath)


def load_cfg(argpath=None):

    success = False
    foundcfg = False
    cfg = None
    cfg_searched_paths = []

    # first check for cmd line 'root='
    if args.path != None:

        foundcfg, etcpath = has_config_dir(args.path)
        if foundcfg:
            cfg = IcalConfig(os.path.abspath(etcpath))
            success = cfg.load()
        else:
            cfg_searched_paths.append(etcpath)

    else:
        # path not on caommand line...
        # first check directory with ical executable
        # then user HOME dir
        if not foundcfg:
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc')
            foundcfg, etcpath = has_config_dir(fpath)

            if foundcfg:
                # cfg = IcalConfig(os.path.dirname(etcpath))
                cfg = IcalConfig(etcpath)
                success = cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

        if not foundcfg:
            foundcfg, etcpath = has_config_dir(os.path.expanduser('~/etc'))

            if foundcfg:
                cfg = IcalConfig(etcpath)
                success = cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

    if not foundcfg:
        success = False
        logging.error('Could not find ICAL configuration directory in these locations:\n' + '\n'.join(cfg_searched_paths))

    return (success, cfg)


if __name__ == '__main__':

    logging.basicConfig(filename='ical.log', 
        format='%(asctime)s %(levelname)s: %(message)s', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %I:%M:%S %Z')
    logging.info('*--------------------------------------------------------------------------------*')
    logging.info('ICAL Starting...')

    parser = argparse.ArgumentParser(description='ICAL Calibration Application.')
    parser.add_argument('-p', '--path', help='Local path to configuration files.')
    args = parser.parse_args()

    load_ok, cfg = load_cfg()


    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = ICALMainWindow()

    main_win = Ui_MainWindow()
    main_win.setupUi(appMainWindow)

    main_win_hlpr = MainWindowHelper(load_ok, cfg, appMainWindow, main_win)

    main_win_hlpr.setup_main_window()

    appMainWindow.show()

    if main_win_hlpr.check_cfg_load():
        res = app.exec()
        logging.info('ICAL Quit')
        sys.exit(res)
    else:
        logging.error('Error loading configuration data.')
        logging.info('ICAL Quit')
        sys.exit(1)

