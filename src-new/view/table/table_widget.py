# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView

from constant_.constant import TABLE_HEADER_LABELS
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.table.table_header import CheckBoxHeader

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class TableWidget(QTableWidget, ScrollableWidget):

    # 定义信号，点击第一列复选框时，发送当前选中状态、第二列的字段名称和当前行
    item_checkbox_clicked = pyqtSignal(bool, str, int)

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.tree_item = None
        self.table_header = ...

    def setup_ui(self):
        # 设置只读表格
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 交替行颜色
        self.setAlternatingRowColors(True)

        # 表格设置为4列
        self.setColumnCount(4)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader()
        self.table_header.setObjectName("table_header")
        # 设置表头
        self.setHorizontalHeader(self.table_header)
        # 设置表头字段
        self.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
        # 设置表头列宽度，第一列全选列
        self.horizontalHeader().resizeSection(0, 60)
        # 第二列字段列，根据大小自动调整宽度
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 最后备注列拉伸到最大
        self.horizontalHeader().setStretchLastSection(True)
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)
