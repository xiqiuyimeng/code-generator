# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from constant.constant import SQL_DATASOURCE_TYPE, STRUCT_DATASOURCE_TYPE
from view.tab.tab_widget import TabWidget

_author_ = 'luwt'
_date_ = '2022/10/9 18:10'


def get_tab_frame(current_frame_name, frame_parent, window):
    """根据当前的frame名称获取对应的tab frame"""
    if current_frame_name == SQL_DATASOURCE_TYPE:
        return SqlTabFrame(frame_parent, window)
    elif current_frame_name == STRUCT_DATASOURCE_TYPE:
        return StructureTabFrame(frame_parent, window)


class AbstractTabFrame(QFrame):
    """tab frame抽象类"""

    def __init__(self, parent, window):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName('tab_frame')

        self._layout = QVBoxLayout(self)

        self.tab_widget = TabWidget(self, main_window=window)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._layout.addWidget(self.tab_widget)


class SqlTabFrame(AbstractTabFrame):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问
        window.sql_tab_widget = self.tab_widget


class StructureTabFrame(AbstractTabFrame):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 为了方便访问
        window.structure_tab_widget = self.tab_widget
