# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from constant.constant import SQL_DATASOURCE_TYPE, STRUCTURE_DATASOURCE_TYPE
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from view.tree.tree_widget.sql_tree_widget import SqlTreeWidget
from view.tree.tree_widget.structure_tree_widget import StructureTreeWidget

_author_ = 'luwt'
_date_ = '2022/9/14 18:01'


def get_tree_frame(current_frame_name, frame_parent, window):
    """根据当前的frame名称获取对应的树结构frame"""
    if current_frame_name == SQL_DATASOURCE_TYPE:
        return SqlTreeFrame(frame_parent, window)
    elif current_frame_name == STRUCTURE_DATASOURCE_TYPE:
        return StructureTreeFrame(frame_parent, window)


class AbstractTreeFrame(QFrame):
    """树结构frame抽象类"""

    def __init__(self, parent, window):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('tree_frame')

        self._layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()
        self._layout.addLayout(self.header_layout)

        # 树头部标题
        self.tree_header_label = QLabel(self)
        self.tree_header_label.setText(self.get_header_text())
        self.tree_header_label.setObjectName('tree_header_label')
        self.header_layout.addWidget(self.tree_header_label)

        self.tree_locate_button = QPushButton(self)
        self.tree_locate_button.setText('定位')
        # 设置比例
        self.header_layout.setStretch(0, 1)
        self.header_layout.addWidget(self.tree_locate_button)

        self.tree_widget = self.get_tree_widget(window)
        self.tree_widget.setObjectName('tree_widget')
        self.tree_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.tree_widget)

        self.tree_locate_button.clicked.connect(self.tree_widget.locate_item)

    def reopen_tree(self):
        self.tree_widget.reopen_tree()

    def get_header_text(self) -> str: ...

    def get_tree_widget(self, window) -> AbstractTreeWidget: ...


class SqlTreeFrame(AbstractTreeFrame):
    """sql数据源列表frame"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问，树部件引用也挂到window上
        window.sql_tree_widget = self.tree_widget

    def get_header_text(self) -> str:
        return SQL_DATASOURCE_TYPE

    def get_tree_widget(self, window) -> AbstractTreeWidget:
        return SqlTreeWidget(self, window)


class StructureTreeFrame(AbstractTreeFrame):
    """结构体数据源列表frame"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问，树部件引用也挂到window上
        window.structure_tree_widget = self.tree_widget

    def get_header_text(self) -> str:
        return STRUCTURE_DATASOURCE_TYPE

    def get_tree_widget(self, window) -> AbstractTreeWidget:
        return StructureTreeWidget(self, window)