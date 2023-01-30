# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidgetItem

from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.tree_item_func import get_item_opened_record, set_item_opened_tab

_author_ = 'luwt'
_date_ = '2022/12/2 11:36'


class AbstractTreeNode:

    def __new__(cls, item: QTreeWidgetItem, tree_widget, window):
        if not hasattr(item, 'tree_node'):
            item.tree_node = object.__new__(cls)
            # 打开数据是不会变的
            item.tree_node.opened_item = get_item_opened_record(item)
        return item.tree_node

    def __init__(self, item: QTreeWidgetItem, tree_widget, window):
        self.item = item
        self.tree_widget = tree_widget
        self.window = window
        self.is_refreshing = False

    def refresh_success(self, *args):
        self.is_refreshing = False

    def refresh_fail(self):
        self.is_refreshing = False

    def reopen_tab(self, table_tab, tab_name, check_state_func):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item, self.tree_widget)
        self.tree_widget.get_current_tab_widget().addTab(tab, tab_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
            lambda check_state: check_state_func(check_state))
        return tab

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def reopen_item(self, opened_items): ...

    def close_item(self): ...

    def change_check_box(self, check_state, clicked): ...

    def do_fill_menu(self, menu): ...

    def handle_menu_func(self, func): ...

    def refresh(self): ...

    def worker_terminate(self): ...
