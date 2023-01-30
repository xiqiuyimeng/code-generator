# -*- coding: utf-8 -*-

from view.tree.tree_item.abstract_tree_node import AbstractTreeNode

_author_ = 'luwt'
_date_ = '2022/7/6 22:08'


class AbstractSqlTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.is_opening = False

    def open_item_fail(self):
        self.is_opening = False

