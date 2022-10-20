# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from constant.constant import CANCEL_OPEN_TABLE_MENU, OPEN_TABLE_MENU, CLOSE_TABLE_MENU
from service.async_func.async_sql_ds_task import OpenTBExecutor
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_widget.tree_item_func import get_item_opened_tab, \
    set_item_opened_tab

_author_ = 'luwt'
_date_ = '2022/7/6 22:05'


class TableTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.table_name = self.item.text(0)
        if not hasattr(self, 'open_tb_executor'):
            self.open_tb_executor: OpenTBExecutor = ...

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.window.sql_tab_widget.setCurrentWidget(tab_widget)
        else:
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_tb_executor.start()

    def open_item_ui(self, table_tab):
        tab = self.reopen_item(table_tab)
        self.window.sql_tab_widget.setCurrentWidget(tab)
        self.is_opening = False

    def reopen_item(self, table_tab):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item)
        self.window.sql_tab_widget.addTab(tab, self.table_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state\
            .connect(lambda check_state: self.set_check_state(check_state))
        return tab

    def open_item_fail(self):
        self.is_opening = False

    def close_item(self):
        tab = get_item_opened_tab(self.item)
        if tab:
            index = self.window.sql_tab_widget.indexOf(tab)
            tab_bar = self.window.sql_tab_widget.tab_bar
            if tab_bar.table_allow_close((index, )):
                # 删除tab
                tab_bar.remove_tab(index)

    def change_check_box(self, check_state):
        # 保存复选框状态变化
        self.save_check_state()
        # 联动表格内的复选框
        tab = get_item_opened_tab(self.item)
        if tab:
            tab.table_frame.table_widget.table_header.change_header_state(check_state)

    def save_check_state(self):
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def set_check_state(self, check_state):
        self.item.setCheckState(0, check_state)
        self.save_check_state()

    def do_fill_menu(self, menu):
        open_menu_name = CANCEL_OPEN_TABLE_MENU.format(self.table_name) \
            if self.is_opening else OPEN_TABLE_MENU.format(self.table_name) \
            if not get_item_opened_tab(self.item) else CLOSE_TABLE_MENU.format(self.table_name)

        menu.addAction(QAction(open_menu_name.format(self.table_name), menu))

    def handle_menu_func(self, func):
        # 打开表
        if func == OPEN_TABLE_MENU.format(self.table_name):
            self.open_item()
        # 取消打开表
        elif func == CANCEL_OPEN_TABLE_MENU.format(self.table_name):
            self.open_tb_executor.worker_terminate(self.open_item_fail)
        # 关闭表
        elif func == CLOSE_TABLE_MENU.format(self.table_name):
            self.close_item()

    def worker_terminate(self):
        if self.open_tb_executor is not Ellipsis:
            self.open_tb_executor.worker_terminate()
