# -*- coding: utf-8 -*-

from view.tree.tree_item.abstract_tree_node import AbstractTreeNode

_author_ = 'luwt'
_date_ = '2022/7/6 22:08'


class AbstractSqlTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        if not hasattr(self, 'is_opening'):
            self.is_opening = False

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def reopen_item(self, opened_items): ...

    def close_item(self): ...

    def change_check_box(self, check_state): ...

    def do_fill_menu(self, menu): ...

    def handle_menu_func(self, func): ...

    def worker_terminate(self): ...

