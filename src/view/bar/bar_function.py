# -*- coding: utf-8 -*-
from src.constant.bar_constant import NO_SELECTED_DATA, GENERATE_ACTION
from src.constant.help.help_constant import CENTRAL_HELP
from src.view.box.message_box import pop_ok
from src.view.dialog.generator.generator_dialog import GeneratorDialog
from src.view.dialog.help_dialog import HelpDialog
from src.view.dialog.template.template_dialog import TemplateDialog
from src.view.dialog.type_mapping.type_mapping_dialog import TypeMappingDialog
from src.view.tree.tree_widget.tree_function import add_conn_func, add_struct_func

_author_ = 'luwt'
_date_ = '2022/5/29 16:51'


def open_conn_dialog(sql_type_action):
    """
    打开添加连接子窗口
    :param sql_type_action: 用来标识sql数据源类型
    """
    add_conn_func(sql_type_action.text())


def open_struct_dialog(struct_type_action, parent_opened_item, parent_item):
    """
    打开添加结构体子窗口
    :param struct_type_action: 用来标识结构体数据源类型
    :param parent_opened_item
    :param parent_item
    """
    add_struct_func(struct_type_action.text(), parent_opened_item, parent_item)


def refresh(main_window):
    # 找出当前节点
    item = main_window.central_widget.tree_frame.tree_widget.currentItem()
    if item:
        main_window.central_widget.tree_frame.tree_widget.refresh(item)


def open_type_mapping_dialog():
    """打开类型映射对话框"""
    TypeMappingDialog().exec()


def open_template_dialog():
    """打开模板对话框"""
    TemplateDialog().exec()


def generate(main_window):
    # 取出当前保存的数据
    selected_data = main_window.central_widget.tree_frame.tree_widget.tree_data
    # 如果还未选择数据，应提示
    if not selected_data:
        pop_ok(NO_SELECTED_DATA, GENERATE_ACTION, main_window)
    else:
        confirm_selected_dialog = GeneratorDialog(main_window.current_ds_category.name,
                                                  selected_data, None)
        confirm_selected_dialog.exec()


def clear_data(main_window):
    tree_widget = main_window.central_widget.tree_frame.tree_widget
    # 取出当前保存的数据
    selected_data = tree_widget.tree_data
    # 清空数据
    selected_data.clear_tree()
    # 设置树的复选框为非选中，并检查是否有打开的表，将状态同步到表格复选框，保存树和表格复选框状态
    tree_widget.set_tree_unchecked()


def open_help_dialog():
    """打开帮助信息对话框"""
    HelpDialog(CENTRAL_HELP).exec()
