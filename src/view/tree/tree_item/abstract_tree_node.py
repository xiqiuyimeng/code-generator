# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidgetItem

from view.tree.tree_item.tree_item_func import get_item_opened_record

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
