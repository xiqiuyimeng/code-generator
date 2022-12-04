# -*- coding: utf-8 -*-
from constant.constant import NO_SELECTED_DATA, GENERATE_ACTION, SQL_DATASOURCE_TYPE, STRUCT_DATASOURCE_TYPE
from view.box.message_box import pop_ok
from view.dialog.generator.confirm_selected.sql_confirm_selected_dialog import SqlConfirmSelectedDialog
from view.tree.tree_widget.tree_function import add_conn_func, add_struct_func

_author_ = 'luwt'
_date_ = '2022/5/29 16:51'


def open_conn_dialog(sql_type_action, tree_widget, screen_rect):
    """
    打开添加连接子窗口
    :param sql_type_action: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param screen_rect: 父窗口大小
    """
    add_conn_func(sql_type_action.text(), tree_widget, screen_rect)


def open_structure_dialog(struct_type_action, tree_widget, screen_rect,
                          parent_opened_item, parent_item):
    """
    打开添加结构体子窗口
    :param struct_type_action: 用来标识结构体数据源类型
    :param tree_widget: 树对象
    :param screen_rect: 父窗口大小
    """
    add_struct_func(struct_type_action.text(), tree_widget, screen_rect,
                    parent_opened_item, parent_item)


def generate(main_window):
    # 取出当前保存的数据
    selected_data = main_window.central_widget.tree_frame.tree_widget.tree_data
    # 如果还未选择数据，应提示
    if not selected_data:
        pop_ok(NO_SELECTED_DATA, GENERATE_ACTION, main_window)
    else:
        if main_window.current_ds_type.name == SQL_DATASOURCE_TYPE:
            confirm_selected_dialog = SqlConfirmSelectedDialog(selected_data, main_window.geometry())
            confirm_selected_dialog.exec()
        elif main_window.current_ds_type.name == STRUCT_DATASOURCE_TYPE:
            pass


def clear_data(main_window):
    tree_widget = main_window.central_widget.tree_frame.tree_widget
    # 取出当前保存的数据
    selected_data = tree_widget.tree_data
    # 清空数据
    selected_data.clear_tree()
    # 设置树的复选框为非选中，并检查是否有打开的表，将状态同步到表格复选框，保存树和表格复选框状态
    tree_widget.set_tree_unchecked()
