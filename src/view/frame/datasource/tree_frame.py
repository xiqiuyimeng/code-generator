# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from src.constant.tree_constant import LOCATION_TXT, CREATE_NEW_FOLDER
from src.enum.ds_category_enum import DsCategoryEnum
from src.view.tree.tree_widget.sql_tree_widget import SqlTreeWidget
from src.view.tree.tree_widget.struct_tree_widget import StructTreeWidget
from src.view.tree.tree_widget.tree_function import add_folder_func
from src.view.tree.tree_widget.tree_widget_abc import TreeWidgetABC
from src.view.window.main_window_func import set_sql_tree_widget, set_struct_tree_widget

_author_ = 'luwt'
_date_ = '2022/9/14 18:01'


def get_tree_frame(current_frame_name, frame_parent):
    """根据当前的frame名称获取对应的树结构frame"""
    if current_frame_name == DsCategoryEnum.sql_ds_category.get_name():
        return SqlTreeFrame(frame_parent)
    elif current_frame_name == DsCategoryEnum.struct_ds_category.get_name():
        return StructTreeFrame(frame_parent)


class TreeFrameABC(QFrame):
    """树结构frame抽象类"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
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
        self.tree_locate_button.setObjectName('locate_button')
        self.tree_locate_button.setText(LOCATION_TXT)
        # 设置比例
        self.header_layout.setStretch(0, 1)
        self.header_layout.addWidget(self.tree_locate_button)

        self.tree_widget = self.get_tree_widget()
        self.tree_widget.setObjectName('tree_widget')
        self.tree_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._layout.addWidget(self.tree_widget)

        self.tree_locate_button.clicked.connect(self.tree_widget.locate_item)

    def reopen_tree(self):
        self.tree_widget.reopen_tree()

    def get_header_text(self) -> str:
        ...

    def get_tree_widget(self) -> TreeWidgetABC:
        ...


class SqlTreeFrame(TreeFrameABC):
    """sql数据源列表frame"""

    def __init__(self, parent):
        super().__init__(parent)
        # 保存引用
        set_sql_tree_widget(self.tree_widget)

    def get_header_text(self) -> str:
        return DsCategoryEnum.sql_ds_category.get_name()

    def get_tree_widget(self) -> SqlTreeWidget:
        return SqlTreeWidget(self)


class StructTreeFrame(TreeFrameABC):
    """结构体数据源列表frame"""

    def __init__(self, parent):
        self.tree_widget: StructTreeWidget = ...
        super().__init__(parent)

        # 增加新建文件夹按钮
        self.create_folder_button = QPushButton(self)
        self.create_folder_button.setObjectName('create_button')
        self.create_folder_button.setText(CREATE_NEW_FOLDER)
        self.header_layout.insertWidget(1, self.create_folder_button)
        self.create_folder_button.clicked.connect(lambda: add_folder_func(self.tree_widget))
        # 保存引用
        set_struct_tree_widget(self.tree_widget)

    def get_header_text(self) -> str:
        return DsCategoryEnum.struct_ds_category.get_name()

    def get_tree_widget(self) -> StructTreeWidget:
        return StructTreeWidget(self)
