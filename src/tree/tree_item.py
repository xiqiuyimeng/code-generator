﻿# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem


_author_ = 'luwt'
_date_ = '2020/9/8 16:40'


class MyTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, tree, parent):
        """自定义树节点类，重写setData方法，完成点击复选框事件"""
        super().__init__(parent)
        self.tree = tree

    def setData(self, column: int, role: int, value):
        # 当点击位置为复选框，且值已经改变，发送信号
        check_change = column == 0 and role == Qt.CheckStateRole and self.checkState(0) != value
        super().setData(column, role, value)
        if check_change:
            self.tree.item_checkbox_clicked.emit(self, value)

