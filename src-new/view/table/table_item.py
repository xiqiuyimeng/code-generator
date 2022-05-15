# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

_author_ = 'luwt'
_date_ = '2022/5/10 15:27'


class TableWidgetItem(QTableWidgetItem):

    def __init__(self, table):
        """自定义单元格项，重写setData方法，完成点击复选框事件"""
        self.table = table
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)

    def setData(self, role, value):
        # 与树节点处理逻辑相同
        check_change = self.data(role).isValid() \
                       and role == Qt.CheckStateRole \
                       and value != self.checkState()
        super().setData(role, value)
        if check_change:
            # 字段在复选框右侧的一列
            field = self.table.item(self.row(), self.column() + 1).text()
            self.table.item_checkbox_clicked.emit(value, field, self.row())

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)
