# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QObject, QEvent, QPoint
from PyQt6.QtWidgets import QTableWidget, QFrame, QToolTip, QAbstractItemView

from src.view.custom_widget.scrollable_widget import ScrollableWidget
from src.view.table.table_item.table_item import TableWidgetItem

_author_ = 'luwt'
_date_ = '2023/2/13 11:38'


class TableWidgetABC(QTableWidget, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signal()
        # 安装监听器
        self.installEventFilter(self)

    def setup_ui(self):
        # 设置无边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        # 隐藏网格线
        self.setShowGrid(False)
        # 去除选中时虚线框
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 交替行颜色
        self.setAlternatingRowColors(True)
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)
        # 只能单选
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.setup_other_ui()

    def setup_other_ui(self):
        ...

    def fill_table(self, *args):
        ...

    def connect_signal(self):
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)
        self.connect_other_signal()

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self and event.type() == QEvent.Type.ToolTip:
            # self.indexAt(pos).isValid()，计算规则是默认隐藏了表头，所以需要减去表头高度，才是真实单元格的位置
            horizontal_header_pos = QPoint(0, self.horizontalHeader().height())
            index = self.indexAt(event.pos() - horizontal_header_pos)
            # 索引有效，且索引处部件为空，证明当前是正常的内容单元格，否则为控件单元格
            if index.isValid() and self.indexWidget(index) is None:
                # 设置气泡提示，向下略微偏移一些，以免鼠标挡住提示文字
                QToolTip.showText(QPoint(event.globalPos().x() + 5, event.globalPos().y() + 10), self.toolTip())
            return True
        return super().eventFilter(obj, event)

    def connect_other_signal(self):
        ...

    def make_item(self, text=None):
        item = TableWidgetItem(self)
        item.setText(text)
        return item

    def insert_row(self, row_index):
        self.insertRow(row_index)
        # 行高设为原行高的1.5倍，主要为了美观
        self.setRowHeight(row_index, round(self.rowHeight(row_index) * 1.5))
