# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.view.tab.tab_widget.tab_widget import TabWidget, SqlTabWidget, StructTabWidget

_author_ = 'luwt'
_date_ = '2022/10/9 18:10'


def get_tab_frame(current_frame_name, frame_parent, window):
    """根据当前的frame名称获取对应的tab frame"""
    if current_frame_name == SQL_DS_CATEGORY:
        return SqlTabFrame(frame_parent, window)
    elif current_frame_name == STRUCT_DS_CATEGORY:
        return StructTabFrame(frame_parent, window)


class AbstractTabFrame(QFrame):
    """tab frame抽象类"""

    def __init__(self, parent, window):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('tab_frame')

        self._layout = QVBoxLayout(self)

        self.tab_widget = self.get_tab_widget(window)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.tab_widget)

    def get_tab_widget(self, window) -> TabWidget: ...


class SqlTabFrame(AbstractTabFrame):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问
        window.sql_tab_widget = self.tab_widget

    def get_tab_widget(self, window) -> TabWidget:
        return SqlTabWidget(self, window)


class StructTabFrame(AbstractTabFrame):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问
        window.struct_tab_widget = self.tab_widget

    def get_tab_widget(self, window) -> TabWidget:
        return StructTabWidget(self, window)
