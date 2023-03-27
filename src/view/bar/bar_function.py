# -*- coding: utf-8 -*-
from src.constant.bar_constant import NO_SELECTED_DATA, GENERATE_ACTION, SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.constant.generator_dialog_constant import SQL_CONFIRM_SELECTED_HEADER_TXT, \
    STRUCTURE_CONFIRM_SELECTED_HEADER_TXT
from src.view.box.message_box import pop_ok
from src.view.dialog.generator.confirm_selected.sql_confirm_selected_dialog import SqlConfirmSelectedDialog
from src.view.dialog.generator.confirm_selected.structure_confirm_selected_dialog import StructureConfirmSelectedDialog
from src.view.dialog.template.template_dialog import TemplateDialog
from src.view.dialog.type_mapping.type_mapping_dialog import TypeMappingDialog
from src.view.tree.tree_widget.tree_function import add_conn_func, add_struct_func

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
    :param parent_opened_item
    :param parent_item
    """
    add_struct_func(struct_type_action.text(), tree_widget, screen_rect,
                    parent_opened_item, parent_item)


def refresh(main_window):
    # 找出当前节点
    item = main_window.central_widget.tree_frame.tree_widget.currentItem()
    if item:
        main_window.central_widget.tree_frame.tree_widget.refresh(item)


def open_type_mapping_dialog(main_window):
    """打开类型映射对话框"""
    TypeMappingDialog(main_window.geometry()).exec()


def open_template_dialog(main_window):
    """打开模板对话框"""
    TemplateDialog(main_window.geometry()).exec()


def generate(main_window):
    # 取出当前保存的数据
    selected_data = main_window.central_widget.tree_frame.tree_widget.tree_data
    # 如果还未选择数据，应提示
    if not selected_data:
        pop_ok(NO_SELECTED_DATA, GENERATE_ACTION, main_window)
    else:
        if main_window.current_ds_category.name == SQL_DS_CATEGORY:
            confirm_selected_dialog = SqlConfirmSelectedDialog(selected_data, main_window.geometry(),
                                                               SQL_CONFIRM_SELECTED_HEADER_TXT)
            confirm_selected_dialog.exec()
        elif main_window.current_ds_category.name == STRUCT_DS_CATEGORY:
            confirm_selected_dialog = StructureConfirmSelectedDialog(selected_data, main_window.geometry(),
                                                                     STRUCTURE_CONFIRM_SELECTED_HEADER_TXT)
            confirm_selected_dialog.exec()


def clear_data(main_window):
    tree_widget = main_window.central_widget.tree_frame.tree_widget
    # 取出当前保存的数据
    selected_data = tree_widget.tree_data
    # 清空数据
    selected_data.clear_tree()
    # 设置树的复选框为非选中，并检查是否有打开的表，将状态同步到表格复选框，保存树和表格复选框状态
    tree_widget.set_tree_unchecked()
