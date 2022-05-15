# -*- coding: utf-8 -*-
"""
树结构，实现了智能展示滚动条功能，智能搜索功能
但是树节点复选框点击信号没有直接可以用的方法，经过计算可以获取复选框矩形，理论上点击坐标处于矩形内，可以发送复选框点击信号，
经测试发现，在矩形四角处似乎有问题，由于复选框圆角问题，导致圆角外坐标判断正确，却不能触发复选框点击状态变化，可能导致逻辑bug
所以根据树节点中数据变化时来判断是否发送复选框点击信号
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from view.custom_widget.scrollable_widget import ScrollableWidget
from view.searcher.smart_item_view import SmartSearcherTreeWidget

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class TreeWidget(QTreeWidget, ScrollableWidget, SmartSearcherTreeWidget):

    # 定义信号，发送点击复选框的树节点和选中状态：全选、部分选、未选择
    item_checkbox_clicked = pyqtSignal(QTreeWidgetItem, int)


