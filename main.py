# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from pydev_ipython.qt import QtGui

from src.constant.constant import BOOT_DIR
from src.main_window.generator_gui import MainWindow
import sys
_author_ = 'luwt'
_date_ = '2020/6/15 17:20'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(
        QtGui.QPixmap(BOOT_DIR + "boot.jpg").scaled(600, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    splash.showMessage("加载中...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
    # 显示启动界面
    splash.show()
    QtWidgets.qApp.processEvents()
    ui = MainWindow()
    ui.show()
    splash.finish(ui)
    app.exec_()
    ui.close_conn()
    sys.exit()
