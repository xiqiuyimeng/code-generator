# -*- coding: utf-8 -*-

from view.tree.tree_item.abstract_tree_node import AbstractTreeNode

_author_ = 'luwt'
_date_ = '2022/12/2 11:32'


class AbstractStructTreeNode(AbstractTreeNode):

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def reopen_item(self, opened_items): ...

    def close_item(self): ...

    def change_check_box(self, check_state, clicked): ...

    def do_fill_menu(self, menu): ...

    def handle_menu_func(self, func): ...

    def set_check_state(self, *args): ...

    def link_parent_node(self):
        # 联动父节点变化
        if self.item.parent():
            parent_node = self.item.parent().tree_node
            parent_node.set_check_state()

    def worker_terminate(self): ...
