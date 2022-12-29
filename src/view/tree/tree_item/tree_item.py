# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

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
        # 当树节点点击，且值已经改变，发送信号
        check_change = self.tree.item_clicked \
                       and column == 0 \
                       and role == Qt.CheckStateRole \
                       and self.checkState(0) != value
        super().setData(column, role, value)
        if check_change:
            self.tree.item_checkbox_clicked.emit(self)
