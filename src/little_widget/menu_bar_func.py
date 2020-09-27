# -*- coding: utf-8 -*-
"""
菜单栏列表生成
"""

from PyQt5 import QtGui, QtWidgets

from src.constant.constant import ADD_CONN_MENU, GENERATE_MENU, FILE_MENU, HELP_MENU, EXIT_MENU, ABOUT_MENU
from src.func.tree_function import add_conn_func

_author_ = 'luwt'
_date_ = '2020/6/27 8:26'


def fill_menu_bar(gui):
    """
    填充菜单栏
    :param gui: 启动的主窗口界面对象
    """
    gui.file_menu = gui.menubar.addMenu(FILE_MENU)
    gui.file_menu.setObjectName("file_menu")
    add_conn_menu(gui)
    generate_menu(gui)
    exit_app_menu(gui)

    gui.help_menu = gui.menubar.addMenu(HELP_MENU)
    gui.help_menu.setObjectName("help_menu")
    help_menu(gui)
    about_menu(gui)


def add_conn_menu(gui):
    """
    添加连接菜单
    :param gui: 启动的主窗口界面对象
    """
    add_action = QtWidgets.QAction(QtGui.QIcon(':/icon/add.png'), ADD_CONN_MENU, gui)
    add_action.setShortcut('Ctrl+N')
    add_action.setStatusTip('在左侧列表中添加一条连接')
    add_action.triggered.connect(lambda: add_conn_func(gui, gui.screen_rect))

    gui.file_menu.addAction(add_action)


def exit_app_menu(gui):
    """
    退出菜单
    :param gui: 启动的主窗口界面对象
    """
    exit_action = QtWidgets.QAction(QtGui.QIcon(':/icon/exit.png'), EXIT_MENU, gui)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('退出应用程序')
    exit_action.triggered.connect(gui.quit)

    gui.file_menu.addAction(exit_action)


def generate_menu(gui):
    """
    生成菜单
    :param gui: 启动的主窗口界面对象
    """
    generate_action = QtWidgets.QAction(QtGui.QIcon(':/icon/exec.png'), GENERATE_MENU, gui)
    generate_action.setShortcut('Ctrl+G')
    generate_action.setStatusTip('根据选择执行生成命令')
    generate_action.triggered.connect(gui.generate)

    gui.file_menu.addAction(generate_action)


def help_menu(gui):
    """帮助菜单"""
    help_action = QtWidgets.QAction(QtGui.QIcon(":/icon/add.png"), HELP_MENU, gui)
    help_action.setShortcut('Ctrl+H')
    help_action.setStatusTip('帮助信息')
    help_action.triggered.connect(gui.help)
    gui.help_menu.addAction(help_action)


def about_menu(gui):
    """关于菜单"""
    about_action = QtWidgets.QAction(QtGui.QIcon(":/icon/exit.png"), ABOUT_MENU, gui)
    about_action.setStatusTip('关于')
    about_action.triggered.connect(gui.about)
    gui.help_menu.addAction(about_action)
