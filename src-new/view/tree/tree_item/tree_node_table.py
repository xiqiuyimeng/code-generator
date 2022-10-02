# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from constant.constant import CANCEL_OPEN_TABLE_MENU, OPEN_TABLE_MENU, CLOSE_TABLE_MENU
from service.async_func.async_sql_ds_task import OpenTBExecutor
from view.table.table_function import fill_table, resize_table_rows
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode

_author_ = 'luwt'
_date_ = '2022/7/6 22:05'


class TableTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.table_name = self.item.text(0)
        self.open_tb_executor = ...

    def open_item(self):
        # 如果当前节点没有打开表，在执行打开
        if self.window.table_widget.tree_item is not self.item:
            # 设置正在打开中状态
            self.item.setData(1, Qt.UserRole, True)
            self.window.table_widget.tree_item = self.item
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            self.item.setData(1, Qt.UserRole + 1, self.open_tb_executor)
            self.open_tb_executor.start()

    def open_item_ui(self, column_list):
        self.item.setData(1, Qt.UserRole, False)
        self.window.table_frame.setHidden(False)
        fill_table(self.window.table_widget, column_list)

    def open_item_fail(self):
        self.item.setData(1, Qt.UserRole, False)

    def close_item(self):
        self.window.table_frame.setHidden(True)
        # 将表格行数置位0
        resize_table_rows(0, self.window.table_widget)
        self.window.table_widget.tree_item = None

    def change_check_box(self, check_state):
        ...

    def do_fill_menu(self, menu):
        return [
            # 根据是否在打开中标识
            CANCEL_OPEN_TABLE_MENU.format(self.table_name)
            if self.item.data(1, Qt.UserRole) else OPEN_TABLE_MENU.format(self.table_name)
            if self.window.table_widget.tree_item is not self.item else CLOSE_TABLE_MENU.format(self.table_name)
        ]

    def handle_menu_func(self, func):
        # 打开表
        if func == OPEN_TABLE_MENU.format(self.table_name):
            self.open_item()
        # 取消打开表
        elif func == CANCEL_OPEN_TABLE_MENU.format(self.table_name):
            self.item.data(1, Qt.UserRole + 1).worker_terminate(self.open_item_fail)
        # 关闭表
        elif func == CLOSE_TABLE_MENU.format(self.table_name):
            pass
