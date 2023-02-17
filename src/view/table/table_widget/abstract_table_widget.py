# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QFrame

from src.view.custom_widget.scrollable_widget import ScrollableWidget
from src.view.table.table_item import TableWidgetItem

_author_ = 'luwt'
_date_ = '2023/2/13 11:38'


class AbstractTableWidget(QTableWidget, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
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
        # 按像素滚动
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setup_other_ui()

    def setup_other_ui(self): ...

    def fill_table(self, *args): ...

    def connect_signal(self):
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)
        self.connect_other_signal()

    def connect_other_signal(self): ...

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def make_item(self, text):
        item = TableWidgetItem(self)
        item.setText(text if text else '')
        return item

