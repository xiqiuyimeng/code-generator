# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QPushButton

from constant.constant import STRUCTURE_TABLE_HEADER_BUTTON_TXT, SQL_DATASOURCE_TYPE, STRUCTURE_DATASOURCE_TYPE
from view.table.table_widget import TableWidget

_author_ = 'luwt'
_date_ = '2022/9/26 19:28'


def get_table_frame(current_frame_name, *args):
    """根据当前的frame名称获取对应的表结构frame"""
    if current_frame_name == SQL_DATASOURCE_TYPE:
        return SqlTableFrame(*args)
    elif current_frame_name == STRUCTURE_DATASOURCE_TYPE:
        return StructureTableFrame(*args)


class AbstractTableFrame(QFrame):
    """表结构frame抽象类"""

    def __init__(self, parent, column_list, item):
        super().__init__(parent)
        self.item = item
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('table_frame')

        self.table_header_label = QLabel(self)
        self.table_header_label.setObjectName('table_header_label')
        header_label_text = self.get_header_label_text()
        self.table_header_label.setText(header_label_text)

        parent.setToolTip(header_label_text)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.get_header_widget())

        self.table_widget = TableWidget(self)
        self.table_widget.setObjectName('table_widget')
        self.table_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.table_widget)

        self.table_widget.fill_table(column_list)

    def get_header_widget(self) -> QWidget: ...

    def get_header_label_text(self) -> str: ...


class SqlTableFrame(AbstractTableFrame):
    """sql数据源表格frame"""

    def __init__(self, *args):
        super().__init__(*args)

    def get_header_widget(self) -> QWidget:
        return self.table_header_label

    def get_header_label_text(self) -> str:
        return f'数据库连接：{self.item.parent().parent().text(0)}\n' \
               f'当前数据库：{self.item.parent().text(0)}\n' \
               f'当前数据表：{self.item.text(0)}'


class StructureTableFrame(AbstractTableFrame):
    """结构体数据源表格frame"""

    def __init__(self, *args):
        super().__init__(*args)
        self.header_widget = ...
        self.header_widget_layout = ...
        self.header_button = ...

    def get_header_widget(self) -> QWidget:
        self.header_widget = QWidget()
        self.header_widget.setObjectName('structure_table_header')
        self.header_widget_layout = QVBoxLayout(self.header_widget)

        self.header_button = QPushButton()
        self.header_button.setObjectName('structure_header_button')
        self.header_button.setText(STRUCTURE_TABLE_HEADER_BUTTON_TXT)

        self.header_widget_layout.addWidget(self.header_button)
        self.header_widget_layout.addWidget(self.table_header_label)
        return self.header_widget



