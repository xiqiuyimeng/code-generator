# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets
from constant import *
_author_ = 'luwt'
_date_ = '2020/6/27 8:26'


def add_conn_menu(self):
    add_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), ADD_CONN_MENU, self)
    add_action.setShortcut('Ctrl+N')
    add_action.setStatusTip('在左侧列表中添加一条连接')
    add_action.triggered.connect(self.add_conn)

    self.file_menu.addAction(add_action)


def exit_app_menu(self):
    exit_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), '退出', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('退出应用程序')
    exit_action.triggered.connect(self.quit)

    self.file_menu.addAction(exit_action)


def generate_menu(self):
    generate_action = QtWidgets.QAction(QtGui.QIcon('right.jpg'), GENERATE_MENU, self)
    generate_action.setShortcut('Ctrl+G')
    generate_action.setStatusTip('根据选择执行生成命令')
    generate_action.triggered.connect(self.generate)

    self.file_menu.addAction(generate_action)
