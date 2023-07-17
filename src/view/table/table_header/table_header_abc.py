# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QAbstractItemView

from src.constant.table_constant import TABLE_HEADER_FIRST_COL_LABEL
from src.view.custom_widget.check_box import CheckBox
from src.view.table.table_item.table_item import make_checkbox_num_widget
from src.view.table.table_widget.table_widget_abc import TableWidgetABC

_author_ = 'luwt'
_date_ = '2023/2/28 14:18'


class TableHeaderABC(TableWidgetABC):
    # 表头复选框点击信号
    header_clicked = pyqtSignal(Qt.CheckState)
    # 表头复选框变化信号
    header_check_changed = pyqtSignal(Qt.CheckState)

    def __init__(self, row_count, column_count, parent_table: TableWidgetABC, *args):
        self.row_count = row_count
        self.column_count = column_count
        self.parent_table = parent_table
        self.check_box: CheckBox = ...
        super().__init__(*args)

    def setup_other_ui(self):
        # 表头隐藏
        self.horizontalHeader().setHidden(True)
        # 不可编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # 设置不可选中
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # 关闭交替行颜色
        self.setAlternatingRowColors(False)
        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 行数
        self.setRowCount(self.row_count)
        # 列数
        self.setColumnCount(self.column_count)

        # 隐藏空白行列
        for idx in range(self.row_count, self.rowCount()):
            self.setRowHidden(idx, True)
        for idx in range(self.column_count, self.columnCount()):
            self.setColumnHidden(idx, True)

        # 设置表头字体
        font = self.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        self.setFont(font)

        # 单元格合并样式
        self.setup_item_span()
        # 设置单元格
        self.setup_items()

    def setup_item_span(self):
        ...

    def setup_items(self):
        checkbox_num_widget = self.get_checkbox_num_widget()
        self.setCellWidget(0, 0, checkbox_num_widget)
        self.check_box = checkbox_num_widget.check_box
        self.setup_header_items()

    def get_checkbox_num_widget(self):
        return make_checkbox_num_widget(TABLE_HEADER_FIRST_COL_LABEL, self.click_header_checkbox)

    def click_header_checkbox(self, check_state):
        # 更改子项复选框状态
        self.change_child_check_state(check_state)
        # 发射点击信号
        self.header_clicked.emit(check_state)
        self.header_check_changed.emit(check_state)

    def setup_header_items(self):
        ...

    def change_child_check_state(self, check_state):
        for row_idx in range(self.parent_table.rowCount()):
            cell_widget = self.parent_table.cellWidget(row_idx, 0)
            if hasattr(cell_widget, 'check_box'):
                check_box = self.parent_table.cellWidget(row_idx, 0).check_box
                if check_box.checkState() != check_state:
                    check_box.setCheckState(check_state)

    def calculate_header_check_state(self):
        """根据父表中所有复选框的状态，计算表头复选框状态"""
        check_state_set = set()
        for row_idx in range(self.parent_table.rowCount()):
            cell_widget = self.parent_table.cellWidget(row_idx, 0)
            if hasattr(cell_widget, 'check_box'):
                check_state_set.add(cell_widget.check_box.checkState())
        if len(check_state_set) == 2:
            header_check_state = Qt.CheckState.PartiallyChecked
        elif len(check_state_set) == 1:
            header_check_state = check_state_set.pop()
        else:
            header_check_state = Qt.CheckState.Unchecked
        self.check_box.setCheckState(header_check_state)
        # 发射表头复选框变化信号
        self.header_check_changed.emit(header_check_state)

    def link_header_check_state(self, check_state):
        # 联动表头复选框状态
        self.check_box.setCheckState(check_state)
        # 设置子项
        self.change_child_check_state(check_state)

    def connect_other_signal(self):
        # 水平滚动条，和父表联动
        self.horizontalScrollBar().valueChanged.connect(self.parent_table.horizontalScrollBar().setValue)
        self.parent_table.horizontalScrollBar().valueChanged.connect(self.horizontalScrollBar().setValue)
