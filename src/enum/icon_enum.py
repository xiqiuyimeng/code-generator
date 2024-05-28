# -*- coding: utf-8 -*-
"""
项目中所有使用到的icon枚举，每个枚举元素包括展示名称、icon具体路径，使用方调用时，获取路径即可渲染icon
"""
from enum import Enum

from PyQt6.QtGui import QIcon

from src.constant.bar_constant import SWITCH_ACTION, ADD_DS_ACTION, REFRESH_ACTION, TYPE_ACTION, TEMPLATE_ACTION, \
    GENERATE_ACTION, CLEAR_DATA_ACTION, EXIT_ACTION, HELP_ACTION, ABOUT_ACTION, SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.constant.ds_type_constant import SQLITE_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, SQLITE_COL, MYSQL_DISPLAY_NAME, \
    MYSQL_DB, MYSQL_TB, MYSQL_COL, ORACLE_DISPLAY_NAME, ORACLE_DB, ORACLE_TB, ORACLE_COL, JSON_DISPLAY_NAME, \
    STRUCT_COL_ICON
from src.constant.generator_dialog_constant import PREVIEW_TREE_FILE_ICON
from src.constant.list_constant import EDIT_LIST_ITEM_ICON, DEL_LIST_ITEM_ICON, DEL_ALL_LIST_ITEMS_ICON, \
    EXPORT_ITEM_ICON
from src.constant.table_constant import ROW_OPERATION_ICON, ROW_CAT_EDIT_ICON, \
    ROW_DEL_ICON, EXPAND_CHILD_TABLE_ICON, COLLAPSE_CHILD_TABLE_ICON, ROW_EXPORT_ICON, ROW_COPY_ICON
from src.constant.tree_constant import OPEN_CONN_ACTION, CANCEL_OPEN_CONN_ACTION, REFRESH_CONN_ACTION, \
    CANCEL_REFRESH_CONN_ACTION, CLOSE_CONN_ACTION, TEST_CONN_ACTION, CANCEL_TEST_CONN_ACTION, ADD_CONN_ACTION, \
    EDIT_CONN_ACTION, DEL_CONN_ACTION, OPEN_DB_ACTION, CANCEL_OPEN_DB_ACTION, CLOSE_DB_ACTION, SELECT_ALL_TB_ACTION, \
    UNSELECT_TB_ACTION, REFRESH_DB_ACTION, CANCEL_REFRESH_DB_ACTION, OPEN_TABLE_ACTION, CANCEL_OPEN_TABLE_ACTION, \
    CLOSE_TABLE_ACTION, SELECT_ALL_FIELD_ACTION, UNSELECT_FIELD_ACTION, REFRESH_TB_ACTION, CANCEL_REFRESH_TB_ACTION, \
    CANCEL_OPEN_STRUCT_ACTION, OPEN_STRUCT_ACTION, CLOSE_STRUCT_ACTION, EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, \
    REFRESH_STRUCT_ACTION, CANCEL_REFRESH_STRUCT_ACTION, SELECT_ALL_ACTION, UNSELECT_ACTION, REFRESH_FOLDER_ACTION, \
    CANCEL_REFRESH_FOLDER_ACTION, CREATE_NEW_FOLDER_ACTION, RENAME_FOLDER_ACTION, DEL_FOLDER_ACTION

_author_ = 'luwt'
_date_ = '2022/9/30 17:57'


icon_dict = dict()


class IconEnum(Enum):

    # window icon
    window_icon = 'window', 'icon:exec.png'

    # bar icon
    switch_ds_category_icon = SWITCH_ACTION, 'icon:switch_ds_category.png'
    add_ds_icon = ADD_DS_ACTION, 'icon:add.png'
    refresh_icon = REFRESH_ACTION, 'icon:refresh.png'
    type_mapping_icon = TYPE_ACTION, 'icon:type_mapping.png'
    template_icon = TEMPLATE_ACTION, 'icon:template.png'
    generate_icon = GENERATE_ACTION, 'icon:exec.png'
    clear_data_icon = CLEAR_DATA_ACTION, 'icon:remove.png'
    exit_icon = EXIT_ACTION, 'icon:exit.png'
    help_icon = HELP_ACTION, 'icon:help.png'
    about_icon = ABOUT_ACTION, 'icon:about.png'

    # 右键菜单 icon
    # sql conn
    open_conn_icon = OPEN_CONN_ACTION, 'icon:exec.png'
    cancel_open_conn_icon = CANCEL_OPEN_CONN_ACTION, 'icon:exec.png'
    refresh_conn_icon = REFRESH_CONN_ACTION, 'icon:exec.png'
    cancel_refresh_conn_icon = CANCEL_REFRESH_CONN_ACTION, 'icon:exec.png'
    close_conn_icon = CLOSE_CONN_ACTION, 'icon:exec.png'
    test_conn_icon = TEST_CONN_ACTION, 'icon:exec.png'
    cancel_test_conn_icon = CANCEL_TEST_CONN_ACTION, 'icon:exec.png'
    add_conn_icon = ADD_CONN_ACTION, 'icon:exec.png'
    edit_conn_icon = EDIT_CONN_ACTION, 'icon:exec.png'
    del_conn_icon = DEL_CONN_ACTION, 'icon:exec.png'
    # sql db
    open_db_icon = OPEN_DB_ACTION, 'icon:exec.png'
    cancel_open_db_icon = CANCEL_OPEN_DB_ACTION, 'icon:exec.png'
    close_db_icon = CLOSE_DB_ACTION, 'icon:exec.png'
    select_all_tb_icon = SELECT_ALL_TB_ACTION, 'icon:exec.png'
    unselect_tb_icon = UNSELECT_TB_ACTION, 'icon:exec.png'
    refresh_db_icon = REFRESH_DB_ACTION, 'icon:exec.png'
    cancel_refresh_db_icon = CANCEL_REFRESH_DB_ACTION, 'icon:exec.png'
    # sql tb
    open_table_icon = OPEN_TABLE_ACTION, 'icon:exec.png'
    cancel_open_table_icon = CANCEL_OPEN_TABLE_ACTION, 'icon:exec.png'
    close_table_icon = CLOSE_TABLE_ACTION, 'icon:exec.png'
    select_all_field_icon = SELECT_ALL_FIELD_ACTION, 'icon:exec.png'
    unselect_field_icon = UNSELECT_FIELD_ACTION, 'icon:exec.png'
    refresh_tb_icon = REFRESH_TB_ACTION, 'icon:exec.png'
    cancel_refresh_tb_icon = CANCEL_REFRESH_TB_ACTION, 'icon:exec.png'

    # struct
    cancel_open_struct_icon = CANCEL_OPEN_STRUCT_ACTION, 'icon:refresh.png'
    open_struct_icon = OPEN_STRUCT_ACTION, 'icon:exec.png'
    close_struct_icon = CLOSE_STRUCT_ACTION, 'icon:wrong.png'
    edit_struct_icon = EDIT_STRUCT_ACTION, 'icon:right.png'
    del_struct_icon = DEL_STRUCT_ACTION, 'icon:remove.png'
    refresh_struct_icon = REFRESH_STRUCT_ACTION, 'icon:remove.png'
    cancel_refresh_struct_icon = CANCEL_REFRESH_STRUCT_ACTION, 'icon:remove.png'
    select_all_icon = SELECT_ALL_ACTION, 'icon:remove.png'
    unselect_icon = UNSELECT_ACTION, 'icon:remove.png'
    refresh_folder_icon = REFRESH_FOLDER_ACTION, 'icon:remove.png'
    cancel_refresh_folder_icon = CANCEL_REFRESH_FOLDER_ACTION, 'icon:remove.png'

    # 列表元素右键
    edit_list_item_icon = EDIT_LIST_ITEM_ICON, 'icon:refresh.png'
    del_list_item_icon = DEL_LIST_ITEM_ICON, 'icon:remove.png'
    del_all_list_items_icon = DEL_ALL_LIST_ITEMS_ICON, 'icon:remove.png'
    export_item_icon = EXPORT_ITEM_ICON, 'icon:right.png'

    # table
    expand_child_table_icon = EXPAND_CHILD_TABLE_ICON, 'icon:add.png'
    collapse_child_table_icon = COLLAPSE_CHILD_TABLE_ICON, 'icon:remove.png'

    # ds category icon
    sql_ds_icon = SQL_DS_CATEGORY, 'icon:add.png'
    struct_ds_icon = STRUCT_DS_CATEGORY, 'icon:add.png'

    # sql ds icon
    # sqlite
    sql_sqlite_conn_icon = SQLITE_DISPLAY_NAME, 'icon:sqlite_conn_icon.png'
    sql_sqlite_db_icon = SQLITE_DB, 'icon:database_icon.png'
    sql_sqlite_tb_icon = SQLITE_TB, 'icon:table_icon.png'
    sql_sqlite_col_icon = SQLITE_COL, 'icon:column_icon.png'
    # mysql
    sql_mysql_conn_icon = MYSQL_DISPLAY_NAME, 'icon:mysql_conn_icon.png'
    sql_mysql_db_icon = MYSQL_DB, 'icon:database_icon.png'
    sql_mysql_tb_icon = MYSQL_TB, 'icon:table_icon.png'
    sql_mysql_col_icon = MYSQL_COL, 'icon:column_icon.png'
    # oracle
    sql_oracle_conn_icon = ORACLE_DISPLAY_NAME, 'icon:oracle_conn_icon.png'
    sql_oracle_db_icon = ORACLE_DB, 'icon:template.png'
    sql_oracle_tb_icon = ORACLE_TB, 'icon:table_icon.png'
    sql_oracle_col_icon = ORACLE_COL, 'icon:column_icon.png'

    # struct ds icon
    json_type_icon = JSON_DISPLAY_NAME, 'icon:json_icon.png'
    struct_col_icon = STRUCT_COL_ICON, 'icon:column_icon.png'
    new_folder_icon = CREATE_NEW_FOLDER_ACTION, 'icon:add.png'
    rename_folder_icon = RENAME_FOLDER_ACTION, 'icon:exec.png'
    del_folder_icon = DEL_FOLDER_ACTION, 'icon:remove.png'

    # 通用表格最后一列操作 icon
    row_operation_icon = ROW_OPERATION_ICON, 'icon:right.png'
    row_cat_edit_icon = ROW_CAT_EDIT_ICON, 'icon:exec.png'
    row_del_icon = ROW_DEL_ICON, 'icon:remove.png'
    # 复制 icon
    row_copy_icon = ROW_COPY_ICON, 'icon:add.png'
    # 导出表格 导出 icon
    row_export_icon = ROW_EXPORT_ICON, 'icon:right.png'

    # 预览生成页，树结构 icon
    preview_tree_file_icon = PREVIEW_TREE_FILE_ICON, 'icon:table_icon.png'


def get_icon_path(name):
    for icon_enum in IconEnum:
        if icon_enum.value[0] == name:
            return icon_enum.value[1]
    # 如果获取不到，给个默认值，创建一个空icon对象，避免程序出错
    return 'default_icon_path'


def create_icon(icon_path, name):
    """创建icon方法，为了保证在系统中，同样的icon，只存在一个，减少重复对象"""
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
