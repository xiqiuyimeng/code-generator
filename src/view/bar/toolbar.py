# -*- coding: utf-8 -*-
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QToolBar, QMenu

from src.constant.bar_constant import SWITCH_ACTION, ADD_DS_ACTION, ADD_DS_ACTION_TIP
from src.view.bar.bar_action import *
from src.view.custom_widget.draggable_widget import DraggableWidget

_author_ = 'luwt'
_date_ = '2022/5/7 12:43'


class ToolBar(QToolBar, DraggableWidget):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window
        self.setObjectName("toolbar")

        self.setIconSize(QSize(50, 40))
        # 设置名称显示在图标下面（默认本来是只显示图标）
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.switch_ds_category_menu = ...
        self.add_ds_menu: QMenu = ...

    def fill_tool_bar(self):
        self.add_switch_ds_category_tool()
        self.add_ds_tool()

        # 刷新
        self.add_refresh_tool()
        self.addSeparator()

        # 类型映射
        self.add_type_mapping_tool()
        # 模板设置
        self.add_template_tool()
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

    def switch_ds_category(self):
        # 重新构建 switch_ds_category_menu 和 add_ds_menu 的下拉列表
        self.switch_ds_category_menu.clear()
        self.add_ds_menu.clear()
        add_switch_ds_category_actions(self.switch_ds_category_menu, self.main_window)
        add_ds_actions(self.add_ds_menu, self.main_window)

    def add_switch_ds_category_tool(self):
        # 实现工具栏下拉效果，需要使用 QToolButton，设置menu即可下拉
        switch_ds_category_tool = add_tool_button(SWITCH_ACTION, SWITCH_ACTION_TIP)

        self.switch_ds_category_menu = QMenu()
        self.switch_ds_category_menu.triggered.connect(self.main_window.switch_ds_category)
        switch_ds_category_tool.setMenu(self.switch_ds_category_menu)

        self.addSeparator()
        self.addWidget(switch_ds_category_tool)

    def add_ds_tool(self):
        add_ds_tool = add_tool_button(ADD_DS_ACTION, ADD_DS_ACTION_TIP)

        self.add_ds_menu = QMenu()
        add_ds_tool.setMenu(self.add_ds_menu)

        self.addWidget(add_ds_tool)

    def add_refresh_tool(self):
        refresh_tool = add_refresh_action(self.main_window)
        self.addAction(refresh_tool)

    def add_type_mapping_tool(self):
        type_mapping_tool = add_type_mapping_action(self.main_window)
        self.addAction(type_mapping_tool)

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
