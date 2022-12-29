# -*- coding: utf-8 -*-
"""
菜单栏展示
"""
from PyQt5.QtWidgets import QMenuBar, QMenu

from constant.constant import FILE_MENU, HELP_MENU, SWITCH_ACTION, ADD_DS_ACTION
from view.bar.bar_action import *

_author_ = 'luwt'
_date_ = '2022/5/7 12:18'


class Menubar(QMenuBar):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window

        self.file_menu: QMenu = self.addMenu(FILE_MENU)
        self.help_menu = self.addMenu(HELP_MENU)

        self.switch_ds_type_menu = ...
        self.add_datasource_menu = ...

    def fill_menu_bar(self):
        self.add_switch_menu()
        self.add_ds_menu()

        # 刷新
        self.add_refresh_menu()
        # 模板设置
        self.add_template_menu()
        # 生成
        self.add_generate_menu()
        # 清空选择
        self.add_clear_menu()
        # 退出
        self.add_exit_menu()

        # 帮助
        self.add_help_menu()
        # 关于
        self.add_about_menu()

    def switch_ds_type(self):
        # 重新构建 switch_ds_type_menu 和 add_datasource_menu 的下拉列表
        self.switch_ds_type_menu.clear()
        self.add_datasource_menu.clear()
        add_switch_ds_type_actions(self.switch_ds_type_menu, self.main_window)
        add_ds_actions(self.add_datasource_menu, self.main_window)

    def add_switch_menu(self):
        self.switch_ds_type_menu = self.file_menu.addMenu(get_icon(SWITCH_ACTION), SWITCH_ACTION)
        self.switch_ds_type_menu.triggered.connect(self.main_window.switch_ds_type)

    def add_ds_menu(self):
        self.add_datasource_menu = self.file_menu.addMenu(get_icon(ADD_DS_ACTION), ADD_DS_ACTION)

    def add_refresh_menu(self):
        refresh_action = add_refresh_action(self.main_window)
        self.file_menu.addAction(refresh_action)

    def add_template_menu(self):
        template_action = add_template_action(self.main_window)
        self.file_menu.addAction(template_action)

    def add_generate_menu(self):
        generate_action = add_generate_action(self.main_window)
        self.file_menu.addAction(generate_action)

    def add_clear_menu(self):
        clear_action = add_clear_data_action(self.main_window)
        self.file_menu.addAction(clear_action)

    def add_exit_menu(self):
        exit_action = add_exit_action(self.main_window)
        self.file_menu.addAction(exit_action)

    def add_help_menu(self):
        help_action = add_help_action(self.main_window)
        self.help_menu.addAction(help_action)

    def add_about_menu(self):
        about_action = add_about_action(self.main_window)
        self.help_menu.addAction(about_action)


