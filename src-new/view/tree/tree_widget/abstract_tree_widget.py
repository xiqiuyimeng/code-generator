# -*- coding: utf-8 -*-
"""
树结构抽象类，实现了智能展示滚动条功能，智能搜索功能
但是树节点复选框点击信号没有直接可以用的方法，经过计算可以获取复选框矩形，理论上点击坐标处于矩形内，可以发送复选框点击信号，
经测试发现，在矩形四角处似乎有问题，由于复选框圆角问题，导致圆角外坐标判断正确，却不能触发复选框点击状态变化，可能导致逻辑bug
所以根据树节点点击且导致复选框改变的需求，经过测试发现相关事件与信号的顺序为：
    mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发 -> itemChanged信号 -> clicked信号
    可以在mousePressEvent事件中设置标志位，表明在点击，在itemChanged信号槽函数中判断是否点击，在clicked信号槽函数中重置标志位，
    实现点击复选框触发事件
"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTreeWidgetItem, QMenu

from view.custom_widget.scrollable_widget import ScrollableWidget
from view.searcher.smart_item_view import SmartSearcherTreeWidget

_author_ = 'luwt'
_date_ = '2022/9/14 15:48'


class AbstractTreeWidget(SmartSearcherTreeWidget, ScrollableWidget):

    def __init__(self, parent, window):
        super().__init__(parent)
        self.main_window = window
        # item 是否正在被鼠标左键点击
        self.item_clicked = False
        self.headerItem().setHidden(True)
        # 统一设置图标大小
        self.setIconSize(QSize(40, 30))
        self.connect_signal()

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            # 判断是左键点击，将标志位置位True
            self.item_clicked = True
        super().mousePressEvent(e)

    def connect_signal(self):
        """定义通用的信号槽连接"""
        # 双击树节点事件
        self.doubleClicked.connect(self.open_tree_item)
        # 右击事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_mouse_clicked)
        # 主要为了实现监听复选框点击
        self.itemClicked.connect(self.handle_item_clicked)
        self.itemChanged.connect(self.handle_item_change)

    def open_tree_item(self, idx):
        item = self.itemFromIndex(idx)
        self.do_open_tree_item(item)

    def handle_right_mouse_clicked(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.itemAt(pos)
        if item:
            # 生成右键菜单
            menu = QMenu()
            # 填充右键菜单内容
            self.do_fill_menu(item, menu)
            # 右键菜单点击事件
            menu.triggered.connect(self.handle_right_menu_func)
            # 右键菜单弹出位置跟随焦点位置
            menu.exec_(QCursor.pos())

    def handle_item_clicked(self):
        # 鼠标左键点击结束事件，将标志位置位False
        self.item_clicked = False

    def handle_item_change(self, item: QTreeWidgetItem):
        # 事件信号顺序是：mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发
        # -> itemChanged信号 -> clicked信号
        if self.item_clicked:
            self.do_handle_item_change(item)

    def handle_right_menu_func(self, action):
        """
        点击右键菜单选项后触发事件
        :param action: 右键菜单中的选项
        """
        # 获取右键点击的项
        item = self.currentItem()
        func_name = action.text()
        self.do_handle_right_menu_func(item, func_name)

    def do_open_tree_item(self, item): ...

    def do_fill_menu(self, item, menu): ...

    def do_handle_right_menu_func(self, item, func_name): ...

    def do_handle_item_change(self, item): ...
