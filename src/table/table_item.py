# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

_author_ = 'luwt'
_date_ = '2020/9/9 10:13'


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, table):
        """自定义单元格项，重写setData方法，完成点击复选框事件"""
        self.table = table
        super().__init__()

    def setData(self, role, value):
        check_change = self.table.checkbox_clicked \
                       and role == Qt.CheckStateRole \
                       and value != self.checkState()
        super().setData(role, value)
        if check_change:
            # 字段在复选框右侧的一列
            field = self.table.item(self.row(), self.column() + 1).text()
            self.table.item_checkbox_clicked.emit(value, field)
            self.table.checkbox_clicked = False
