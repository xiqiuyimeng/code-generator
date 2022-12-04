# -*- coding: utf-8 -*-
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode

_author_ = 'luwt'
_date_ = '2022/12/2 12:09'


class StructTreeNode(AbstractStructTreeNode):

    def open_item(self):
        super().open_item()

    def open_item_ui(self, *args):
        super().open_item_ui(*args)

    def open_item_fail(self):
        super().open_item_fail()

    def reopen_item(self, opened_items):
        super().reopen_item(opened_items)

    def close_item(self):
        super().close_item()

    def change_check_box(self, check_state):
        super().change_check_box(check_state)

    def do_fill_menu(self, menu):
        super().do_fill_menu(menu)

    def handle_menu_func(self, func):
        super().handle_menu_func(func)

    def worker_terminate(self):
        super().worker_terminate()
