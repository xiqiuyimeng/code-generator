# -*- coding: utf-8 -*-
"""
菜单栏展示
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

from constant.constant import FILE_MENU, HELP_MENU, ADD_CONN_MENU, GENERATE_MENU, EXIT_MENU, ABOUT_MENU
from view.bar.bar_function import add_sql_datasource_actions

_author_ = 'luwt'
_date_ = '2022/5/7 12:18'


class Menubar(QMenuBar):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window

        self.file_menu: QMenu = ...
        self.help_menu = ...

    def fill_menu_bar(self):
        self.file_menu = self.addMenu(FILE_MENU)
        self.file_menu.setObjectName("file_menu")
        self.add_conn_menu()
        self.add_generate_menu()
        self.add_exit_menu()

        self.help_menu = self.addMenu(HELP_MENU)
        self.help_menu.setObjectName("help_menu")
        self.add_help_menu()
        self.add_about_menu()

    def add_conn_menu(self):
        add_menu: QMenu = self.file_menu.addMenu(ADD_CONN_MENU)
        add_sql_datasource_actions(self.main_window, add_menu)

    def add_generate_menu(self):
        generate_action = QAction(QIcon(':/icon/exec.png'), GENERATE_MENU, self.main_window)
        generate_action.setShortcut('Ctrl+G')
        generate_action.setStatusTip('根据选择执行生成命令')
        # generate_action.triggered.connect(gui.generate)

        self.file_menu.addAction(generate_action)

    def add_exit_menu(self):
        exit_action = QAction(QIcon(':/icon/exit.png'), EXIT_MENU, self.main_window)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.main_window.close)

        self.file_menu.addAction(exit_action)

    def add_help_menu(self):
        help_action = QAction(QIcon(":/icon/add.png"), HELP_MENU, self.main_window)
        help_action.setShortcut('Ctrl+H')
        help_action.setStatusTip('帮助信息')
        # help_action.triggered.connect(gui.help)

        self.help_menu.addAction(help_action)

    def add_about_menu(self):
        about_action = QAction(QIcon(":/icon/exit.png"), ABOUT_MENU, self.main_window)
        about_action.setStatusTip('关于')
        # about_action.triggered.connect(gui.about)

        self.help_menu.addAction(about_action)

