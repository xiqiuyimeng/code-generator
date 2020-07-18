# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import sip
from generator_gui import MainWindow
import sys
_author_ = 'luwt'
_date_ = '2020/6/15 17:20'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec_()
    ui.close_conn()
    print('退出')
    sys.exit()
