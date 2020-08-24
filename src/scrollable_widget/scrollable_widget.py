# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAbstractScrollArea, QTreeWidget, QTableWidget, QScrollArea, QTextBrowser

_author_ = 'luwt'
_date_ = '2020/8/24 15:41'


class MyScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, a0):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)

    def leaveEvent(self, a0):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)


class MyTreeWidget(QTreeWidget, MyScrollableWidget):
    ...


class MyTableWidget(QTableWidget, MyScrollableWidget):
    ...


class MyScrollArea(QScrollArea, MyScrollableWidget):
    ...


class MyTextBrowser(QTextBrowser, MyScrollableWidget):
    ...
