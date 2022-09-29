# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from constant.constant import REFRESH_ACTION, REFRESH_ACTION_TIP, CLEAR_DATA_ACTION, CLEAR_DATA_ACTION_TIP, \
    TEMPLATE_ACTION_TIP, TEMPLATE_ACTION, GENERATE_ACTION, GENERATE_ACTION_TP, EXIT_ACTION, EXIT_ACTION_TP, \
    HELP_ACTION, HELP_ACTION_TIP, ABOUT_ACTION_TIP, ABOUT_ACTION, SWITCH_ACTION_TIP, SQL_DATASOURCE_TYPE,\
    STRUCTURE_DATASOURCE_TYPE
from service.system_storage.conn_type import ConnTypeEnum
from view.bar.bar_function import open_conn_dialog

_author_ = 'luwt'
_date_ = '2022/9/29 12:38'


def add_switch_ds_type_actions(parent_menu, main_window):
    for ds_type in main_window.datasource_types:
        switch_ds_type_action = QAction(QIcon(ds_type.icon_path), ds_type.name, main_window)
        switch_ds_type_action.setStatusTip(f'{SWITCH_ACTION_TIP} {ds_type.name}')
        parent_menu.addAction(switch_ds_type_action)


def add_ds_actions(parent_menu, main_window):
    # 检查是否已经存在信号槽连接，如果存在，断开信号槽连接
    if parent_menu.receivers(parent_menu.triggered):
        parent_menu.triggered.disconnect()
    # 根据当前的数据源类型，决定构建的action类型
    if main_window.current_ds_type.name == SQL_DATASOURCE_TYPE:
        add_sql_ds_actions(parent_menu, main_window)
        # 连接菜单点击信号槽
        parent_menu.triggered.connect(lambda action: open_conn_dialog(action, main_window.tree_widget,
                                                                      main_window.geometry()))
    elif main_window.current_ds_type.name == STRUCTURE_DATASOURCE_TYPE:
        add_structure_ds_actions(parent_menu, main_window)


def add_sql_ds_actions(parent_menu, main_window):
    for conn_type in ConnTypeEnum:
        add_action = QAction(QIcon(conn_type.value.icon_path), conn_type.value.display_name, main_window)
        add_action.setStatusTip('在左侧列表中添加一条连接')
        parent_menu.addAction(add_action)


def add_structure_ds_actions(parent_menu, main_window): ...


def add_refresh_action(main_window):
    refresh_action = QAction(QIcon(':/icon/refresh.png'), REFRESH_ACTION, main_window)
    refresh_action.setStatusTip(REFRESH_ACTION_TIP)
    return refresh_action


def add_template_action(main_window):
    template_action = QAction(QIcon(':/icon/template.png'), TEMPLATE_ACTION, main_window)
    template_action.setStatusTip(TEMPLATE_ACTION_TIP)
    return template_action


def add_generate_action(main_window):
    generate_action = QAction(QIcon(':/icon/exec.png'), GENERATE_ACTION, main_window)
    generate_action.setStatusTip(GENERATE_ACTION_TP)
    return generate_action


def add_clear_data_action(main_window):
    clear_action = QAction(QIcon(':/icon/remove.png'), CLEAR_DATA_ACTION, main_window)
    clear_action.setStatusTip(CLEAR_DATA_ACTION_TIP)
    return clear_action


def add_exit_action(main_window):
    exit_action = QAction(QIcon(':/icon/exit.png'), EXIT_ACTION, main_window)
    exit_action.setStatusTip(EXIT_ACTION_TP)
    exit_action.triggered.connect(main_window.close)
    return exit_action


def add_help_action(main_window):
    help_action = QAction(QIcon(':/icon/exec.png'), HELP_ACTION, main_window)
    help_action.setStatusTip(HELP_ACTION_TIP)
    return help_action


def add_about_action(main_window):
    about_action = QAction(QIcon(':/icon/exec.png'), ABOUT_ACTION, main_window)
    about_action.setStatusTip(ABOUT_ACTION_TIP)
    return about_action
