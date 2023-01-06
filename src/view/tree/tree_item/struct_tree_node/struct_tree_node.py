# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from constant.constant import EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, CANCEL_OPEN_STRUCT_ACTION, OPEN_STRUCT_ACTION, \
    CLOSE_STRUCT_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_struct_executor import *
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record, get_item_opened_tab, set_item_opened_tab, \
    link_table_checkbox, save_tree_data, get_add_del_data
from view.tree.tree_widget.tree_function import edit_struct_func

_author_ = 'luwt'
_date_ = '2022/12/2 12:09'


class StructTreeNode(AbstractStructTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.struct_name = self.item.text(0)
        self.open_struct_executor: OpenStructExecutor = ...
        self.is_opening = False
        # 打开数据是不会变的
        self.opened_item = get_item_opened_record(self.item)

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.window.struct_tab_widget.setCurrentWidget(tab_widget)
        else:
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            self.open_struct_executor = globals()[self.opened_item.data_type.parse_executor](
                self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_struct_executor.start()

    def open_item_ui(self, table_tab):
        tab = self.reopen_item(table_tab)
        self.window.struct_tab_widget.setCurrentWidget(tab)
        self.is_opening = False

    def open_item_fail(self):
        self.is_opening = False

    def reopen_item(self, table_tab):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item)
        self.window.struct_tab_widget.addTab(tab, self.struct_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
            lambda check_state: self.set_check_state(check_state))
        return tab

    def close_item(self):
        super().close_item()

    def change_check_box(self, check_state):
        # 保存复选框状态变化
        self.save_check_state()
        # 联动表格内的复选框
        link_table_checkbox(self.item, check_state)

    def do_fill_menu(self, menu):
        # 打开
        open_struct_action = CANCEL_OPEN_STRUCT_ACTION \
            if self.is_opening else OPEN_STRUCT_ACTION \
            if not self.item.childCount() else CLOSE_STRUCT_ACTION
        menu.addAction(QAction(get_icon(open_struct_action), open_struct_action.format(self.struct_name), menu))
        menu.addSeparator()

        # 编辑
        menu.addAction(QAction(get_icon(EDIT_STRUCT_ACTION),
                               EDIT_STRUCT_ACTION.format(self.struct_name), menu))
        # 删除
        menu.addAction(QAction(get_icon(DEL_STRUCT_ACTION),
                               DEL_STRUCT_ACTION.format(self.struct_name), menu))

    def handle_menu_func(self, func):
        # 打开结构体
        if func == OPEN_STRUCT_ACTION.format(self.struct_name):
            self.open_item()
        # 取消打开结构体
        elif func == CANCEL_OPEN_STRUCT_ACTION.format(self.struct_name):
            self.open_struct_executor.worker_terminate(self.open_item_fail)
        # 关闭结构体
        elif func == CLOSE_STRUCT_ACTION.format(self.struct_name):
            pass
        # 编辑结构体
        elif func == EDIT_STRUCT_ACTION.format(self.struct_name):
            edit_struct_func(self.opened_item.data_type.display_name, self.tree_widget,
                             self.window.geometry(), self.opened_item.id)
        # 删除结构体
        elif func == DEL_STRUCT_ACTION.format(self.struct_name):
            pass

    def close_tab_callback(self):
        # 清空列数据，提供给tab bar调用，在关闭tab时调用
        if self.item.checkState(0):
            del_data = get_add_del_data(self.item)
            self.tree_widget.tree_data.clear_node_children(del_data)

    def set_check_state(self, check_state):
        self.item.setCheckState(0, check_state)
        self.save_check_state()

    def save_check_state(self):
        # 保存选中数据
        save_tree_data(self.item, self.tree_widget.tree_data)
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def worker_terminate(self):
        if self.open_struct_executor is not Ellipsis:
            self.open_struct_executor.worker_terminate()
