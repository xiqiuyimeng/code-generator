# -*- coding: utf-8 -*-
"""
自定义滚动区域部件，进入控件区域时显示滚动条，离开时隐藏
"""
from PyQt5.QtWidgets import QAbstractScrollArea

_author_ = 'luwt'
_date_ = '2022/5/7 17:18'


class ScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, a0):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)
        self.horizontalScrollBar().setHidden(False)

    def leaveEvent(self, a0):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)
        self.horizontalScrollBar().setHidden(True)
