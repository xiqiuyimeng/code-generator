# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import ctypes
from src.main_window.generator_gui import MainWindow
from src.read_qrc.read_file import read_qss, read_template
from src.sys.sys_info_storage.template_sqlite import TemplateSqlite
from static import image_rc

import sys


_author_ = 'luwt'
_date_ = '2020/6/15 17:20'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(
        QtGui.QPixmap(":/boot_jpg/boot.jpg").scaled(600, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    splash.showMessage("加载中...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
    # 显示启动界面
    splash.show()
    QtWidgets.qApp.processEvents()
    template = TemplateSqlite().get_templates(tp_type=0)
    # 如果默认模板不存在，则初始化
    if not template:
        # 初始化模板文件
        TemplateSqlite().init_template(read_template())
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
    ui.close_conn()
    sys.exit()
