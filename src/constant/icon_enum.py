# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtGui import QIcon

from src.constant.constant import SQL_DATASOURCE_TYPE, STRUCT_DATASOURCE_TYPE, SWITCH_ACTION, ADD_DS_ACTION, \
    REFRESH_ACTION, TEMPLATE_ACTION, GENERATE_ACTION, CLEAR_DATA_ACTION, EXIT_ACTION, HELP_ACTION, ABOUT_ACTION, \
    SQLITE_DISPLAY_NAME, MYSQL_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, MYSQL_DB, MYSQL_TB, OPEN_CONN_ACTION, \
    CANCEL_OPEN_CONN_ACTION, CLOSE_CONN_ACTION, TEST_CONN_ACTION, CANCEL_TEST_CONN_ACTION, ADD_CONN_ACTION, \
    EDIT_CONN_ACTION, DEL_CONN_ACTION, SQLITE_COL, MYSQL_COL, JSON_DISPLAY_NAME, FOLDER_TYPE, NAME_AVAILABLE, \
    NAME_EXISTS, CREATE_NEW_FOLDER_ACTION, RENAME_FOLDER_ACTION, DEL_FOLDER_ACTION, CANCEL_OPEN_STRUCT_ACTION, \
    OPEN_STRUCT_ACTION, CLOSE_STRUCT_ACTION, EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, EXPAND_CHILD_TABLE, \
    COLLAPSE_CHILD_TABLE, STRUCT_COL_ICON, CANCEL_REFRESH_CONN_ACTION, REFRESH_CONN_ACTION, OPEN_DB_ACTION, \
    CANCEL_OPEN_DB_ACTION, CLOSE_DB_ACTION, SELECT_ALL_TB_ACTION, UNSELECT_TB_ACTION, REFRESH_DB_ACTION, \
    CANCEL_REFRESH_DB_ACTION, OPEN_TABLE_ACTION, CANCEL_OPEN_TABLE_ACTION, CLOSE_TABLE_ACTION, \
    SELECT_ALL_FIELD_ACTION, UNSELECT_FIELD_ACTION, REFRESH_TB_ACTION, CANCEL_REFRESH_TB_ACTION, \
    REFRESH_STRUCT_ACTION, CANCEL_REFRESH_STRUCT_ACTION, REFRESH_FOLDER_ACTION, CANCEL_REFRESH_FOLDER_ACTION, \
    SELECT_ALL_ACTION, UNSELECT_ACTION, ORACLE_DISPLAY_NAME, ORACLE_DB, ORACLE_TB, ORACLE_COL

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
    # sql conn
    open_conn_icon = OPEN_CONN_ACTION, ':/icon/exec.png'
    cancel_open_conn_icon = CANCEL_OPEN_CONN_ACTION, ':/icon/exec.png'
    refresh_conn_icon = REFRESH_CONN_ACTION, ':/icon/exec.png'
    cancel_refresh_conn_icon = CANCEL_REFRESH_CONN_ACTION, ':/icon/exec.png'
    close_conn_icon = CLOSE_CONN_ACTION, ':/icon/exec.png'
    test_conn_icon = TEST_CONN_ACTION, ':/icon/exec.png'
    cancel_test_conn_icon = CANCEL_TEST_CONN_ACTION, ':/icon/exec.png'
    add_conn_icon = ADD_CONN_ACTION, ':/icon/exec.png'
    edit_conn_icon = EDIT_CONN_ACTION, ':/icon/exec.png'
    del_conn_icon = DEL_CONN_ACTION, ':/icon/exec.png'
    # sql db
    open_db_icon = OPEN_DB_ACTION, ':/icon/exec.png'
    cancel_open_db_icon = CANCEL_OPEN_DB_ACTION, ':/icon/exec.png'
    close_db_icon = CLOSE_DB_ACTION, ':/icon/exec.png'
    select_all_tb_icon = SELECT_ALL_TB_ACTION, ':/icon/exec.png'
    unselect_tb_icon = UNSELECT_TB_ACTION, ':/icon/exec.png'
    refresh_db_icon = REFRESH_DB_ACTION, ':/icon/exec.png'
    cancel_refresh_db_icon = CANCEL_REFRESH_DB_ACTION, ':/icon/exec.png'
    # sql tb
    open_table_icon = OPEN_TABLE_ACTION, ':/icon/exec.png'
    cancel_open_table_icon = CANCEL_OPEN_TABLE_ACTION, ':/icon/exec.png'
    close_table_icon = CLOSE_TABLE_ACTION, ':/icon/exec.png'
    select_all_field_icon = SELECT_ALL_FIELD_ACTION, ':/icon/exec.png'
    unselect_field_icon = UNSELECT_FIELD_ACTION, ':/icon/exec.png'
    refresh_tb_icon = REFRESH_TB_ACTION, ':/icon/exec.png'
    cancel_refresh_tb_icon = CANCEL_REFRESH_TB_ACTION, ':/icon/exec.png'

    # struct
    cancel_open_struct_icon = CANCEL_OPEN_STRUCT_ACTION, ':/icon/refresh.png'
    open_struct_icon = OPEN_STRUCT_ACTION, ':/icon/exec.png'
    close_struct_icon = CLOSE_STRUCT_ACTION, ':/icon/wrong.png'
    edit_struct_icon = EDIT_STRUCT_ACTION, ':/icon/right.png'
    del_struct_icon = DEL_STRUCT_ACTION, ':/icon/remove.png'
    refresh_struct_icon = REFRESH_STRUCT_ACTION, ':/icon/remove.png'
    cancel_refresh_struct_icon = CANCEL_REFRESH_STRUCT_ACTION, ':/icon/remove.png'
    select_all_icon = SELECT_ALL_ACTION, ':/icon/remove.png'
    unselect_icon = UNSELECT_ACTION, ':/icon/remove.png'
    refresh_folder_icon = REFRESH_FOLDER_ACTION, ':/icon/remove.png'
    cancel_refresh_folder_icon = CANCEL_REFRESH_FOLDER_ACTION, ':/icon/remove.png'

    # table
    expand_child_table_icon = EXPAND_CHILD_TABLE, ':/icon/add.png'
    collapse_child_table_icon = COLLAPSE_CHILD_TABLE, ':/icon/remove.png'

    # 名称校验 icon
    name_available_icon = NAME_AVAILABLE, ':/icon/right.png'
    name_unavailable_icon = NAME_EXISTS, ':/icon/wrong.png'

    # datasource type icon
    sql_ds_icon = SQL_DATASOURCE_TYPE, ':/icon/add.png'
    structure_ds_icon = STRUCT_DATASOURCE_TYPE, ':/icon/add.png'

    # sql datasource icon
    # sqlite
    sql_sqlite_conn_icon = SQLITE_DISPLAY_NAME, ':/icon/table_icon.png'
    sql_sqlite_db_icon = SQLITE_DB, ':/icon/database_icon.png'
    sql_sqlite_tb_icon = SQLITE_TB, ':/icon/table_icon.png'
    sql_sqlite_col_icon = SQLITE_COL, ':/icon/column_icon.png'
    # mysql
    sql_mysql_conn_icon = MYSQL_DISPLAY_NAME, ':/icon/mysql_conn_icon.png'
    sql_mysql_db_icon = MYSQL_DB, ':/icon/database_icon.png'
    sql_mysql_tb_icon = MYSQL_TB, ':/icon/table_icon.png'
    sql_mysql_col_icon = MYSQL_COL, ':/icon/column_icon.png'
    # oracle
    sql_oracle_conn_icon = ORACLE_DISPLAY_NAME, ':/icon/right.png'
    sql_oracle_db_icon = ORACLE_DB, ':/icon/template.png'
    sql_oracle_tb_icon = ORACLE_TB, ':/icon/table_icon.png'
    sql_oracle_col_icon = ORACLE_COL, ':/icon/column_icon.png'

    # structure datasource icon
    folder_icon = FOLDER_TYPE, ':/icon/template.png'
    json_type_icon = JSON_DISPLAY_NAME, ':/icon/exec.png'
    struct_col_icon = STRUCT_COL_ICON, ':/icon/column_icon.png'
    new_folder_icon = CREATE_NEW_FOLDER_ACTION, ':/icon/add.png'
    rename_folder_icon = RENAME_FOLDER_ACTION, ':/icon/exec.png'
    del_folder_icon = DEL_FOLDER_ACTION, ':/icon/remove.png'


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
