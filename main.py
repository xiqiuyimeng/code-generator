# -*- coding: utf-8 -*-
import ctypes

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import sys
from src.service.read_qrc.read_config import read_qss
from src.view.window.main_window import MainWindow
from src.logger.log import logger as log
# 引入静态资源
from static import image_rc
# 引入pyinstaller打包使用的过渡图程序，打包的时候需要放开
# import src.loading_window

_author_ = 'luwt'
_date_ = '2022/5/11 10:33'


if __name__ == "__main__":
    log.info("**********生成器启动**********")
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(
        QPixmap(":/boot/boot.jpg").scaled(600, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    splash.showMessage("加载中...", Qt.AlignHCenter | Qt.AlignBottom)
    # 显示启动界面
    splash.show()
    QtWidgets.qApp.processEvents()
    # 获取当前屏幕分辨率
    desktop = QtWidgets.QApplication.desktop()
    app.setStyleSheet(read_qss())
    screen_rect = desktop.screenGeometry()
    ui = MainWindow(screen_rect)
    # 声明AppUserModelID，否则windows认为这是python子程序，无法使用自定义任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("generator")
    ui.show()
    splash.finish(ui)
    app.exec_()
    log.info("**********生成器退出**********\n")
    sys.exit()
