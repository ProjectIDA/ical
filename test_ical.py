import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.iCalGui.mw import *
from gui.iCalGui.setup_mw import MainWindowHelper #setup_main_window, setup_tableview

app = QtWidgets.QApplication(sys.argv)
appMainWindow = QtWidgets.QMainWindow()

main_win = Ui_MainWindow()
main_win.setupUi(appMainWindow)

mw_hlpr = MainWindowHelper(appMainWindow, main_win)

mw_hlpr.setup_main_window()
# setup_tableview(appMainWindow, mw_ui)

appMainWindow.show()

sys.exit(app.exec_())
