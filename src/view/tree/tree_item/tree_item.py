# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem

from src.view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/12/9 17:50'


class TreeWidgetItem(QTreeWidgetItem):

    def __init__(self, tree, parent):
        """
        自定义树节点类，重写setData方法，完成点击复选框事件
        """
        super().__init__(parent)
        self.tree = tree

    def setData(self, column: int, role: int, value):
        # 当前树节点点击，且值已经改变，发送信号
        check_change = self.tree.item_clicked \
                       and self.tree.clicked_item is not Ellipsis \
                       and self.tree.clicked_item is self \
                       and column == 0 \
                       and role == Qt.ItemDataRole.CheckStateRole \
                       and self.checkState(0) != value
        super().setData(column, role, value)
        if check_change:
            self.tree.item_checkbox_clicked.emit(self)

    def __lt__(self, other):
        """重载操作符，实现自定义排序"""
        return get_item_opened_record(self).item_order < get_item_opened_record(other).item_order
