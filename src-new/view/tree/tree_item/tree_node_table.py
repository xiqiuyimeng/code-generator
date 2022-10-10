# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from constant.constant import CANCEL_OPEN_TABLE_MENU, OPEN_TABLE_MENU, CLOSE_TABLE_MENU
from service.async_func.async_sql_ds_task import OpenTBExecutor
from view.tab.tab_ui import TabTableUI
from view.table.table_function import resize_table_rows
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_widget.tree_item_func import set_item_opening_flag, set_item_opening_worker, get_item_opened_tab, \
    set_item_opened_tab

_author_ = 'luwt'
_date_ = '2022/7/6 22:05'


class TableTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.table_name = self.item.text(0)
        self.open_tb_executor = ...

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.window.sql_tab_widget.setCurrentWidget(tab_widget)
        else:
            # 执行打开tab页, 设置正在打开中状态
            set_item_opening_flag(self.item, True)
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            set_item_opening_worker(self.item, self.open_tb_executor)
            self.open_tb_executor.start()

    def open_item_ui(self, column_list):
        set_item_opening_flag(self.item, False)
        tab = self.reopen_item(column_list)
        self.window.sql_tab_widget.setCurrentWidget(tab)

    def reopen_item(self, col_list):
        # 创建tab页
        tab = TabTableUI(self.window, col_list, self.item)
        self.window.sql_tab_widget.addTab(tab, self.table_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        return tab

    def open_item_fail(self):
        set_item_opening_flag(self.item, False)

    def close_item(self):
        self.window.tab_frame.setHidden(True)
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
