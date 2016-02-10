import os
import sys
import time
import argparse

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
    warns = []
    errs = []

    # first check for cmd line 'root='
    if args.path != None:

        foundcfg, etcpath = has_config_dir(args.path)
        if foundcfg:
            cfg = IcalConfig(os.path.abspath(etcpath))
            success, errs = cfg.load()
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
                success, errs = cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

        if not foundcfg:
            foundcfg, etcpath = has_config_dir(os.path.expanduser('~/etc'))

            if foundcfg:
                cfg = IcalConfig(etcpath)
                success, errs = cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

    if not foundcfg:

        success = False
        errs.append('ERROR: Could not find configuration dir:\n' + '\n'.join(cfg_searched_paths))


    return (success, cfg, errs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ICAL Calibration Application.')
    parser.add_argument('-p', '--path', help='Local path to configuration files.')
    args = parser.parse_args()

    load_ok, cfg, errs = load_cfg()


    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = ICALMainWindow()

    main_win = Ui_MainWindow()
    main_win.setupUi(appMainWindow)

    main_win_hlpr = MainWindowHelper(load_ok, cfg, errs, appMainWindow, main_win)

    main_win_hlpr.setup_main_window()

    appMainWindow.show()

    if main_win_hlpr.check_cfg_load():
        sys.exit(app.exec_())
    else:
        sys.exit(1)

