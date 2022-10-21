# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget

from view.table.table_item import TableWidgetItem

_author_ = 'luwt'
_date_ = '2022/5/31 21:09'
    
    
def fill_table(table_widget, cols):
    """
    将列名字段全数填充在表中，四列多行表
    :param table_widget: 表格对象
    :param cols: 字段信息的数组，为二维数组
    """
    # 首先调整行数
    resize_table_rows(len(cols), table_widget)
    # 填充数据
    for i, col in enumerate(cols):
        for n, field in enumerate(col, start=1):
            # 建立一个新的对象，赋值，填充到表格中对应位置
            item = TableWidgetItem(table_widget)
            table_widget.setItem(i, n, item)
            item.setText(field)
    # 设置表格根据内容调整行高
    table_widget.resizeRowsToContents()


def resize_table_rows(row_nums, table_widget: QTableWidget):
    row_count = table_widget.rowCount()
    sub_row_nums = row_count - row_nums
    # 如果表格当前行大于需要的，那么就移除多余的行
    if sub_row_nums > 0:
        [table_widget.removeRow(i) for i in reversed(range(row_nums, row_count))]
    # 如果表格当前行小于需要的，那么就增加
    elif sub_row_nums < 0:
        for i in range(row_count, row_nums):
            table_widget.insertRow(i)
            # 设置checkbox在第一列
            table_check_item = TableWidgetItem(table_widget)
            table_check_item.setCheckState(Qt.Unchecked)
            # 加上行号
            table_check_item.setText(i + 1)
            table_widget.setItem(i, 0, table_check_item)


