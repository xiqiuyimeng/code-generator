# -*- coding: utf-8 -*-
"""
菜单栏列表生成
"""
from PyQt5 import QtGui, QtWidgets
from constant import *
_author_ = 'luwt'
_date_ = '2020/6/27 8:26'


def fill_menu_bar(gui):
    gui.file_menu = gui.menubar.addMenu('文件')
    add_conn_menu(gui)
    generate_menu(gui)
    exit_app_menu(gui)

    gui.help_menu = gui.menubar.addMenu('帮助')


def add_conn_menu(gui):
    add_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), ADD_CONN_MENU, gui)
    add_action.setShortcut('Ctrl+N')
    add_action.setStatusTip('在左侧列表中添加一条连接')
    add_action.triggered.connect(gui.add_conn)

    gui.file_menu.addAction(add_action)


def exit_app_menu(gui):
    exit_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), '退出', gui)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('退出应用程序')
    exit_action.triggered.connect(gui.quit)

    gui.file_menu.addAction(exit_action)


def generate_menu(gui):
    generate_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), GENERATE_MENU, gui)
    generate_action.setShortcut('Ctrl+G')
    generate_action.setStatusTip('根据选择执行生成命令')
    generate_action.triggered.connect(gui.generate)

    gui.file_menu.addAction(generate_action)
