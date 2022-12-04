# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidgetItem

_author_ = 'luwt'
_date_ = '2022/12/2 11:36'


class AbstractTreeNode:

    def __new__(cls, item: QTreeWidgetItem, tree_widget, window):
        if not hasattr(item, 'node'):
            item.node = object.__new__(cls)
        return item.node

    def __init__(self, item: QTreeWidgetItem, tree_widget, window):
        self.item = item
        self.tree_widget = tree_widget
        self.window = window
