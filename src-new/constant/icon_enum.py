# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtGui import QIcon

from constant.constant import SQL_DATASOURCE_TYPE, STRUCTURE_DATASOURCE_TYPE, SWITCH_ACTION, ADD_DS_ACTION, \
    REFRESH_ACTION, TEMPLATE_ACTION, GENERATE_ACTION, CLEAR_DATA_ACTION, EXIT_ACTION, HELP_ACTION, ABOUT_ACTION, \
    SQLITE_DISPLAY_NAME, MYSQL_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, MYSQL_DB, MYSQL_TB, OPEN_CONN_ACTION, \
    CANCEL_OPEN_CONN_ACTION, CLOSE_CONN_ACTION, TEST_CONN_ACTION, CANCEL_TEST_CONN_ACTION, ADD_CONN_ACTION, \
    EDIT_CONN_ACTION, DEL_CONN_ACTION

_author_ = 'luwt'
_date_ = '2022/9/30 17:57'


icon_dict = dict()


class IconEnum(Enum):

    # window icon
    window_icon = 'window', ':/icon/exec.png'

    # bar icon
    switch_ds_type_icon = SWITCH_ACTION, ':/icon/exec.png'
    add_ds_icon = ADD_DS_ACTION, ':/icon/add.png'
    refresh_icon = REFRESH_ACTION, ':/icon/refresh.png'
    template_icon = TEMPLATE_ACTION, ':/icon/template.png'
    generate_icon = GENERATE_ACTION, ':/icon/exec.png'
    clear_data_icon = CLEAR_DATA_ACTION, ':/icon/remove.png'
    exit_icon = EXIT_ACTION, ':/icon/exit.png'
    help_icon = HELP_ACTION, ':/icon/exec.png'
    about_icon = ABOUT_ACTION, ':/icon/exec.png'

    # 右键菜单 icon
    open_conn_icon = OPEN_CONN_ACTION, ':/icon/exec.png'
    cancel_open_conn_icon = CANCEL_OPEN_CONN_ACTION, ':/icon/exec.png'
    close_conn_icon = CLOSE_CONN_ACTION, ':/icon/exec.png'
    test_conn_icon = TEST_CONN_ACTION, ':/icon/exec.png'
    cancel_test_conn_icon = CANCEL_TEST_CONN_ACTION, ':/icon/exec.png'
    add_conn_icon = ADD_CONN_ACTION, ':/icon/exec.png'
    edit_conn_icon = EDIT_CONN_ACTION, ':/icon/exec.png'
    del_conn_icon = DEL_CONN_ACTION, ':/icon/exec.png'

    # datasource type icon
    sql_ds_icon = SQL_DATASOURCE_TYPE, ':/icon/add.png'
    structure_ds_icon = STRUCTURE_DATASOURCE_TYPE, ':/icon/add.png'

    # sql datasource icon
    # sqlite
    sql_sqlite_conn_icon = SQLITE_DISPLAY_NAME, ':/icon/table_icon.png'
    sql_sqlite_db_icon = SQLITE_DB, ':/icon/database_icon.png'
    sql_sqlite_tb_icon = SQLITE_TB, ':/icon/table_icon.png'
    # mysql
    sql_mysql_conn_icon = MYSQL_DISPLAY_NAME, ':/icon/mysql_conn_icon.png'
    sql_mysql_db_icon = MYSQL_DB, ':/icon/database_icon.png'
    sql_mysql_tb_icon = MYSQL_TB, ':/icon/table_icon.png'


def get_icon_path(name):
    for icon_enum in IconEnum:
        if icon_enum.value[0] == name:
            return icon_enum.value[1]


def create_icon(icon_path, name):
    icon = QIcon(icon_path)
    icon_dict[icon_path] = icon
    return get_icon(name)


def get_icon(name):
    icon_path = get_icon_path(name)
    if icon_path:
        # 首先获取icon，如果不存在，再创建icon
        icon = icon_dict.get(icon_path)
        if not icon:
            return create_icon(icon_path, name)
        return icon
