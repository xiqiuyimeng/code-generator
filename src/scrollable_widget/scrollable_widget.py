# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractScrollArea, QTreeWidget, QTableWidget, QScrollArea, QTextBrowser, QTreeWidgetItem

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

    # 定义信号，发送点击复选框的树节点和是否选中
    item_checkbox_clicked = pyqtSignal(QTreeWidgetItem, bool)


class MyTableWidget(QTableWidget, MyScrollableWidget):
    ...


class MyScrollArea(QScrollArea, MyScrollableWidget):
    ...


class MyTextBrowser(QTextBrowser, MyScrollableWidget):
    ...
