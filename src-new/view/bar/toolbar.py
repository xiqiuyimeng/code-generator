# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolBar, QMenu, QToolButton

from constant.constant import SWITCH_ACTION, ADD_CONN_MENU
from view.bar.bar_action import *
from view.custom_widget.draggable_widget import DraggableWidget

_author_ = 'luwt'
_date_ = '2022/5/7 12:43'


class ToolBar(QToolBar, DraggableWidget):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window
        self.setObjectName("toolbar")

        self.setIconSize(QSize(50, 40))
        # 设置名称显示在图标下面（默认本来是只显示图标）
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.switch_ds_type_menu = ...
        self.add_ds_menu: QMenu = ...

    def fill_tool_bar(self):
        self.add_switch_source_type_tool()
        self.add_ds_tool()

        # 模板设置
        self.add_template_tool()

        self.addSeparator()

        # 刷新
        self.add_refresh_tool()
        # 生成
        self.add_generate_tool()
        # 清空选择
        self.add_clear_tool()

        self.addSeparator()

        # 帮助
        self.add_help_tool()
        # 关于
        self.add_about_tool()
        # 退出
        self.add_exit_tool()

    def switch_ds_type(self):
        # 重新构建 switch_ds_type_menu 和 add_ds_menu 的下拉列表
        self.switch_ds_type_menu.clear()
        self.add_ds_menu.clear()
        # 由于 add_ds_menu 是在添加 action 的时候才连接信号槽，所以这里必须先断开之前的信号槽连接，否则会导致信号槽多次连接
        if self.add_ds_menu.receivers(self.add_ds_menu.triggered):
            self.add_ds_menu.triggered.disconnect()
        add_switch_ds_type_actions(self.switch_ds_type_menu, self.main_window)
        add_ds_actions(self.add_ds_menu, self.main_window)

    def add_switch_source_type_tool(self):
        # 实现工具栏下拉效果，需要使用 QToolButton，设置menu即可下拉
        switch_ds_type_tool = QToolButton()
        switch_ds_type_tool.setIcon(QIcon(':/icon/exec.png'))
        switch_ds_type_tool.setText(SWITCH_ACTION)
        switch_ds_type_tool.setStatusTip(SWITCH_ACTION_TIP)
        switch_ds_type_tool.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        switch_ds_type_tool.setPopupMode(QToolButton.InstantPopup)

        self.switch_ds_type_menu = QMenu()
        self.switch_ds_type_menu.triggered.connect(self.main_window.switch_ds_type)
        switch_ds_type_tool.setMenu(self.switch_ds_type_menu)

        self.addSeparator()
        self.addWidget(switch_ds_type_tool)

    def add_ds_tool(self):
        add_ds_tool = QToolButton()
        add_ds_tool.setIcon(QIcon(':/icon/add.png'))
        add_ds_tool.setText(ADD_CONN_MENU)
        add_ds_tool.setStatusTip(ADD_CONN_MENU)
        add_ds_tool.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        add_ds_tool.setPopupMode(QToolButton.InstantPopup)

        self.add_ds_menu = QMenu()
        add_ds_tool.setMenu(self.add_ds_menu)

        self.addWidget(add_ds_tool)

    def add_refresh_tool(self):
        refresh_tool = add_refresh_action(self.main_window)
        self.addAction(refresh_tool)

    def add_template_tool(self):
        template_tool = add_template_action(self.main_window)
        self.addAction(template_tool)

    def add_generate_tool(self):
        generate_tool = add_generate_action(self.main_window)
        self.addAction(generate_tool)

    def add_clear_tool(self):
        clear_tool = add_clear_data_action(self.main_window)
        self.addAction(clear_tool)

    def add_help_tool(self):
        help_tool = add_help_action(self.main_window)
        self.addAction(help_tool)

    def add_about_tool(self):
        about_tool = add_about_action(self.main_window)
        self.addAction(about_tool)

    def add_exit_tool(self):
        exit_tool = add_exit_action(self.main_window)
        self.addAction(exit_tool)
