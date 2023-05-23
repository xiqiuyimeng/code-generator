# -*- coding: utf-8 -*-
import ctypes
import importlib
import platform
import sys

import win32gui
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from src.constant.window_constant import WINDOW_TITLE
from src.logger.log import logger as log
from src.service.read_qrc.read_config import read_qss
from src.service.util.init_util import init_data
from src.view.window.main_window import MainWindow
from src.view.window.main_window_func import set_window

# 引入静态资源
from static import image_rc

pyi_splash_spec = importlib.util.find_spec("pyi_splash")
if pyi_splash_spec is not None:
    import pyi_splash

_author_ = 'luwt'
_date_ = '2022/5/11 10:33'


def enum_window(hwnd, enum_result: list):
    """找到当前窗口splash对应的窗口句柄"""
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == WINDOW_TITLE:
            enum_result.append(hwnd)


def move_above_splash(hwnd):
    """将当前窗口移到splash屏上方"""
    splash_hwnd = list()
    win32gui.EnumWindows(enum_window, splash_hwnd)
    if len(splash_hwnd) > 0:
        if win32gui.GetForegroundWindow() == splash_hwnd[0]:
            # SWP_NOMOVE | SWP_NOSIZE
            flags = 0x03
        else:
            # SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE
            flags = 0x13

        # Move our window, so it is immediately after the splash window.
        # Activate if splash was foreground, otherwise not.
        win32gui.SetWindowPos(hwnd, splash_hwnd[0], 0, 0, 0, 0, flags)
        # Now move the splash window so that it is behind the main window.
        # Always "no activate"
        win32gui.SetWindowPos(splash_hwnd[0], hwnd, 0, 0, 0, 0, 0x13)
        # Make ourselves the foreground window.
        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            # 这样可以避免多次点击导致的获取句柄错误
            pass


if __name__ == "__main__":
    log.info("**********生成器启动**********")
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(
        QtGui.QPixmap(":/boot_jpg/boot.jpg").scaled(600, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    splash.showMessage("加载中...", Qt.AlignHCenter | Qt.AlignBottom)
    # 显示启动界面
    splash.show()
    QtWidgets.qApp.processEvents()
    # 后台数据初始化
    init_data()
    # 获取当前屏幕分辨率
    desktop = QtWidgets.QApplication.desktop()
    app.setStyleSheet(read_qss())
    screen_rect = desktop.screenGeometry()
    main_window = MainWindow(screen_rect)
    # 保存引用
    set_window(main_window)
    # 声明AppUserModelID，否则windows认为这是python子程序，无法使用自定义任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("generator")
    main_window.show()
    if pyi_splash_spec is not None and pyi_splash.is_alive():
        if platform.system() == 'Windows':
            move_above_splash(main_window.winId())
        pyi_splash.close()
    splash.finish(main_window)
    app.exec_()
    log.info("**********生成器退出**********\n")
    sys.exit()
