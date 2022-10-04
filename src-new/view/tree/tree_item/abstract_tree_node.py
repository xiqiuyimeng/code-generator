# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidgetItem

_author_ = 'luwt'
_date_ = '2022/7/6 22:08'


class AbstractTreeNode:

    def __init__(self, item: QTreeWidgetItem, tree_widget, window):
        self.item = item
        self.tree_widget = tree_widget
        self.window = window

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def reopen_item(self, opened_items): ...

    def close_item(self): ...

    def change_check_box(self, check_state): ...

    def do_fill_menu(self, menu): ...

    def handle_menu_func(self, func): ...

