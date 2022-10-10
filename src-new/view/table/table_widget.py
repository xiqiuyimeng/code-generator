# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView

from constant_.constant import TABLE_HEADER_LABELS
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.table.table_header import CheckBoxHeader
from view.table.table_item import TableWidgetItem

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
        self.setColumnCount(6)
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

    def fill_table(self, cols):
        """
        将列名字段全数填充在表中，四列多行表
        :param cols: 字段信息的数组
        """
        # 填充数据
        for i, col in enumerate(cols):
            # 插入新的一行
            self.insertRow(i)
            # 设置checkbox在第一列
            table_check_item = TableWidgetItem(self)
            if col.checked:
                check_status = Qt.Checked
            else:
                check_status = Qt.Unchecked
            table_check_item.setCheckState(check_status)
            # 加上行号
            table_check_item.setText(i + 1)
            self.setItem(i, 0, table_check_item)
            # gui.table_header.all_header_combobox.append(table_check_item)

            self.setItem(i, 1, self.make_item(col.col_name))
            self.setItem(i, 2, self.make_item(col.data_type))
            self.setItem(i, 3, self.make_item(col.full_data_type))
            self.setItem(i, 4, self.make_item(col.is_pk))
            self.setItem(i, 5, self.make_item(col.col_comment))
        # 设置表格根据内容调整行高
        self.resizeRowsToContents()

    def make_item(self, text):
        item = TableWidgetItem(self)
        item.setText(text)
        return item
