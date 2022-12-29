# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

_author_ = 'luwt'
_date_ = '2022/5/10 15:27'


class TableWidgetItem(QTableWidgetItem):

    def __init__(self, table):
        """自定义单元格项"""
        self.table = table
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)
