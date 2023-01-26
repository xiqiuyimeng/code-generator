# -*- coding: utf-8 -*-
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

from constant.constant import SQL_DATASOURCE_TYPE, STRUCT_DATASOURCE_TYPE
from view.table.table_widget.abstract_table_widget import AbstractTableWidget
from view.table.table_widget.sql_table_widget import SqlTableWidget
from view.table.table_widget.struct_table_widget import StructTableWidget

_author_ = 'luwt'
_date_ = '2022/9/26 19:28'


def get_table_frame(current_frame_name, *args):
    """根据当前的frame名称获取对应的表结构frame"""
    if current_frame_name == SQL_DATASOURCE_TYPE:
        return SqlTableFrame(*args)
    elif current_frame_name == STRUCT_DATASOURCE_TYPE:
        return StructTableFrame(*args)


class AbstractTableFrame(QFrame):
    """表结构frame抽象类"""

    def __init__(self, main_window, parent, column_list, tree_item):
        super().__init__(parent)
        self.main_window = main_window
        self.column_list = column_list
        self.tree_item = tree_item
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('table_frame')

        self.table_header_label = QLabel(self)
        self.table_header_label.setObjectName('table_header_label')
        header_label_text = self.get_header_label_text()
        self.table_header_label.setText(header_label_text)

        parent.setToolTip(header_label_text)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.table_header_label)

        self.table_widget = ...
        self.add_table()

    def get_header_label_text(self) -> str: ...

    def get_table_widget(self) -> AbstractTableWidget: ...

    def refresh_ui(self, column_list):
        self.column_list = column_list
        self._layout.removeWidget(self.table_widget)
        sip.delete(self.table_widget)
        self.add_table()

    def add_table(self):
        self.table_widget = self.get_table_widget()
        self.table_widget.setObjectName('table_widget')
        self.table_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.table_widget)

        self.table_widget.fill_table()


class SqlTableFrame(AbstractTableFrame):
    """sql数据源表格frame"""

    def get_header_label_text(self) -> str:
        return f'数据库连接：{self.tree_item.parent().parent().text(0)}\n' \
               f'当前数据库：{self.tree_item.parent().text(0)}\n' \
               f'当前数据表：{self.tree_item.text(0)}'

    def get_table_widget(self) -> AbstractTableWidget:
        return SqlTableWidget(self.main_window, self, self.column_list)


class StructTableFrame(AbstractTableFrame):
    """结构体数据源表格frame"""

    def get_header_label_text(self) -> str:
        return f'当前结构体：{self.tree_item.text(0)}'

    def get_table_widget(self) -> AbstractTableWidget:
        return StructTableWidget(self.main_window, self, self.column_list)



