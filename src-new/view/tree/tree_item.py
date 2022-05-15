# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

_author_ = 'luwt'
_date_ = '2022/5/10 14:58'


class TreeWidgetItem(QTreeWidgetItem):

    def __init__(self, tree, parent):
        """
        自定义树节点类，重写setData方法，完成点击复选框事件，
        参考自https://stackoverflow.com/questions/9686648/is-it-possible-to-create-a-signal-for-when-a-qtreewidgetitem-checkbox-is-toggled
        """
        super().__init__(parent)
        self.tree = tree

    def setData(self, column: int, role: int, value):
        # 如果是第一列，操作角色为复选框，非初始化阶段，值改变的情况下，发送信号
        check_change = column == 0 \
                       and role == Qt.CheckStateRole \
                       and self.data(column, role).isValid() \
                       and value != self.checkState(0)
        super().setData(column, role, value)
        if check_change:
            self.tree.item_checkbox_clicked.emit(self, value)

    def setText(self, column, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(column, text)
