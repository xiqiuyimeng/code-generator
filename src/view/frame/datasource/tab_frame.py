# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from src.service.system_storage.ds_category_sqlite import DsCategoryEnum
from src.view.tab.tab_widget.tab_widget import TabWidget, SqlTabWidget, StructTabWidget
from src.view.window.main_window_func import set_sql_tab_widget, set_struct_tab_widget

_author_ = 'luwt'
_date_ = '2022/10/9 18:10'


def get_tab_frame(current_frame_name, frame_parent):
    """根据当前的frame名称获取对应的tab frame"""
    if current_frame_name == DsCategoryEnum.sql_ds_category.value.name:
        return SqlTabFrame(frame_parent)
    elif current_frame_name == DsCategoryEnum.struct_ds_category.value.name:
        return StructTabFrame(frame_parent)


class TabFrameABC(QFrame):
    """tab frame抽象类"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('tab_frame')

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = self.get_tab_widget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.tab_widget)

    def get_tab_widget(self) -> TabWidget: ...


class SqlTabFrame(TabFrameABC):

    def __init__(self, parent):
        super().__init__(parent)
        # 保存引用
        set_sql_tab_widget(self.tab_widget)

    def get_tab_widget(self) -> TabWidget:
        return SqlTabWidget(self)


class StructTabFrame(TabFrameABC):

    def __init__(self, parent):
        super().__init__(parent)
        # 保存引用
        set_struct_tab_widget(self.tab_widget)

    def get_tab_widget(self) -> TabWidget:
        return StructTabWidget(self)
