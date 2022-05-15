# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget

from view.custom_widget.scrollable_widget import ScrollableWidget

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class TableWidget(QTableWidget, ScrollableWidget):

    # 定义信号，点击第一列复选框时，发送当前选中状态、第二列的字段名称和当前行
    item_checkbox_clicked = pyqtSignal(bool, str, int)
