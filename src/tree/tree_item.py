# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem


_author_ = 'luwt'
_date_ = '2020/9/8 16:40'


class MyTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, tree, parent):
        """
        自定义树节点类，重写setData方法，完成点击复选框事件，
        参考自https://stackoverflow.com/questions/9686648/is-it-possible-to-create-a-signal-for-when-a-qtreewidgetitem-checkbox-is-toggled
        """
        super().__init__(parent)
        self.tree = tree

    def setData(self, column: int, role: int, value):
        # 当点击位置为复选框，且值已经改变，发送信号
        check_change = self.tree.checkbox_clicked \
                       and column == 0 \
                       and role == Qt.CheckStateRole \
                       and self.checkState(0) != value
        super().setData(column, role, value)
        if check_change:
            self.tree.item_checkbox_clicked.emit(self, value)
            # 复原树控件中标志项
            self.tree.checkbox_clicked = False

    def setText(self, column, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(column, text)

