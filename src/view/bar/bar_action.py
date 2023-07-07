# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolButton

from src.constant.bar_constant import REFRESH_ACTION, REFRESH_ACTION_TIP, CLEAR_DATA_ACTION, CLEAR_DATA_ACTION_TIP, \
    TEMPLATE_ACTION_TIP, TEMPLATE_ACTION, GENERATE_ACTION, GENERATE_ACTION_TP, EXIT_ACTION, EXIT_ACTION_TP, \
    HELP_ACTION, HELP_ACTION_TIP, ABOUT_ACTION_TIP, ABOUT_ACTION, SWITCH_ACTION_TIP, TYPE_ACTION, TYPE_ACTION_TIP
from src.enum.ds_category_enum import DsCategoryEnum
from src.enum.icon_enum import get_icon
from src.enum.conn_type_enum import ConnTypeEnum
from src.enum.struct_type_enum import StructTypeEnum
from src.view.bar.bar_function import open_conn_dialog, generate, clear_data, open_struct_dialog, refresh, \
    open_type_mapping_dialog, open_template_dialog, open_help_dialog, open_about_dialog

_author_ = 'luwt'
_date_ = '2022/9/29 12:38'


def add_switch_ds_category_actions(parent_menu, main_window):
    for ds_category in main_window.ds_categories:
        switch_ds_category_action = QAction(get_icon(ds_category.name), ds_category.name, main_window)
        switch_ds_category_action.setStatusTip(f'{SWITCH_ACTION_TIP} {ds_category.name}')
        parent_menu.addAction(switch_ds_category_action)


def add_ds_actions(parent_menu, main_window):
    # 检查是否已经存在信号槽连接，如果存在，断开信号槽连接
    if parent_menu.receivers(parent_menu.triggered):
        parent_menu.triggered.disconnect()
    # 根据当前的数据源类型，决定构建的action类型
    if main_window.current_ds_category.name == DsCategoryEnum.sql_ds_category.get_name():
        add_sql_ds_actions(parent_menu, main_window)
    elif main_window.current_ds_category.name == DsCategoryEnum.struct_ds_category.get_name():
        add_struct_ds_actions(parent_menu, main_window)


def add_sql_ds_actions(parent_menu, main_window):
    # 连接菜单点击信号槽
    parent_menu.triggered.connect(lambda action: open_conn_dialog(action))
    for conn_type in ConnTypeEnum:
        conn_type_name = conn_type.value.display_name
        add_action = QAction(get_icon(conn_type_name), conn_type_name, main_window)
        parent_menu.addAction(add_action)


def add_struct_ds_actions(parent_menu, main_window, parent_opened_item=None, parent_item=None):
    parent_menu.triggered.connect(lambda action: open_struct_dialog(action, parent_opened_item, parent_item))
    for struct_type in StructTypeEnum:
        struct_type_name = struct_type.value.display_name
        add_action = QAction(get_icon(struct_type_name), struct_type_name, main_window)
        parent_menu.addAction(add_action)


def add_tool_button(action_name, action_tip):
    tool_button = QToolButton()
    tool_button.setIcon(get_icon(action_name))
    tool_button.setText(action_name)
    tool_button.setStatusTip(action_tip)
    tool_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    return tool_button


def add_refresh_action(main_window):
    refresh_action = QAction(get_icon(REFRESH_ACTION), REFRESH_ACTION, main_window)
    refresh_action.setStatusTip(REFRESH_ACTION_TIP)
    refresh_action.triggered.connect(lambda: refresh(main_window))
    return refresh_action


def add_type_mapping_action(main_window):
    type_mapping_action = QAction(get_icon(TYPE_ACTION), TYPE_ACTION, main_window)
    type_mapping_action.setStatusTip(TYPE_ACTION_TIP)
    type_mapping_action.triggered.connect(lambda: open_type_mapping_dialog())
    return type_mapping_action


def add_template_action(main_window):
    template_action = QAction(get_icon(TEMPLATE_ACTION), TEMPLATE_ACTION, main_window)
    template_action.setStatusTip(TEMPLATE_ACTION_TIP)
    template_action.triggered.connect(lambda: open_template_dialog())
    return template_action


def add_generate_action(main_window):
    generate_action = QAction(get_icon(GENERATE_ACTION), GENERATE_ACTION, main_window)
    generate_action.setStatusTip(GENERATE_ACTION_TP)
    generate_action.triggered.connect(lambda: generate(main_window))
    return generate_action


def add_clear_data_action(main_window):
    clear_action = QAction(get_icon(CLEAR_DATA_ACTION), CLEAR_DATA_ACTION, main_window)
    clear_action.setStatusTip(CLEAR_DATA_ACTION_TIP)
    clear_action.triggered.connect(lambda: clear_data(main_window))
    return clear_action


def add_exit_action(main_window):
    exit_action = QAction(get_icon(EXIT_ACTION), EXIT_ACTION, main_window)
    exit_action.setStatusTip(EXIT_ACTION_TP)
    exit_action.triggered.connect(main_window.close)
    return exit_action


def add_help_action(main_window):
    help_action = QAction(get_icon(HELP_ACTION), HELP_ACTION, main_window)
    help_action.setStatusTip(HELP_ACTION_TIP)
    help_action.triggered.connect(lambda: open_help_dialog())
    return help_action


def add_about_action(main_window):
    about_action = QAction(get_icon(ABOUT_ACTION), ABOUT_ACTION, main_window)
    about_action.setStatusTip(ABOUT_ACTION_TIP)
    about_action.triggered.connect(lambda: open_about_dialog())
    return about_action
