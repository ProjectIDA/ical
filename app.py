from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("ICal")

        closeBtn = QPushButton("Quit")
        closeBtn.pressed.connect(self.closePushed)

        self.setCentralWidget(closeBtn)

    def closePushed(self):
        app.exit(0)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
