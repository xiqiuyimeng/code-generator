# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QFrame

from src.view.custom_widget.scrollable_widget import ScrollableWidget
from src.view.table.table_item.table_item import TableWidgetItem
from src.view.table.table_item.table_item_delegate import TextInputDelegate

_author_ = 'luwt'
_date_ = '2023/2/13 11:38'


class AbstractTableWidget(QTableWidget, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.text_input_delegate: TextInputDelegate = ...
        self.setup_ui()
        self.connect_signal()

    def setup_ui(self):
        # 设置无边框
        self.setFrameShape(QFrame.NoFrame)
        # 隐藏网格线
        self.setShowGrid(False)
        # 去除选中时虚线框
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 交替行颜色
        self.setAlternatingRowColors(True)
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)

        # 设置表头字体加粗
        font = self.horizontalHeader().font()
        # 比原字体略大一点
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        self.horizontalHeader().setFont(font)

        self.setup_other_ui()

    def setup_other_ui(self): ...

    def fill_table(self, *args): ...

    def connect_signal(self):
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)
        self.connect_other_signal()

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def connect_other_signal(self): ...

    def make_item(self, text=None):
        item = TableWidgetItem(self)
        item.setText(text if text else '')
        return item

    def set_text_input_delegate(self, columns):
        # 设置编辑器代理
        self.text_input_delegate = TextInputDelegate()
        [self.setItemDelegateForColumn(col, self.text_input_delegate) for col in columns]

    def insert_row(self, row_index):
        self.insertRow(row_index)
        # 行高设为原行高的1.5倍，主要为了美观
        self.setRowHeight(row_index, round(self.rowHeight(row_index) * 1.5))

