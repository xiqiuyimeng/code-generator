# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.constant.tree_constant import LOCATION_TXT, CREATE_NEW_FOLDER
from src.view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from src.view.tree.tree_widget.sql_tree_widget import SqlTreeWidget
from src.view.tree.tree_widget.struct_tree_widget import StructTreeWidget
from src.view.tree.tree_widget.tree_function import add_folder_func

_author_ = 'luwt'
_date_ = '2022/9/14 18:01'


def get_tree_frame(current_frame_name, frame_parent, window):
    """根据当前的frame名称获取对应的树结构frame"""
    if current_frame_name == SQL_DS_CATEGORY:
        return SqlTreeFrame(frame_parent, window)
    elif current_frame_name == STRUCT_DS_CATEGORY:
        return StructureTreeFrame(frame_parent, window)


class AbstractTreeFrame(QFrame):
    """树结构frame抽象类"""

    def __init__(self, parent, window):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('tree_frame')

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout = QHBoxLayout()
        self._layout.addLayout(self.header_layout)

        # 树头部标题
        self.tree_header_label = QLabel(self)
        self.tree_header_label.setText(self.get_header_text())
        self.tree_header_label.setObjectName('tree_header_label')
        self.header_layout.addWidget(self.tree_header_label)

        self.tree_locate_button = QPushButton(self)
        self.tree_locate_button.setText(LOCATION_TXT)
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
        return SQL_DS_CATEGORY

    def get_tree_widget(self, window) -> SqlTreeWidget:
        return SqlTreeWidget(self, window)


class StructureTreeFrame(AbstractTreeFrame):
    """结构体数据源列表frame"""

    def __init__(self, parent, window):
        self.tree_widget: StructTreeWidget = ...
        super().__init__(parent, window)

        # 增加新建文件夹按钮
        self.create_folder_button = QPushButton(self)
        self.create_folder_button.setText(CREATE_NEW_FOLDER)
        self.header_layout.insertWidget(1, self.create_folder_button)
        self.create_folder_button.clicked.connect(
            lambda: add_folder_func(window.geometry(), self.tree_widget))

        # 为了方便访问，树部件引用也挂到window上
        window.struct_tree_widget = self.tree_widget

    def get_header_text(self) -> str:
        return STRUCT_DS_CATEGORY

    def get_tree_widget(self, window) -> StructTreeWidget:
        return StructTreeWidget(self, window)
