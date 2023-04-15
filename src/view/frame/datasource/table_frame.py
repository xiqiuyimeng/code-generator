# -*- coding: utf-8 -*-
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.view.table.table_widget.ds_table_widget.ds_col_table_widget_abc import DsColTableWidgetABC
from src.view.table.table_widget.ds_table_widget.sql_table_widget import SqlDsColTableWidget
from src.view.table.table_widget.ds_table_widget.struct_table_widget import StructDsColTableWidget

_author_ = 'luwt'
_date_ = '2022/9/26 19:28'


def get_table_frame(current_frame_name, *args):
    """根据当前的frame名称获取对应的表结构frame"""
    if current_frame_name == SQL_DS_CATEGORY:
        return SqlTableFrame(*args)
    elif current_frame_name == STRUCT_DS_CATEGORY:
        return StructTableFrame(*args)


class TableFrameABC(QFrame):
    """表结构frame抽象类"""

    def __init__(self, main_window, parent, column_list, tree_item, tree_widget):
        super().__init__(parent)
        self.main_window = main_window
        self.column_list = column_list
        self.tree_item = tree_item
        self.tree_widget = tree_widget
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('table_frame')

        self.table_header_label = QLabel(self)
        self.table_header_label.setObjectName('table_header_label')
        header_label_text = self.get_header_label_text()
        self.table_header_label.setText(header_label_text)

        # 设置气泡提示内容
        parent.setToolTip(header_label_text)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.table_header_label)

        self.table_widget = ...
        self.add_table()

    def get_header_label_text(self) -> str: ...

    def get_table_widget(self) -> DsColTableWidgetABC: ...

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


class SqlTableFrame(TableFrameABC):
    """sql数据源表格frame"""

    def get_header_label_text(self) -> str:
        return f'数据库连接：{self.tree_item.parent().parent().text(0)}\n' \
               f'当前数据库：{self.tree_item.parent().text(0)}\n' \
               f'当前数据表：{self.tree_item.text(0)}'

    def get_table_widget(self) -> DsColTableWidgetABC:
        return SqlDsColTableWidget(self.main_window, self.tree_widget, self, self.column_list)


class StructTableFrame(TableFrameABC):
    """结构体数据源表格frame"""

    def get_header_label_text(self) -> str:
        return f'当前结构体：{self.tree_item.text(0)}'

    def get_table_widget(self) -> DsColTableWidgetABC:
        return StructDsColTableWidget(self.main_window, self.tree_widget, self, self.column_list)



