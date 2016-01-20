import os
import sys
import argparse

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.iCalGui.mainwindow import *
from gui.iCalGui.mainwindow_helper import MainWindowHelper #setup_main_window, setup_tableview

from config.ical_config import IcalConfig


def has_config_dir(path):
    fpath = os.path.abspath(os.path.join(path, 'etc'))
    return (os.path.exists(fpath), fpath)


def load_cfg(argpath=None):


    foundcfg = False
    cfg = None
    cfg_searched_paths = []
    # load config files..

    # first check for cmd line 'root='
    if args.path != None:

        foundcfg, etcpath = has_config_dir(args.path)
        if foundcfg:
            cfg = IcalConfig(os.path.dirname(etcpath))
            cfg.load()
        else:
            cfg_searched_paths.append(etcpath)

    else:
        # path not on caommand line...
        # first check directory with ical executable
        # then user HOME dir

        if not foundcfg:
            fpath = os.path.dirname(os.path.abspath(__file__))
            foundcfg, etcpath = has_config_dir(fpath)

            if foundcfg:
                cfg = IcalConfig(os.path.dirname(etcpath))
                cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

        if not foundcfg:
            foundcfg, etcpath = has_config_dir(os.path.expanduser('~'))

            if foundcfg:
                cfg = IcalConfig(os.path.dirname(etcpath))
                cfg.load()
            else:
                cfg_searched_paths.append(etcpath)

    if not foundcfg:

        print('ERROR: Could not load configuration data from etc directory.\n')
        print('ERROR: Paths checked:')
        for p in cfg_searched_paths:
            print('   '+p)

    # else:
    return cfg


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ICAL Calibration Application.')
    parser.add_argument('-p', '--path', help='Local path to configuration files.')
    args = parser.parse_args()

    cfg = load_cfg()

    if cfg:
        # Ok, cooking with gas!

        app = QtWidgets.QApplication(sys.argv)
        appMainWindow = QtWidgets.QMainWindow()

        main_win = Ui_MainWindow()
        main_win.setupUi(appMainWindow)

        mw_hlpr = MainWindowHelper(cfg, appMainWindow, main_win)

        mw_hlpr.setup_main_window()

        appMainWindow.show()

        sys.exit(app.exec_())

